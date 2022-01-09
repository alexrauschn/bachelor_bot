# BAREBONES CHATBOT
# intents:
# row 0 = first intent, row 1 = second intent...
# position 0 = score, position 1 = score moderated by number of patterns, pos 2 = ranking by score,
# pos 3 = ranking by moderated score, pos 4 = mixed ranking (used for output)
# pos 5 = category name, pos 6 = answer, pos 7 - XXX = patterns
arrayIntents = [
[0.0, 0.0, 99.0, 99.0, 99.0, "gastgewerbe_indoor", "Ein Tisch darf aus maximal vier Personen zuzueglich bis zu 6 minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt leben.", "indoor", " geschlossene", "Raeume", "geschlossener", "Raum", "drinnen", "Inneren", "innen", "sitzen", "essen", "Tisch"],
[0.0, 0.0, 99.0, 99.0, 99.0, "gastgewerbe_outdoor", "Ein Tisch darf aus maximal zehn Personen zuzueglich bis zu zehn minderjaehrigen Kindern bestehen, wenn diese Personen nicht in einem gemeinsamen Haushalt lebt.", "outdoor", "out-door", "Biergarten", "draussen", "Freien", "frischen", "Luft ", "ausserhalb", "sitzen", "essen", "Tisch"],
[0.0, 0.0, 99.0, 99.0, 99.0, "gemeinsamer_haushalt", "Fuer Personen die in einem Haushalt leben gelten die Beschraenkungen auf eine Personenzahl nicht.", "gemeinsamer", "ein", "Haushalt", "zusammen", "gemeinsam", "leben", "ein Haushalt", "zusammen", "Wohnen", "zusammenwohnen"],
[0.0, 0.0, 99.0, 99.0, 99.0, "test_pcr", "Mit einem negativen PCR-Test darf man innerhalb von 72 Stunden ein Gastgewerbe betreten.", "PCR-Test", " molekularbiologischer Test", "Gueltigkeit", "gueltig", "Wielange", "lange", "Laenge", "Gurgeltest", "PCR-Gurgeltest", "Gueltigkeitsdauer", " Zutrittstest", "Zutrittstests"],
[0.0, 0.0, 99.0, 99.0, 99.0, "berechtigung", "Der Kunde muss einen den Nachweis einer geringen epidemiologischen Gefahr erbringen, dh. Sie muessen getestet, genesen oder geimpft sein.", "Berechtigung", " notwendig", "noetig", "braucht", "brauche", "betreten", "Nachweisen", "Zutritt", "Wann", "wann", "hinein", "darf", "duerfen", "Gasthaus", "Restaurant", "Cafe"],
[0.0, 0.0, 99.0, 99.0, 99.0, "test_antigen", "Mit einem negativem Antigentest einer Befugten stelle darf man innerhalb von 48 Stunden ein Gastgewerbe betreten)", "Antigentest", "befugte", "Stelle", "Teststelle", "Gueltigkeit", "Wielange", "lange", "Testcenter", "Test-Center", "Teststrasse", "Gueltigkeitsdauer"],
[0.0, 0.0, 99.0, 99.0, 99.0, "test_selbst", "Mit einem behoerdlich erfassten negativen Selbsttest darf man 24 Stunden ein Gastgewerbe betreten", "Selbsttest", " Antigentest", "Gueltigkeit", "lange", "behoerdliche", "Datenverarbeitung", "registrierter", "Test", "Selbsttest", "Gueltigkeitsdauer"],
[0.0, 0.0, 99.0, 99.0, 99.0, "test_betreiber", "Sollte kein Test vorliegen kann ausnahmsweise ein Selbsttest unter Aufsicht des Betreibers durchgefuehrt werden, der fuer die Dauer des Aufenthalts gueltig ist", "Kein", "Test", "ohne", "vor", "Ort", "Selbsttest", "im", "Betrieb", "durch", "Betreiber", "von"],
[0.0, 0.0, 99.0, 99.0, 99.0, "maske", "In geschlossenen Raeumen besteht die Pflicht zum Tragen einer FFP2-Maske, ausser am Tisch (Verabreichungsplatz)", "Maskenpflicht", "Maske", "Masken", "tragen", " FFP2-Maske", "aufhaben", "anhaben"],
[0.0, 0.0, 99.0, 99.0, 99.0, "genesen", "Eine ueberstandene Erkrankung an COVID-19 berechtigt zum Betreten eines Gastgewerbes, wenn diese nicht mehr als 6 Monate zurueck liegt und aerztlich oder durch einen Absonderungsbescheid bestaetigt ist, oder ein Nachweis ueber neutralisierte Antikoerper der nicht aelter als 3 Monate ist.", "Absonderungsbescheid", "aerztliche", "Bestaetigung", "Attest", "aerztliches", "Infektion", "ueberstanden", "genesen", "erkrankt", "Antikoerper", "Nachweis", "Erkrankung"],
[0.0, 0.0, 99.0, 99.0, 99.0, "abstand", "Zwischen Personen die nicht im selben Haushalt leben oder zu einer Besuchergruppe gehoeren muss ein Abstand von min. zwei Metern eingehalten werden. Der gleiche Abstand muss zwischen den Tischen verschiedener Besuchsgruppen bestehen.", "Abstand", "wieweit", "weg", "Entfernung", "Abstaende", "entfernt", "einhalten", "einzuhalten", "nahe", "Naehe"],
[0.0, 0.0, 99.0, 99.0, 99.0, "oeffnungszeit", "Falls keine anderen strengeren Beschraenkungen gelten duerfen zwischen 05:00 und 22:00 Kunden den Gastbetrieb betreten. Zwischen 22.00 und 05:00 ist auch das Abholen nur Lieferservices erlaubt.", "Oeffnungszeiten", "Oeffnungszeit", "offenhaben", "offen", "wielange", "geoeffnet ", "aufsperren", "Sperrstunde", "zusperren", "Abholung", "abholen", "Lieferservice", "Lieferdienst"],
[0.0, 0.0, 99.0, 99.0, 99.0, "essen", "Speisen und Getraenke duerfen grundsaetzlich nur im Sitzen konsumiert werden und es muss genuegend Abstand zu Ausgabestellen bestehen. Nur bei Imbiss- und Gastronomiestaende darf auch im Stehen konsumiert werden.", "Regeln", "Essen", "Vorschriften", "Speisen", "Getraenke", "Getraenk", "konsumieren", "konsumiert", "Konsum", "trinken", "essen", "gegessen", "wie", "sitzen", "sitzend", "stehend", "Tisch", "wo", "getrunken", "stehen", "Bar", "Tisch"],
[0.0, 0.0, 99.0, 99.0, 99.0, "impfung_", "Ab 22. Tag nach der Erstimpfung mit einem zweiteiligen Impfstoff berechtigt diese einen fuer 3 Monaten ab der ersten Impfung zum Zutritt zu einer Gaststaette, mit der Zweitimpfung fuer 9 Monate. Eine einteilige Impfung berechtigt ab dem 22. Tag fuer 9 Monaete zum Zutritt.", "Erstimpfung", "wielange", "Zweitimpfung", "Gueltigkeit", "Impfung", "geimpft", "Zutritt", "Dosis", "Erstdosis"]
]

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