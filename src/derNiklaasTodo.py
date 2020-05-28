#############################################################
# Dieses Modul erlaubt die Sprachsteuerung der TO-DO-Liste  #
# von `derNiklaas` via TIANE. Die TO-DO-Liste gibt es hier: #
# https://github.com/derNiklaas/TODO-List                   #
#############################################################

from urllib.request import urlopen, Request
from urllib.parse import quote
import re

PRIORITY = 1
PORT = 9999

patternChange = re.compile(r'^setze? (den (ersten|zweiten|dritten|vieren|1\.|2\.|3\|4\.) Eintrag auf|Eintrag (eins|zwei|drei|vier|1|2|3|4) auf) (.*)$', re.I)
patternToggle = re.compile(r'^(schalte den (ersten|zweiten|dritten|vieren|1\.|2\.|3\|4\.) Eintrag um|schalte Eintrag (eins|zwei|drei|vier|1|2|3|4) um|ich habe den (ersten|zweiten|dritten|vieren|1\.|2\.|3\|4\.) Eintrag( nicht)? erledigt|ich habe Eintrag (eins|zwei|drei|vier|1|2|3|4)( nicht)? erledigt).*?$', re.I)
patternShow = re.compile(r'^zeige? (mir)? die (TODO|TO-DO|TO DO)[-? ]Liste.*?$', re.I)
patternHide = re.compile(r'^(lasse? die (TODO|TO-DO|TO DO)[-? ]Liste verschwinden|Verstecke? die (TODO|TO-DO|TO DO)[-? ]Liste).*?$', re.I)

def isValid(text):
    text = text.lower().strip()
    return patternChange.match(text) is not None or patternToggle.match(text) is not None \
           or patternShow.match(text) is not None or patternHide.match(text) is not None

def handle(txt, tiane, profile):
    text = txt.lower().strip()
    numberMap = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '1.': 1,
        '2.': 2,
        '3.': 3,
        '4.': 4,
        'eins': 1,
        'zwei': 2,
        'drei': 3,
        'vier': 4,
        'ersten': 1,
        'zweiten': 2,
        'dritten': 3,
        'vierten': 4
    }
    match = patternChange.match(text)
    if match is not None:
        numInput = match.group(2)
        if numInput is None:
            numInput = match.group(3)
        num = numberMap[numInput]
        if num is 1:
            numStr = 'settaskOne'
        elif num is 2:
            numStr = 'settaskTwo'
        elif num is 3:
            numStr = 'settaskThree'
        else:
            numStr = 'settaskFour'

        print(match.group(3))
        print(type(match.group(3)))

        urlopen(Request('http://localhost:9999/send?function=' + numStr + '-' + quote(match.group(4))))
        return
    match = patternToggle.match(text)
    if match is not None:
        numInput = match.group(2)
        if numInput is None:
            numInput = match.group(3)
        if numInput is None:
            numInput = match.group(4)
        if numInput is None:
            numInput = match.group(6)
        num = numberMap[numInput]
        if num is 1:
            numStr = 'toggleTaskOne'
        elif num is 2:
            numStr = 'toggleTaskTwo'
        elif num is 3:
            numStr = 'toggleTaskThree'
        else:
            numStr = 'toggleTaskFour'
        urlopen(Request('http://localhost:9999/send?function=' + numStr))
        return
    match = patternShow.match(text)
    if match is not None:
        urlopen(Request('http://localhost:9999/send?function=show'))
        return
    match = patternHide.match(text)
    if match is not None:
        urlopen(Request('http://localhost:9999/send?function=hide'))
        return
    tiane.say('Das kann ich noch nicht. Da must du deine To-Do-Liste selbst bearbeiten.')

