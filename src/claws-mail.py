#############################################################
# Diese Modul lässt TIANE mails vorschreiben und öffnet     #
# diese dann in 'claws-mail'. Dazu muss 'claws-mail'        #
# installiert sein. Zu mAufrufen nutze 'TIANE mail Betreff' #
# wobei Betreff durch den Betreff der Mail ersetzt werden   #
# soll. Dann die Mail diktieren und zum Schluss nur das     #
# Wort 'fertig' sagen.                                      #
#############################################################

import os
import tempfile

WORDS = ['mail', 'e-mail']

def isValid(text):
    text = text.lower().strip()
    if text.startswith('mail ') or text.lower().startswith('e-mail ') or text.lower().startswith('email ') or text.lower().startswith('e mail '):
        return True
    return False


def handle(text, tiane, profile):
    text = text.strip()
    if text.lower().startswith("mail ") or text.lower().startswith('e-mail ') or text.lower().startswith('email ') or text.lower().startswith('e mail '):
        subject = text[5:]
        tiane.say('Vertrau mir deine Mail an. Zum Beenden nutze das Wort fertig.')
        body = []
        text = tiane.listen().strip()
        while (text.lower() != 'stop' and text.lower() != 'stopp' and text.lower() != 'fertig'):
            if text != '' and text != 'TIMEOUT_OR_INVALID':
                body.append(text)
            text = tiane.listen().strip()
        tiane.end_Conversation()
        try:
            file = tempfile.NamedTemporaryFile(mode='w', delete=False)
            file.write('To: \n')
            file.write('Subject: ' + subject + '\n\n')
            for line in body:
                file.write(line + '\n\n')
            file.close()
            os.system('claws-mail --compose-from-file "' + file.name + '"')
        except IOError:
            tiane.say('Es ist ein Fehler aufgetreten.')
