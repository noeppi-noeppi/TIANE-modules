#######################################################################
# Lässt TIANE Programme auf dem server ausführen. Dazu muss eine      #
# Konfigurationsdatei angelegt werden. (Im gleichen Verzeichnis,      #
# wo auch dieses Modul liegt). Diese muss 'programmstart.cfg'         #
# heißen. Sie sieht folgendermaßen aus: (Beispiel)                    #
#                                                                     #
# browser:firefox                                                     #
# terminal:xterm                                                      #
#                                                                     #
# github:firefox "https://github.com/"                                #
# wikipedia:firefox "https://wikipedia.org/"                          #
#                                                                     #
# google:firefox "https://www.startpage.com/do/dsearch?query={}"      #
#                                                                     #
# Vor dem Doppelpunkt steht der aufrufbare Name, dahinter der Befehl. #
# Programme im ersten Block werden mit dem wort 'starte' gestartet,   #
# Programme im zweiten Block mit 'öffne'. Beim Spezialfall 'google'   #
# Wird {} mit der Nachfolgenden Suche ersetzt. (ALs URL encoded).     #
# Deshalb kann man dann z.B. 'TIANE google Wie lerne ich Python'      #
# sagen und es würde gegooglet. (Bzw mit startpage gesucht in diesem  #
# Fall.                                                               #
#######################################################################

import os
from os.path import expanduser
import inspect
import urllib.parse

commandDictStart = {}
commandDictOpen = {}
specialGoogle = ''

PRIORITY = 12

if (os.path.exists(os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)),
                                'programmstart.cfg'))):
    print("Parsing programs")
    with open(os.path.join(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)),
                           'programmstart.cfg')) as f:
        opens = False
        for rline in f:
            line = rline.strip().split('#', 1)[0].strip()
            if (line == ''):
                opens = True
            else:
                d = line.split(':', 1)
                if (d[0].lower() == 'google'):
                    specialGoogle = d[1]
                elif (opens):
                    commandDictOpen[d[0].lower()] = d[1]
                else:
                    commandDictStart[d[0].lower()] = d[1]
        print("Found {} programs for key start".format(len(commandDictStart)))
        print("Found {} programs for key open".format(len(commandDictOpen)))
else:
    print("File programmstart.cfg not found.")

WORDS = ['starte', 'öffne', 'google'] + list(commandDictStart.keys()) + list(commandDictOpen.keys())
CD_COMMAND = 'cd {};'.format(expanduser('~'))

def isValid(text):
    text = text.lower()
    if ("starte" in text):
        for key in commandDictStart:
            if (key.lower() in text):
                return True
    elif ("öffne" in text):
        for key in commandDictOpen:
            if (key.lower() in text):
                return True
    elif (text.startswith("google") and specialGoogle != ''):
        return True
    return False


def handle(text, tiane, profile):
    text = text.lower()
    if (text.startswith("google ") and specialGoogle != ''):
        os.system(CD_COMMAND + specialGoogle.format(urllib.parse.quote(text[7:])) + ' &')
        tiane.say('Ich habe Google geöffnet')
        return
    for key in commandDictStart:
        if (key.lower() in text):
            os.system(CD_COMMAND + commandDictStart[key] + ' &')
            tiane.say('Ich habe {} gestartet'.format(key))
            return
    for key in commandDictOpen:
        if (key.lower() in text):
            os.system(CD_COMMAND + commandDictOpen[key] + ' &')
            tiane.say('Ich habe {} geöffnet'.format(key))
            return
    tiane.say('Ich konnte dieses Programm nicht finden.')
