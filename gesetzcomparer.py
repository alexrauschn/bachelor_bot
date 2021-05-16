import requests
import re
from bs4 import BeautifulSoup


def write_gastbewerbetext_to_file(filename, url):
    start = '<h2 class="UeberschrPara AlignCenter">Gastgewerbe</h2>'
    end = '<h2'

    s = requests.get(url).text
    #only get relevant part of text
    gastgewerbe_absatz = BeautifulSoup(((s.split(start))[1].split(end)[0]), 'lxml')

    f = open(filename, "w+", encoding="utf-8")
    f.write(gastgewerbe_absatz.text)
    f.close()


# 1. local txt laden
# 2. url text laden
# 3. comparen
# 4. rückgabe 1 oder 0


def get_current_url():
    start = '<h2 id="-span-aktuelles-span-span-span-"><span>Aktuelles: </span><span></span></h2>'
    end = '<ul>'
    original_url = 'https://www.sozialministerium.at/Informationen-zum-Coronavirus/Coronavirus---Rechtliches.html'
    s = requests.get(original_url).text
    # print(s)
    long_string = ((s.split(start))[1].split(end)[0])

   # start = 'Ausgegeben am '
   # end = '</p>'
    #date_original = ((s.split(start))[1].split(end)[0])

    # get link itself
    start = 'href=\"'
    end = '.html'
    short_string = ((long_string.split(start))[1].split(end)[0])
    return short_string + ".html"

def compare_files(oldFilename, newFilename):
    oldfFile = open(oldFilename, "r", encoding="utf-8")
    newFile = open(newFilename, "r", encoding="utf-8")
    return oldfFile.read() == newFile.read()

def are_local_files_up_to_date():
    newGewerbeTextFilename = "newText.txt"
    oldGewerbeTextFileName = "currentText.txt"
    oldGewerbeTexthtml = "currentText.html"
    write_gastbewerbetext_to_file(newGewerbeTextFilename, get_current_url())
    write_gastbewerbetext_to_file(oldGewerbeTextFileName, get_current_url())

    if(compare_files(oldGewerbeTextFileName, newGewerbeTextFilename)):
        print("same")
    else:
        print("they're different")

are_local_files_up_to_date()
#are_local_files_up_to_date()

