import time
from model import classify, response, numberOfEpochs, timeDifferenceBuilding
from bb import getRankedIntents

thesisMode = True

if thesisMode:
    questionToAsk = "Kann ich mit 5 Freunden draussen an einem Tisch im Biergarten sitzen?"
    answerExpected = "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."
else:
    print("\n----------\n")
    print("Note: Do not use umlauts or anything else of the like. ")
    questionToAsk = input("Please enter the question you want to ask: ")

firstRun = False

# NEURAL NETWORK MODEL

if firstRun:

    print("----------\n")
    timeBeforeAnswer = time.perf_counter() * 1000.0

    classified = classify(questionToAsk)
    if isinstance(classified, list):
        classed = str((classify(questionToAsk))[0][0])
        percNN = str(((classify(questionToAsk))[0][1])*100)
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
                        "\nThe categorization via NN was " + classed + " - NN correct: " + correctAnswer +
                        ". Percentage match: " + percNN +
                        ". It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model. "
                        + "The number of epochs was " + str(numberOfEpochs) + " (" + str(float(timeDifferenceBuilding)/float(numberOfEpochs))
                        + " ms per epoch). It took " + str(timeDifferenceAnswer) + " milliseconds to answer the question via the NN model.\nThe categorization via BB was "
                        + catBB + " - BB correct: " + correctBB + ". Percentage match: " + percBB +
                        ". It took " + str(timeDifferenceBarebones) + " milliseconds to structure the BB data and answer the question.\n"
                        + differentAns + corrOne + "\n---------------------\n")
    comparisonLog.close()

# antwort beider modelle noch printen lassen; iwas spinnt da noch

def answerLoop(questionToAsk, answerExpected):
    # neural network output
    print("Question asked: " + questionToAsk + "\n")

    print("-------Neural network output-------\n")
    timeBeforeAnswer = time.perf_counter() * 1000.0

    print("Classification according to the NN model / percentage match: ")
    classified = classify(questionToAsk)
    if isinstance(classified, list):
        if classified:
            classed = str((classify(questionToAsk))[0][0])
            percNN = str(((classify(questionToAsk))[0][1])*100)
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

    timeAfterAnswer = time.perf_counter() * 1000.0
    timeDifferenceAnswerFloat = (timeAfterAnswer - timeBeforeAnswer)
    timeDifferenceAnswer = "{:.2f}".format(timeDifferenceAnswerFloat)
    print("It took " + timeDifferenceBuilding + " milliseconds to train and build the NN model" + ".\n")
    print("The number of epochs was " + str(numberOfEpochs) + " (" + str(
        float(timeDifferenceBuilding) / float(numberOfEpochs)) + " ms per epoch).\n")
    print("It took " + timeDifferenceAnswer + " milliseconds to answer the question via the NN model.")

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

