import csv

# BAREBONES CHATBOT
# get intents
# read from csv
datafile = open('intents.csv', 'r')
datareader = csv.reader(datafile, delimiter=';')
arrayIntents = []
for row in datareader:
    arrayIntents.append(row)

# add information to start of each row
# row 0 = first intent, row 1 = second intent...
# position 0 = score, position 1 = score moderated by number of patterns, pos 2 = ranking by score,
# pos 3 = ranking by moderated score, pos 4 = mixed ranking (used for output)
# pos 5 = category name, pos 6 = answer, pos 7 - XXX = patterns

startStuffing = [99.0, 99.0, 99.0, 0.0, 0.0]
for s in range(len(startStuffing)):
    for j in range(len(arrayIntents)): # iterate through rows
        arrayIntents[j].insert(0,startStuffing[s])

# convert array to lowercase
for j in range(len(arrayIntents)):  # iterate through rows
    for k in range(len(arrayIntents[j])):  # iterate through columns
        if k > 6:
            arrayIntents[j][k] = arrayIntents[j][k].lower()

# prepare question
def prepareQuestion (questionToAsk):

    # convert question to lowercase
    questionToAskLower = questionToAsk.lower()

    # convert question to list
    splitEarly = questionToAskLower.split()

    # remove word after "nicht"
    for i in range(len(splitEarly) - 1):  # iterate through input
        if (splitEarly[i] == "nicht"):
            splitEarly.pop(i + 1)

    # convert list to string
    splitInput = ""
    for i in splitEarly:
        splitInput += i + " "

    return splitInput

def getBBScore (splitInput):
    # reset all scores and ranks to default (positions 0 - 4; 0.0, 0.0, 99.0, 99.0, 99.0)
    for j in range(len(arrayIntents)):  # iterate through intent rows
        arrayIntents[j][0] = 0.0
        arrayIntents[j][1] = 0.0
        arrayIntents[j][2] = 99.0
        arrayIntents[j][3] = 99.0
        arrayIntents[j][4] = 99.0

    # get barebones score
    for j in range(len(arrayIntents)):  # iterate through intent rows
        for k in range(len(arrayIntents[j])):  # iterate through intent columns
            if k > 6:
                if arrayIntents[j][k] in splitInput:
                    arrayIntents[j][0] = arrayIntents[j][0] + 1
                    print("\nWort " + str(arrayIntents[j][k]) + " gefunden in Reihe " + str(j) + " an Stelle " + str(k) + ", ganze Zeile: " + str(arrayIntents[j]))

    # get score moderated by length
    for j in range(len(arrayIntents)): # iterate through rows
            arrayIntents[j][1] = ((arrayIntents[j][0])/(len((arrayIntents[j])) - 8))

    return arrayIntents

def rankByScore(regIntents, ref, trg):

    # sort by score
    rankedIntents = sorted(regIntents, key=lambda x: x[ref], reverse=True)

    # write place
    n = 0  # rank counter
    m = 0  # duplicate counter

    for j in range(len(rankedIntents) - 1): # iterate through rows
        if rankedIntents[j][ref] != rankedIntents[j+1][ref]:        # no more duplicates
            if rankedIntents[j][ref] != rankedIntents[j-1][ref]:    # first after duplicates
                n = n + m
                rankedIntents[j][trg] = n
                n = n + 1
                m = 0
            else:                                               # last of duplicates
                rankedIntents[j][trg] = n
                m = m + 1
        else:                                                   # duplicate
            rankedIntents[j][trg] = n
            m = m + 1

    # rank last position
    lastPos = (len(rankedIntents) - 1)

    if rankedIntents[lastPos - 1][ref] > rankedIntents[lastPos][ref]:
        rankedIntents[lastPos][trg] = (rankedIntents[lastPos - 1][trg] + 1)
    else:
        rankedIntents[lastPos][trg] = (rankedIntents[lastPos - 1][trg])

    return rankedIntents

# get rank for regular score
def rankByRegScore (arrayIntents):
    rankIntents = rankByScore(arrayIntents, 0, 2)
    return rankIntents

# get rank for moderated score
def rankModerated(rankIntents):
    rankIntents = rankByScore(rankIntents, 1, 3)
    return rankIntents

# get mixed rank
def mixedRank(rankIntents):
    for j in range(len(rankIntents)): # iterate through rows
        rankIntents[j][4] = (((rankIntents[j][2])+(rankIntents[j][3])))

    rankIntents = sorted(rankIntents, key=lambda x: x[4], reverse=False)
    return rankIntents

def getRankedIntents(questionToAsk):
    splitInput = prepareQuestion(questionToAsk)
    arrayIntents = getBBScore(splitInput)
    rankIntents = rankByRegScore(arrayIntents)
    rankIntents = rankModerated(rankIntents)
    rankIntents = mixedRank(rankIntents)
    return rankIntents