import json
import analytics
import uuid
import time
import random
import datetime
import requests
import time

#User Inputs
SEGMENT_WRITE_KEY = "" #insert your Segment Write Key here
NUMBER_OF_USERS = None #Keep below 500 for the sake of the Random User API.

if SEGMENT_WRITE_KEY == "":
	SEGMENT_WRITE_KEY = raw_input("Insert your Segment write key (or hardcode @ line 11):  ")
analytics.write_key = SEGMENT_WRITE_KEY

if NUMBER_OF_USERS == None:
	print "How many users to generate? (or hardcode @ line 12)"
	NUMBER_OF_USERS = raw_input("Integer between 1 and 500:  ")
	try:
		NUMBER_OF_USERS = int(NUMBER_OF_USERS)
	except:
		print "Bad input; defaulting to 500."
		NUMBER_OF_USERS = 500

	if NUMBER_OF_USERS > 500:
		NUMBER_OF_USERS = 500

print "Generating " + str(NUMBER_OF_USERS) + " users. You can overwrite this on line 11."



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
		"Bill View",
		"Comment"
	]

	d1 = datetime.datetime.now() - datetime.timedelta(days=5)
	d2 = datetime.datetime.now()

	for iteration in range(NUMBER_OF_USERS):
		
		random_user = str(uuid.uuid4())
		
		randomUserList = json.loads(requests.get("https://uinames.com/api/?ext&amount="+str(NUMBER_OF_USERS)).text)
		try:
			currentUser = randomUserList[iteration]
		except KeyError: # if only 1 user is requested, API will return a Dict, not a List.
			currentUser = randomUserList

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
				continue
			
			elif eventName == "Vote" or eventName == "Comment":
				eventProperties = {
					"Current Bill": billChoice["key"], "Bill ID": billChoice["billRef"], 
					"User Scrolled?": random.choice([True, False]), 
					"Vote Type": random.choice(["Yea", "Nay"]),
					"Bill Category": random.choice(["environment", "economy", "immigration", "firearms", "drugs", "nuclear weapons", "civil rights", "privacy", "international trade"]),
					"Current Vote Count": random.randint(0,20000)
					}
			
			elif eventName == "Bill View":
				eventProperties = {
					"Current Bill": billChoice["key"], "Bill ID": billChoice["billRef"],
					"Bill Category": random.choice(["environment", "economy", "immigration", "firearms", "drugs", "nuclear weapons", "civil rights", "privacy", "international trade"]),
					"Current Vote Count": random.randint(0,20000)
					}

			analytics.track(random_user, eventName, eventProperties, timestamp=randomTimestamp)


		