arrayQuestions = [

    # gastgewerbe outdoor
    ["Kann ich mit 5 Freunden draussen an einem Tisch im Biergarten sitzen?",
     "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],
    ["Darf man draussen mit Freunden an einem Tisch ohne Maske was gemeinsam essen?",
     "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],
    ["Ist es moeglich unter Freunden im Freien etwas zu trinken?",
     "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],
    ["Kann ich mit Freunden draussen was trinken oder ist das verboten?",
     "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],
    ["Ist es erlaubt unter Freunden im Freien was zu essen",
     "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt."],

    # gastegewerbe indoor
    ["Kann ich mit 5 Leuten im geschlossenen Raum sitzen und was trinken?",
     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],
    ["Ich will mit ein paar Freunden (anderer Haushalt) was drinnen essen, geht das?",
     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],
    ["Wie ist das drinnen kann ich da mit leuten was trinken oder nicht",
     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],
    ["Ist es erlaubt wenn man am Fenster sitzt zu siebt zu sein wenn man was trinkt?",
     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],
    ["Wir wollen nichts essen sondern nur was trinken, sind aber sieben Leute. Das waere drinnen. Geht das?",
     "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben."],

    # gemeinsamer haushalt
    ["Was ist wenn ich mit jemandem essen gehen will der ein Mitbewohner ist?",
     "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht."],
    ["Was ist wenn ich mit der Person gemeinsam lebe mit der ich mich treffen will?",
     "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht."],
    ["Was ist wenn die Person zusammen mit mir lebt und wir was trinken gehen wollen?",
     "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht."],
    ["Ich lebe sowieso mit meiner Partnerin zusammen, wie sehen die Regeln dann aus?",
     "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht."],
    ["Wenn man zusammen wohnt, gelten dann andere regeln?",
     "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht."],

    # berechtigung
    ["Was muss ich denn vorweisen koennen wenn ich fortgehen will",
     "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein."],
    ["Was wird als Nachweis benoetigt wenn ich in die Kneipe will?",
     "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein."],
    ["Wie ist das mit den Nachweisen, was brauche ich da?",
     "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein."],
    ["Was benoetige ich an Nachweisen wenn ich wo hingehen will?",
     "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein."],
    ["Wenn ich getestet und geimpft bin, reicht das dann zur Berechtigung?",
     "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein."],

    # test PCR
    ["Wie lange haelt ein Gurgeltest?",
     "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten."],
    ["Wie lange gilt ein PCR-Test?",
     "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten."],
    ["Wie lange gilt ein PCR-Selbsttest?",
     "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten."],
    ["Wie ist das mit den Tests von Allesgurgelt, wie lange zaehlen die?",
     "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten."],
    ["Wenn ich mich selber teste, was fuer Regeln gelten dann?",
     "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten."],

    # test antigen
    ["Was ist mit Nasenabstrichtests, wie lange gelten die?",
     "Mit einem negativem Antigentest einer befugten Stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten."],
["Wie lange gilt ein Schnelltest?",
 "Mit einem negativem Antigentest einer befugten Stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten."],
["Wie lange haelt ein Antigentest?",
 "Mit einem negativem Antigentest einer befugten Stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten."],
["Haelt ein Schnelltest fuer mehr als zwei Tage?",
 "Mit einem negativem Antigentest einer befugten Stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten."],
["Wie lange kann ich mit einem Test von einer Teststrasse was anfangen?",
 "Mit einem negativem Antigentest einer befugten Stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten."],

# Selbsttest
["Was ist wenn ich mit selber teste, wie lange gilt das?",
 "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten"],
["Wenn ich selbst einen Antigentest durchfuehre, wie lange gilt der dann?",
 "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten"],
["Wie lange gilt ein Selbsttest?",
 "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten"],
["Kann ich mit einem Selbsttest was trinken gehen?",
 "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten"],
["Ich habe mich selber getestet, erlaubt mir das jetzt in ein Gasthaus zu gehen?",
 "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten"],

# Betreiberdurchgeführter Test
["Kann ich mich nicht vor Ort in der Kneipe testen lassen?",
 "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist"],
["Was ist wenn ich keinen Test vorweisen kann?",
 "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist"],
["Ich bin aber ungetestet, was jetzt?",
 "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist"],
["Wenn ich ohne Teste komme muss ich dann gehen?",
 "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist"],
["Was ist wenn ich keinen Test habe, kann mich dann nicht einfach der Wirt testen?",
 "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist"],

# Maskenpflicht
["Wo muss ich ueberall Maske tragen?",
 "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)"],
["Wie ist das mit der Maskenpflicht?",
 "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)"],
["Reicht eine Maske aus Stoff?",
 "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)"],
["Ich kann mit diesen Masken nicht gescheit atmen, kann ich auch mit Faceshield in die Kneipe?",
 "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)"],
["Muss ich die Maske die ganze Zeit aufhaben oder wie ist das in der Kneipe? So kann ich doch nicht essen.",
 "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)"],

# genesen
["Ich bin genesen, kann ich jetzt in die Kneipe?",
 "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist."],
["Brauche ich ein Attest wenn ich genesen bin?",
 "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist."],
["Ich habe einen Nachweis dass ich schon mal Coronakrank war, ist das gleichwertig zur Impfung?",
 "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist."],
["Ich hatte Corona schon aber bin wieder gesund und habe auch einen Nachweise, kann ich was trinken gehen?",
 "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist."],
["Ich habe einen Antikoerpernachweis, zaehlt das als Impfung?",
 "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist."],

# Abstand
["Wie viel Abstand muss ich wahren?",
 "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen."],
["Wie viel Platz muss zwischen Personen sein?",
 "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen."],
["Wie viele Meter Abstand muessen eingehalten werden?",
 "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen."],
["Welche Entfernung ist zwischen Besuchern noetig?",
 "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen."],
["Gilt die Abstandsregel mit dem >Baby-Elefanten< auch im Wirtshaus?",
 "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen."],

# oeffnungszeit
["Wann kann ich in eine Kneipe gehen?",
 "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt."],
["Wann haben Restaurants geöffnet?",
 "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt."],
["Was sind die Oeffnungszeiten von Gastbetrieben?",
 "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt."],
["Wie lange hat denn jetzt alles ueberhaupt geoffnet?",
 "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt."],
["Um wieviel Uhr muessen die Laeden aktuell schliessen?",
 "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt."],

# essen
["Wie ist das mit dem Konsum von Speisen?",
 "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden."],
["Kann ich einfach im Stehen trinken oder muss ich sitzen?",
 "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden."],
["Was gilt wenn ich nicht sitzen will sondern beim Essen stehen will?",
 "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden."],
["Kann ich direkt an der Essensausgabe essen oder muss ich zum Tisch gehen?",
 "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden."],
["Kann ich an der Theke im Stehen essen?",
 "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden."],

# impfung
["Wie lange gilt eine Impfung?",
 "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt."],
["Wie bald nach der Impfung gelte ich als geimpft?",
 "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt."],
["Wie schnell nachdem ich die Spritze bekommen habe gelte ich als geimpft?",
 "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt."],
["Wieviele Tage nach der Impfung gelte ich denn als geimpft?",
 "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt."],
["Darf ich nach der ersten Impf-Dosis schon ohne Test in die Kneipe?",
 "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt."],

]

if thesisMode:
    for i in range(len(arrayQuestions)):
        questionToAsk = arrayQuestions[i][0]
        answerExpected = arrayQuestions[i][1]
        extraInfo = open('log_perf.txt', 'a')
        extraInfo.write("Iteration: " + str(i) + "\n")
        extraInfo.close()
        answerLoop(questionToAsk, answerExpected)