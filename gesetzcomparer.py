import requests
# import re
import filecmp
from bs4 import BeautifulSoup


# 1. local txt laden
# 2. url text laden
# 3. comparen
# 4. rückgabe 1 oder 0

# get the live file and write a local copy of the plain text
def write_gastbewerbetext_to_file(filename, url):
    start = '<h2 class="UeberschrPara AlignCenter">Gastgewerbe</h2>'
    end = '<h2'

    # get content of passed path / url
    if "http" in url:
        s = requests.get(url).text
    else:
        temp_s = open(url, "r", encoding="utf-8")
        s = temp_s.read()
        temp_s.close()

    # only get relevant part of text, including html tags
    gastgewerbe_absatz = BeautifulSoup(((s.split(start))[1].split(end)[0]), 'lxml')

    # write cropped part into file
    f = open(filename, "w+", encoding="utf-8")

    # only get the text, discard html tags
    f.write(gastgewerbe_absatz.text)
    f.close()

# get the current URL of the live file
def get_current_url():
    # get link area
    start = '<h2 id="-span-aktuelles-span-span-span-"><span>Aktuelles: </span><span></span></h2>'
    end = '<ul>'
    original_url = 'https://www.sozialministerium.at/Informationen-zum-Coronavirus/Coronavirus---Rechtliches.html'
    s = requests.get(original_url).text
    # print(s)
    long_string = ((s.split(start))[1].split(end)[0])
    #start = 'Ausgegeben am '
    #end = '</p>'
    #date_original = ((s.split(start))[1].split(end)[0])

    # get link itself
    start = 'href=\"'
    end = '.html'
    short_string = ((long_string.split(start))[1].split(end)[0])
    return short_string + ".html"

def compare_files(oldFilename, newFilename):
    check = filecmp.cmp(oldFilename, newFilename)
    return check

#   oldFile = open(oldFilename, "r", encoding="utf-8")
#   newFile = open(newFilename, "r", encoding="utf-8")
#   return oldFile.read() == newFile.read()



def are_local_files_up_to_date():
    newGewerbeTextFilename = "liveText.txt"
    oldGewerbeTextFileName = "localText.txt"
    oldGewerbeTexthtml = "local.html"
    write_gastbewerbetext_to_file(newGewerbeTextFilename, get_current_url())
    write_gastbewerbetext_to_file(oldGewerbeTextFileName, oldGewerbeTexthtml)

    if(compare_files(oldGewerbeTextFileName, newGewerbeTextFilename)):
        print("same")
    else:
        print("they're different")

are_local_files_up_to_date()

