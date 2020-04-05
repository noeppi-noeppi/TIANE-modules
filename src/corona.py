###################################################
# Hiermit kann TIANE die Corona-Daten bis gestern #
# für verschiedene Länder vorlesen.               #
###################################################

from urllib.request import urlopen, Request
import json
import datetime

def isValid(text):
    text = text.lower().strip()
    if ('corona' in text or 'covid-19' in text) and ('info' in text or 'daten' in text):
        return True
    return False


def handle(txt, tiane, profile):
    day_map = {
        1: 'ersten',
        2: 'zweiten',
        3: 'dritten',
        4: 'vierten',
        5: 'fünften',
        6: 'sechsten',
        7: 'siebten',
        8: 'achten',
        9: 'neunten',
        10: 'zehnetn',
        11: 'elften',
        12: 'zwölften',
        13: 'dreizehnten',
        14: 'vierzehnten',
        15: 'fünfzehnten',
        16: 'sechzehnten',
        17: 'siebzehnten',
        18: 'achtzehnten',
        19: 'neunzehnten',
        20: 'zwanzigsten',
        21: 'einundzwanzigsten',
        22: 'zweiundzwanzigsten',
        23: 'dreiundzwanzigsten',
        24: 'vierundzwanzigsten',
        25: 'fünfundzwanzigsten',
        26: 'sechsundzwanzigsten',
        27: 'siebenundzwanzigsten',
        28: 'achtundzwanzigsten',
        29: 'neunundzwanzigsten',
        30: 'dreißigsten',
        31: 'einunddreißigsten'
    }

    month_map = {
        1: 'Januar',
        2: 'Februar',
        3: 'März',
        4: 'April',
        5: 'Mai',
        6: 'Juni',
        7: 'Juli',
        8: 'August',
        9: 'September',
        10: 'Oktober',
        11: 'November',
        12: 'Dezember'
    }

    countryMap = {
        'Deutschland': 'Germany',
        'China': 'China',
        'Italien': 'Italy',
        'Frankreich': 'France',
        'Spanien': 'Spain',
        'Iran': 'Iran',
        'Türkei': 'Turkey',
        'Schweiz': 'Switzerland',
        'Belgien': 'Belgium',
        'Niederlande': 'Netherlands',
        'Kanada': 'Canada',
        'Österreich': 'Austria',
        'Südkorea': 'Korea, South',
        'Portugal': 'Portugal',
        'Brasilien': 'Brazil',
        'Israel': 'Israel',
        'Schweden': 'Sweden',
        'Australien': 'Australia',
        'Norwegen': 'Norway',
        'Russland': 'Russia',
        'Irland': 'Ireland',
        'Tschechien': 'Czechia',
        'Dänemark': 'Denmark',
        'Chile': 'Chile',
        'Polen': 'Poland',
        'Indien': 'India',
        'Luxemburg': 'Luxembourg',
        'Thailand': 'Thailand',
        'Saudi Arabien': 'Saudi Arabia',
        'Indonesien': 'Indonesia',
        'Finnland': 'Finland',
        'Mexiko': 'Mexico',
        'Griechenland': 'Greece',
        'Südafrika': 'South Africa',
        'Serbien': 'Serbia',
        'Singapur': 'Singapore',
        'Ukraine': 'Ukraine',
        'Kroatien': 'Croatia',
        'Ägypten': 'Egypt',
        'Neuseeland': 'New Zealand'
    }

    text = txt.lower()

    countryCode = 'Germany'
    countryName = 'Deutschland'

    if 'vereinigt' in text and 'königreich' in text:
        countryCode = 'United Kingdom'
        countryName = 'England'

    if 'usa' in text or ('vereinigt' in text and 'staat' in text):
        countryCode = 'US'
        countryName = 'den Vereinigten Staaten'

    for key in countryMap:
        if key.lower() in text:
            countryCode = countryMap[key]
            countryName = key

    try:
        request = Request('https://pomber.github.io/covid19/timeseries.json')
        response = urlopen(request)
        answer = json.loads(response.read())

        now = datetime.datetime.now()
        latest = None
        if tiane.analysis['time'] is None:
            latest = answer[countryCode][-1]
        elif int(tiane.analysis['time']['year']) == now.year and int(tiane.analysis['time']['month']) == now.month and int(tiane.analysis['time']['day']) == now.day:
            latest = answer[countryCode][-1]
        else:
            for possible in answer[countryCode]:
                possible_date_tokens = possible['date'].split('-', 2)
                if int(tiane.analysis['time']['year']) == int(possible_date_tokens[0]) and int(tiane.analysis['time']['month']) == int(possible_date_tokens[1]) and int(tiane.analysis['time']['day']) == int(possible_date_tokens[2]):
                    latest = possible

        if latest is None:
            tiane.say('Für diese Zeit kann ich keine Daten finden. Hier die aktuellen.')
            latest = answer[countryCode][-1]

        date_tokens = latest['date'].split('-', 2)
        return_string = 'Am {} {} {} gab es in {} {} Infizierte, {} Todesfälle und {} wieder Gesunde.'\
            .format(day_map[int(date_tokens[2])], month_map[int(date_tokens[1])], date_tokens[0], countryName, str(latest['confirmed']), str(latest['deaths']), str(latest['recovered']))
        tiane.say(return_string)
    except SyntaxError:
        tiane.say('Momentan kann ich leider keine daten finden.')