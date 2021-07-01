# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from model import words, classes, ignore_words
from model import clean_up_sentence

# import our chat-bot's intents file
import json
with open('intents.json') as json_data:
    intents = json.load(json_data)

# define variables
xp_words = words
question_word = []
xp_classes = classes
xp_documents = []

question = "kann ich mit freunden draussen sitzen?"

# function to tokenize the question
def tokenizeInput(question):
    global question_word
    w = nltk.word_tokenize(question)
    # add w to our "simple" words list; this is the question in the form of a list
    question_word.extend(w)
    # stem question words
    question_word = [stemmer.stem(w.lower()) for w in question_word if w not in ignore_words]
    question_word = sorted(list(set(question_word)))
    # remove duplicates
    # question_classes = sorted(list(set(question_classes)))

# or just use...
# question_classes = clean_up_sentence(question)

# or: adapt previous class (from model.py) to create the desired array / list structure, starting line 28
# is ['intents'] just a row name? :o

# convert results into a list of lists. the super list contains the lists, the sublists have the following dimensions:
# [n][0][#]: key words
# [n][1][0]: response
# [n][2][0,1]: absolute and relative score
# [n][3][0,1,2]: absolute, relative and combined rank


# sort lists so they contain the tag, keywords and response in one row respectively...
# response class uses a LIST, structure can be inferred by looking at that class...

# compare the lists
# generate two sets of rankings

# more sophisticated approach:
# https://stackoverflow.com/questions/8897593/how-to-compute-the-similarity-between-two-text-documents


# step 1: tokenize and stem json word lists
#   => this is already done; however, the format is not exactly what we need

# step 2: convert this into a list of lists
# okay, maybe...
# HIER MUSS MAN DAS IRGENDWIE SO HINKRIEGEN DASS ER IN JEDER ZEILE EINEN NEUEN TAG HAT
# also: erste spalte die schlüsselwörter, zweite spalte die antwort. ersteres eine liste, zweiteres ein string
# dritte spalte dann anzahl übereinstimmungen absolut, vierte spalte relativ, fünfte rang absolut, sechste rang relativ, siebte rang gemischt
# neue zeile = neues intent
xp_list = []

# https://blog.finxter.com/wp-content/uploads/2020/04/listoflist-768x432.jpg
# liste 1: 7 einträge
# spalte 1: list of lists (als inhalt)
# list of lists hat: wortliste 1, wortliste 2, wortliste 3...
# die wortlisten haben jeweils variable längen
# spalten 2 - 7: arrays mit jeweils einem eintrag pro spalte (item 1, 2, 3...)
# eintrag NUMMER eins der spalte gehört zu wortliste 1, eintrag nummer zwei zu wortliste zwei...

# hier machen die das mit dictionaries: https://online.datasciencedojo.com/blogs/building-a-rule-based-chatbot-in-python
# cosine match: https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/

xp_liste = [[]],[],[],[],[],[],[]
append to xp_liste[0]
# => neue liste dranhängen? geht das mit append? dass er erkennt welcher elementtyp (bei position 0: liste) erwartet wird?
# append oder insert into?
# jedenfalls dann auch bei position 2 - 7 mit append? dass er jeweils ein neues item generieren würde??

# siehe https://blog.finxter.com/python-list-of-lists/

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        # add to our words list
        xp_words.extend(w)

        # mein codeversuch...
        xp_list.insert(0, [w])

        # add to documents in our corpus
        xp_documents.append((w, intent['tag']))
        # add to our classes list (unless it already exists)
        if intent['tag'] not in xp_classes:
            xp_classes.append(intent['tag'])

# stem and lower each word and remove duplicates
xp_words = [stemmer.stem(w.lower()) for w in xp_words if w not in ignore_words]
xp_words = sorted(list(set(words)))

# xp_words = [][[]][]
# xp_words[n][0] = intent['tag']
# xp_words[n][1] = [tagliste]
# xp_words[n][2] = intent['reply']

# step 3: tokenize and stem the input question
# step 4: convert this into a list
# step 5: compare the sublists with the question list
# step 6: quantify the match
# step 7: return the N for the best match
# step 8: return the replied tied to this N