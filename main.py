# fix lowercase
# fix puncutation
# fix timer: https://stackoverflow.com/questions/85451/pythons-time-clock-vs-time-time-accuracy
# time.perf_counter() (process time ist nur PROZESS-weit)
# siehe https://stackoverflow.com/questions/7370801/how-to-measure-elapsed-time-in-python

# fix csv read: https://www.delftstack.com/de/howto/python/python-read-csv-into-array/ (PRIO 2!)
# pre-define array intents with FLOAT (= 0.0 and 99.0) so it's not int: PRIO 1

# achtung: muss man als liste initialisieren, oder? sonst BLEIBT es empty?
# geht das bei loops mit dem abfangen leerer listen?
# was wenn es liste WAR, aber dann empty IST (aktuell bei neuem durchlauf nummer xyz)?

# firstRUn noch mal fixen am ende dann

# kleinschreibung, punctuation muss nicht weg, da ist er "robust"

# bleibt: csv-read (nimmer heute)

import time
from model import classify, response, numberOfEpochs, timeDifferenceBuilding
from bb import getRankedIntents

thesisMode = True

if thesisMode:
    questionToAsk = "Kann ich mit 5 Freunden draussen an einem Tisch im Biergarten sitzen?"
    answerExpected = "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."
else:
    print("\n----------\n")
    questionToAsk = input("Please enter the question you want to ask: ")

firstRun = False

# NEURAL NETWORK MODEL

if firstRun:

    print("----------\n")
    timeBeforeAnswer = time.perf_counter() * 1000.0

    classified = classify(questionToAsk)
    if isinstance(classified, list):
        classed = str((classify(questionToAsk))[0][0])
        percNN = str((classify(questionToAsk))[0][1])
    else:
        classed = "No categorization possible since threshold was not met (NN)."
        percNN = "(not available)"

    print(classed)
    print(percNN)
    print("\n")

    print(response(questionToAsk))
    timeAfterAnswer = time.perf_counter() * 1000.0
    timeDifferenceAnswerFloat = (timeAfterAnswer - timeBeforeAnswer)
    timeDifferenceAnswer = "{:.2f}".format(timeDifferenceAnswerFloat)
    print("\n----------\n")
    print("It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model" + ".\n")
    print("The number of epochs was " + str(numberOfEpochs) + " (" + str(float(timeDifferenceBuilding)/float(numberOfEpochs)) + " ms per epoch).\n")
    print("It took " + timeDifferenceAnswer + " milliseconds to answer the question via the NN model.")

# BAREBONES MODEL

# arrange array, get answer
# als funktion via def getTime machen; nicht automatisch ablaufen lassen

if firstRun:

    timeBeforeBarebones = time.perf_counter() * 1000.0
    rankIntents = getRankedIntents(questionToAsk)
    timeAfterBarebones = time.perf_counter() * 1000.0
    timeDifferenceBarebones = (timeAfterBarebones - timeBeforeBarebones)

    answerFull = response(questionToAsk)
    if isinstance(answerFull, tuple):
        answerReceived = str(response(questionToAsk)[0])
    else:
        answerReceived = "No answer satisfied the threshold criteria for the NN."

    # output
    print("Answer based on the barebones model: \n")
    if (rankIntents[0][0] > 0):
        answerBB = str(rankIntents[0][6])
        catBB = str(rankIntents[0][5])
        percBB = str(rankIntents[0][1])
    else:
        answerBB = "No answer satisfied the threshold criteria for the BB model."
        catBB = "(not applicable)"
        percBB = "(not applicable)"

    print(answerBB)
    print("It took " + str(timeDifferenceBarebones) + " milliseconds to process the data for the barebones model. \n")


    # def debugInfo(rankIntents):
        # print debug info for BB model
        # for j in range(len(arrayIntents)):
        #    print("Kategorie " + str(rankIntents[j][5]) + " hat " + str(rankIntents[j][0]) + " Punkte; bereinigter Score: " + str(rankIntents[j][1])
        #          + ", \nfinaler Rang: " + str(rankIntents[j][4]) + ", Ranking nach reiner Score: " + str(rankIntents[j][2]) +
        #          ", Ranking moderiert: " + str(rankIntents[j][3]) + "\n")

    # information for thesis
    # determine whether the result from the NN was correct
    if thesisMode:
        if (answerExpected == answerReceived):
             correctAnswer = "yes"
        else:
             correctAnswer = "no"

def writeInfo(answerExpected, rankIntents, answerReceived):

    if (answerExpected == rankIntents[0][6]):
        correctBB = "yes"
    else:
        correctBB = "no"

    if answerReceived != rankIntents[0][6]:
        differentAns = "The models got different results "
        if answerExpected == answerReceived:
            corrOne = "- NN was correct."
        else:
            corrOne = "- BB was correct."
    else:
        differentAns = "Both models got the same results "
        if answerExpected != answerReceived:
            corrOne = "- neither was correct."
        else:
            corrOne = "- both were correct."

    return differentAns, correctBB, corrOne

