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
startStuffing = [0.0, 0.0, 99.0, 99.0, 99.0]
for s in range(len(startStuffing)):
    for j in range(len(arrayIntents)): # iterate through rows
        arrayIntents[j].insert(0,startStuffing[s])

# prepare question
def prepareQuestion (questionToAsk):

    splitInput = questionToAsk.split()

    for i in range(len(splitInput) - 1): # iterate through input
        if (splitInput[i] == "nicht"):
            splitInput.pop(i+1)

    # remove duplicates
    splitInput = list(dict.fromkeys(splitInput))

    return splitInput

def getBBScore (splitInput):
    # get barebones score
    for i in range(len(splitInput)): # iterate through input
        for j in range(len(arrayIntents)): # iterate through rows
            for k in range(len(arrayIntents[j])): # iterate through columns
                if splitInput[i] == arrayIntents[j][k]:
                    if k > 6:
                        arrayIntents[j][0] = arrayIntents[j][0] + 1

    # get score moderated by length
    for i in range(len(splitInput)): # iterate through input
        for j in range(len(arrayIntents)): # iterate through rows
            # if arrayIntents[j][0] != 0: # otherwise division by zero
            arrayIntents[j][1] = ((arrayIntents[j][0])/(len((arrayIntents[j])) - 7))
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
# https://stackoverflow.com/questions/20183069/how-to-sort-multidimensional-array-by-column
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