import openpyxl
import os

column = {
    "expert": "A",
    "affiliation": "B",
    "interests": "C",
    "email": "D",
    "phone": "E",
    "address": "F",
    "country": "G",
    "language": "H",
    "position": "I",
}


def choose_language(counrty):
    dict_language = {
        'Russia': 'Russian',
        'Turkey': 'Turkish',
        'Lithuania': 'Lithuanian',
        'Poland': 'Polish',
        'United States of America': 'English',
        'United Kingdom': 'English',
        'Japan': 'Japanese',
        'Republic of Ireland': 'Irish/English',
        'South Africa': 'Afrikaans/English',
        'India': 'Hindi/English',
        'Switzerland': 'French',
        'New Zealand': 'English',
        'Australia': 'Mandarin',
        'Spain': 'Spanish',
        'Austria': 'German',
        'Singapore': 'English/Standard Mandarin',
        'France': 'French',
        'Germany': 'German',
        'Finland': 'Finnish',
        'Israel': 'Hebrew',
        'Mozambique': 'Portuguese',
        'Portugal': 'Portuguese',
        'Iran': 'Persian',
        'Italy': 'Italian',
        'Canada': 'French/English',
        'Netherlands': 'Dutch/English',
        'Malaysia': 'Malay',
        'Norway': 'Norwegian',
        'Brazil': 'Portuguese',
        'Hong Kong': 'Chinese/English',
        'China': 'Standard Mandarin',
        'South Korea': 'Korean',
        'Greece': 'Greek',
        'Taiwan': 'Mandarin Chinese',
        'Croatia': 'Croatian',
        'Cyprus': 'Turkish/Greek',
        'Denmark': 'Danish',
        'West Germany': 'Frisian/Saterland Frisian',
        'Luxembourg': 'French',
        'Belgium': 'French',
        'Colombia': 'Spanish',
        'Sweden': 'Swedish',
        'Thailand': 'Thai',
        'Hungary': 'Hungarian',
        'Pakistan': 'Urdu/English',
        'Philippines': 'English/Filipino',
        'Estonia': 'Estonian',
        'Slovenia': 'Slovenian',
    }

    return dict_language.setdefault(counrty, '')


if __name__ == '__main__':
    path_worksheet = os.path.join(os.getcwd(), 'result.xlsx')
    wb = openpyxl.load_workbook(path_worksheet)
    st = wb.active
    for i in range(2, 5664):
        st[column["language"] + str(i)] = choose_language(st[column['country'] + str(i)].value)

    wb.save(path_worksheet)
