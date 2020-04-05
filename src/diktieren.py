#############################################################
# Ähnlich wie das MAIL modul, nur dass hier ein TExt-Editor #
# geöffnet wird. Um einzustellen welcher es sein soll, kann #
# die variable TEXT_EDITOR abgeändert werden.               #
#############################################################

import os
import tempfile

TEXT_EDITOR = 'pluma'

WORDS = ['diktier', 'text']

def isValid(text):
    text = text.lower().strip()
    if ('text' in text and 'diktier' in text):
        return True
    return False


def handle(text, tiane, profile):
    tiane.say('Dann leg mal los.')
    body = []
    text = tiane.listen().strip()
    while (text.lower() != 'stop' and text.lower() != 'stopp' and text.lower() != 'fertig'):
        if text != '' and text != 'TIMEOUT_OR_INVALID':
            body.append(text)
        text = tiane.listen().strip()
    tiane.end_Conversation()
    try:
        file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        for line in body:
            file.write(line + '\n')
        file.close()
        os.system(TEXT_EDITOR + ' "' + file.name + '"')
    except IOError:
        tiane.say('Es ist ein Fehler aufgetreten.')
