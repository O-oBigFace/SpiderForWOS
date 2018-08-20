import os

column = {
    "expert": "A",
    "affiliation": "B",
    "interests": "C",
    "email": "D",
    "name": "E",
    "citedby": "F",
    "hindex": "G",
    "hindex5y": "H",
    "i10index": "I",
    "i10index5y": "J",
    "url_picture": "K",
    "phone": "L",
    "address": "M",
    "country": "N",
    "language": "O",
    "position": "P",
}

if __name__ == '__main__':
    print(os.path.abspath(os.path.join(os.getcwd(), '..')))