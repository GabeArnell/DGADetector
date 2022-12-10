#!/usr/bin/python3

import sys
from datetime import *

domain = sys.argv[1].lower()
topleveldomain = domain.split(".")[-1].lower().strip()
print("Checking domain: ", domain)
print("Top level domain: ", topleveldomain)

topDomainScore = 100
wordMatchScore = 100
lengthScore = 100
ageScore = 100

topdomFile = open("badtoplevels.txt", "r")
topdomList = topdomFile.read().split("\n")
topdomFile.close()

print("\n = Checking Top Level Domain = ")
for d in topdomList:
    if d.lower().strip() == topleveldomain:
        print("Top Level Domain is suspicious: ."+topleveldomain)
        topDomainScore = 0
if topDomainScore == 100:
    print("Domain not found on suspicion list")

print("\n = Checking Word Matching = ")
letterList = []
for l in domain:
    if l == ".":
        break
    letterList.append(False)

#print("Letter Slots", letterList)
# checking words that exist
wordsFile = open("words.txt", "r")
wordList = wordsFile.read().split("\n")
wordsFile.close()

for word in wordList:
    word = word.strip().lower()
    if word in domain and len(word) > 2:
        s = domain.find(word)
        e = s+len(word)
        print("Word in domain", word)
        for i in range(s,e):
            if len(letterList) > i:
                letterList[i] = True
                
unusedPenalty = 100 / len(domain) * 2
for test in letterList:
    if test == False:
        wordMatchScore -= unusedPenalty
wordMatchScore = round(wordMatchScore)
if (wordMatchScore < 0):
    wordMatchScore = 0

#print("New Letter Slots", letterList)


print("\n = Checking Length = ")
lengthPenalty = 5
cropLength = len(domain) - len(topleveldomain)
if (cropLength > 12):
    print("length is considerably long, marking off some points")
    while cropLength > 12:
        lengthScore -= lengthPenalty
        lengthPenalty +=1
        cropLength -= 1
if lengthScore < 0:
    lengthScore = 0


print("\n = Checking WhoIs Lookup = ")
import whois
print("Current Date", date.today())
dayPenalty = 1
try:
    w = whois.whois(domain)
    creationDate = w["creation_date"].date()
    #print(type(creationDate))
    print("Domain Creation Date: ", creationDate)
    dayDiff = str(date.today() - creationDate).split(" ")[0]
    dayDiff = int(dayDiff)
    print("Domain created", dayDiff, " day(s) ago.")
    if (dayDiff <= 30):
        print("Domain is considerably new, deducting points.")
        while cropLength > 12:
            ageScore -= dayPenalty
            dayPenalty +=1
            dayDiff -= 1
    else:
    	print("Domain old enough.")
except:
    print("No domain found on WhoIS")
    print("Giving avg score")
    ageScore = 25

if ageScore < 0:
    ageScore = 0


finalScore = topDomainScore + wordMatchScore + lengthScore + ageScore
finalScore = round(finalScore/4)
print("\n = Results = ")
print("Top Level Score", topDomainScore)
print("Word Match Score", wordMatchScore)
print("Length Score", lengthScore)
print("Age Score", ageScore)
print("Final Score: ", finalScore)
if finalScore <= 60:
    print("\nDomain is likely malicious/generated")
else:
    print("\nDomain is not likely malicious/generated")

