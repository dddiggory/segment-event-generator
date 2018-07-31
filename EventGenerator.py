import json
import analytics
import uuid
import time
import random
import datetime
import requests
import time

#insert your Segment Write Key here
SEGMENT_WRITE_KEY = "6f4pcfvQXv60D3gWgB1YUAW8N5A82Tu8"

if SEGMENT_WRITE_KEY == "":
	SEGMENT_WRITE_KEY = raw_input("Insert your Segment write key (or hardcode @ line 11):  ")

analytics.write_key = SEGMENT_WRITE_KEY

NUMBER_OF_USERS = 450

start_time = time.time()

def randomDate(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)

def reformat(userStr):
	try:
		return ((userStr.decode('utf-8')).replace("\"",""))
	except:
		return userStr


with open("bills.json") as readfile:
	eventData = json.load(readfile)

	eventChoices = [
		"Application Opened",
		"Vote",
		"Bill View"
	]

	d1 = datetime.datetime.now() - datetime.timedelta(days=5)
	d2 = datetime.datetime.now()

	for iteration in range(NUMBER_OF_USERS):
		
		random_user = str(uuid.uuid4())
		
		randomUserList = json.loads(requests.get("https://uinames.com/api/?ext&amount="+str(NUMBER_OF_USERS)).text)
		currentUser = randomUserList[iteration]

		userName = reformat(currentUser["name"] + " " + currentUser["surname"])
		userEmail = reformat(currentUser["email"])
		userRegion = reformat(currentUser["region"])
		userDOB = reformat(currentUser["birthday"]["mdy"])
		userAge = reformat(currentUser["age"])
		userPhone = reformat(currentUser["phone"])
		userTraits = {
			"name": userName, "email": userEmail, "Region": userRegion, "birthday": userDOB,
			"age": userAge, "phone": userPhone
		}
		analytics.identify(random_user, userTraits)

		NUMBER_OF_EVENTS = random.randint(1, 20)
		elapsed_seconds = time.time() - start_time
		elapsed = (datetime.datetime(1,1,1) + datetime.timedelta(seconds=elapsed_seconds))

		print "("+str(elapsed.minute) + ":" + str(elapsed.second).zfill(2) + ") " + str(iteration) + ": " + userName + ", " + str(NUMBER_OF_EVENTS) + " events."

		for subiteration in range(NUMBER_OF_EVENTS):
			eventName = random.choice(eventChoices)
			billChoice = random.choice(eventData["data"])
			randomTimestamp = randomDate(d1, d2)
			eventProperties = {}

			if eventName == "Application Opened":
				analytics.track(random_user, eventName, timestamp=randomTimestamp)
			
			elif eventName == "Vote":
				eventProperties = {
					"Current Bill": billChoice["key"], "Bill ID": billChoice["billRef"], 
					"User Scrolled?": random.choice([True, False]), 
					"Vote Type": random.choice(["Yea", "Nay"]),
					"Bill Category": random.choice(["environment", "economy", "immigration", "firearms", "drugs", "nuclear weapons", "civil rights", "privacy", "international trade"])
					}
				analytics.track(random_user, "Vote", eventProperties, timestamp=randomTimestamp)
			
			elif eventName == "Bill View":
				eventProperties = {
					"Current Bill": billChoice["key"], "Bill ID": billChoice["billRef"],
					"Bill Category": random.choice(["environment", "economy", "immigration", "firearms", "drugs", "nuclear weapons", "civil rights", "privacy", "international trade"])
					}
				analytics.track(random_user, "Bill View", eventProperties, timestamp=randomTimestamp)




		