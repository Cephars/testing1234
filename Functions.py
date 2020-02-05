import sys, re
from random import randint


# A GUESSER FUNCTION.
def guesser():
    num1 = int(sys.argv[1])
    num2 = int(sys.argv[2])
    print(f'Helloo, Welcome to Guess_World!')
    while True:
        try:

            guess = int(input("Please input your guess: "))
            comp = randint(num1, num2)
            print(f'Random Value: {comp}')
            if guess == comp:
                break
            print('Wrong guess!')
        except ValueError:
            print('Please input a valid number.')

    return 'Nice'


#A PASSWORD CHECKER FUNCTION

def validate_pin(pin):


    pat = '[.?\-",_:;(){}*+ ]'
    pat2 = '[a-zA-Z]'
    if pin[-1] == " ":
        return False
    elif (len(pin) == 6 or len(pin) == 4) and (not re.search(pat, pin) and not re.search(pat2, pin)):
        return True
    else:
        return False


def jpg_to_png_converter():
    import os, sys
    from PIL import Image

    first = sys.argv[1]
    second = sys.argv[2]

    if not os.path.exists(second):
        os.makedirs(second)

    for filename in os.listdir(first):
        if filename.endswith('jpg'):
            img = Image.open(f'{first}\\{filename}')
            clean = os.path.splitext(filename)[0]
            img.save(f'{second}\\{clean}.png')


def pdf_converter(pdfs):
    import PyPDF2
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write('super.pdf')


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def list_sorter(hn_list):
    return sorted(hn_list, key=lambda k: k['Votes'], reverse=True)


def hn_news_scrapper():
    import requests, pprint
    from bs4 import BeautifulSoup


    hn_list = []
    for num in range(1, 2):
        url = requests.get(f'https://news.ycombinator.com/news?p={num}')
        soup = BeautifulSoup(url.text, 'html.parser')
        header = soup.select('.storylink')
        score = soup.select('.subtext')
        author = soup.select('.hnuser')

        for i, j in enumerate(header):
            text = j.getText()
            link = j.get('href')
            votes = score[i].select('.score')
            user = author[i].getText()
            if len(votes):
                point = int(votes[0].getText().strip(' points'))
                if point > 100:

                    hn_list.append({'Header': text, 'Link': link, 'Votes': point, 'Author': user})

        return list_sorter(hn_list)


def email_sender():
    import smtplib, getpass, ssl
    from email.message import EmailMessage
    from getpass import getpass

    context = ssl.create_default_context()
    email = EmailMessage()
    email['to'] = input('Receiver\'s Email: ')
    email['subject'] = input('Email Subject: ')
    email.set_content(f'{hn_news_scrapper()}')
    email['from'] = input('Sender\'s Name to Display: ')
    sender = input('Sender\'s Address: ')
    password = getpass('Sender\'s Password: ')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.login(sender, password)
        smtp.send_message(email)
        print('Good Job!')


def b(text):
    for ch in [' ', ':',',', '(','#']:
        if ch in text:
            text = text.replace(ch, '-')
    for ch2 in [')',"'"]:
        if ch2 in text:
            text = text.replace(ch2,'')
    return text.lower()


def book_scraper():
    import requests, pandas as pd
    from bs4 import BeautifulSoup
    title = []
    rating = []
    cost = []

    for num in range(1, 51):
        url = requests.get(f'http://books.toscrape.com/catalogue/page-{num}.html')
        soup = BeautifulSoup(url.text, 'html.parser')

        for t, r, c in zip(soup.select('.image_container >a>img'), soup.select('p.star-rating'),
                           soup.select('p.price_color')):
            title.append(t['alt'])
            rating.append(r.attrs['class'][-1])
            cost.append(c.getText()[1:])

    novels = pd.DataFrame({"Title": title, "Price": cost, "Rating":rating})
    return novels