def safeLog(questionToAsk, classed, correctAnswer, percNN, timeDifferenceBuilding, numberOfEpochs, timeDifferenceAnswer, catBB, correctBB, percBB, timeDifferenceBarebones, differentAns, corrOne):
    # safe results into a file
    comparisonLog = open('log_perf.txt', 'a')
    comparisonLog.write("The question asked was: " + questionToAsk +
                        "\nThe categorization via NN was " + classed + " - correct: " + correctAnswer +
                        ". Percentage match: " + percNN +
                        ". It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model. "
                        + "The number of epochs was " + str(numberOfEpochs) + " (" + str(float(timeDifferenceBuilding)/float(numberOfEpochs))
                        + " ms per epoch). It took " + str(timeDifferenceAnswer) + " milliseconds to answer the question via the NN model.\nThe categorization via BB was "
                        + catBB + " - correct: " + correctBB + ". Percentage match: " + percBB +
                        ". It took " + str(timeDifferenceBarebones) + " milliseconds to structure the BB data and answer the question.\n"
                        + differentAns + corrOne + "\n---------------------\n")
    comparisonLog.close()

def answerLoop(questionToAsk, answerExpected):
    # neural network output
    print("-------Neural network output-------\n")
    timeBeforeAnswer = time.perf_counter() * 1000.0

    print("Classification according to the NN model / percentage match: ")
    classified = classify(questionToAsk)
    if isinstance(classified, list):
        if classified:
            classed = str((classify(questionToAsk))[0][0])
            percNN = str((classify(questionToAsk))[0][1])
        else:
            classed = "No categorization possible since threshold was not met (NN)."
            percNN = "(not available)."
    else:
        classed = "No categorization possible since threshold was not met (NN)."
        percNN = "(not available)."
    print(classed + " / " + percNN)
    print("\n")

    print("Answer according to the NN model: ")
    answerFull = response(questionToAsk)
    if isinstance(answerFull, tuple):
        if answerFull:
            answerReceived = str(response(questionToAsk)[0])
        else:
            answerReceived = "No answer satisfied the threshold criteria for the NN."
    else:
        answerReceived = "No answer satisfied the threshold criteria for the NN."
    print(answerReceived)
    # print("\n----------\n")

    timeAfterAnswer = time.perf_counter() * 1000.0
    timeDifferenceAnswerFloat = (timeAfterAnswer - timeBeforeAnswer)
    timeDifferenceAnswer = "{:.2f}".format(timeDifferenceAnswerFloat)
    print("It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model" + ".\n")
    print("The number of epochs was " + str(numberOfEpochs) + " (" + str(
        float(timeDifferenceBuilding) / float(numberOfEpochs)) + " ms per epoch).\n")
    print("It took " + timeDifferenceAnswer + " milliseconds to answer the question via the NN model.")

# https://stackoverflow.com/questions/85451/pythons-time-clock-vs-time-time-accuracy

    # bb output
    print("-------Barebones output-------\n")

    timeBeforeBarebones = time.perf_counter() * 1000.0
    rankIntents = getRankedIntents(questionToAsk)
    timeAfterBarebones = time.perf_counter() * 1000.0
    timeDifferenceBarebones = (timeAfterBarebones - timeBeforeBarebones)
    print("\nAnswer based on the barebones model: \n")

    if (rankIntents[0][0] > 0):
        answerBB = str(rankIntents[0][6])
        catBB = str(rankIntents[0][5])
        percBB = str(rankIntents[0][1])
    else:
        answerBB = "No answer satisfied the threshold criteria for the BB model."
        catBB = "(not applicable)"
        percBB = "(not applicable)"

    print(answerBB)
    print("It took " + str(timeDifferenceBarebones) + " milliseconds to process the data for the barebones model. \n")

    # meta data
    answerFull = response(questionToAsk)
    if isinstance(answerFull, tuple):
        answerReceived = str(response(questionToAsk)[0])
    else:
        answerReceived = "No answer satisfied the threshold criteria for the NN."

    differentAns = writeInfo(answerExpected, rankIntents, answerReceived)[0]
    correctBB = writeInfo(answerExpected, rankIntents, answerReceived)[1]
    corrOne = writeInfo(answerExpected, rankIntents, answerReceived)[2]
    if (answerExpected == answerReceived):
        correctAnswer = "yes"
    else:
        correctAnswer = "no"
    safeLog(questionToAsk, classed, correctAnswer, percNN, timeDifferenceBuilding, numberOfEpochs, timeDifferenceAnswer, catBB, correctBB, percBB, timeDifferenceBarebones, differentAns, corrOne)

# jetzt arrays mit fragen-antwort-kombinationen definieren
arrayQuestions = [

            ["Kann ich mit 5 Freunden draussen an einem Tisch im Biergarten sitzen?",
        "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],
        ["Kann ich mit 5 Leuten drinnen im geschlossenen Raum sitzen?",
        "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],

        ["KANN ICH MIT 56 LEUTEN DRINNEN??? IM GESCHLOSSENEN RAUM SITZEN????",
                     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],
]

if thesisMode:
    for i in range(len(arrayQuestions)):
        questionToAsk = arrayQuestions[i][0]
        answerExpected = arrayQuestions[i][1]
        answerLoop(questionToAsk, answerExpected)

# dieses array durchlesen lassen und als questionToAsk und answerExpected an answerLoop geben bis zum Ende der Liste