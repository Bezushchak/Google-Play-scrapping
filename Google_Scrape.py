# First of all making sure that the parsed url is not blocked in the robots.txt
# You may get acquainted with the link: https://play.google.com/robots.txt
from bs4 import BeautifulSoup as bs
import html
import requests

my_url = "https://play.google.com/store/apps/category/GAME"


def get_categories():
    response = requests.get(my_url)
    soup = bs(response.text, 'html.parser')
    for a in soup.find_all('h2'):
        yield [a.get_text(), a.parent.get('href')]


def get_categories_with_game():
    for categ in get_categories():
        response = requests.get('https://play.google.com' + categ[1])
        soup = bs(response.text, 'html.parser')
        for a in soup.find_all('div', {"class": "WsMG1c"}):
            yield [categ[0], a.get_text()]


def main():
    for category, game in get_categories_with_game():
        print('APP/CATEGORY-GAMES/' + category + '/' + game)

# Problem 1. Simply printing the scraped data on the screen
main()

# Problem 2. Getting the data in the csv format to display on the server
import pandas as pd

dispcateg = []
dispgame = []
for category, game in get_categories_with_game():
    try:
        dispcateg.append(category)
        dispgame.append(game)
    except:
        dispcateg.append('NA')
        dispgame.append('NA')

result_final = pd.DataFrame(
     {
      'category': dispcateg,
      'app_name': dispgame,
     }
)

result_final.to_csv('bezushchak.csv')
