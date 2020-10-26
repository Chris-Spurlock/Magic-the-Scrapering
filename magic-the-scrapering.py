"""
Under Construction
Next steps:
-Add commentary
-refactor/functionize code
-expand scrape to every card (currently first page of results)
-export results to csv
"""

# import libraries
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

# initialize lists to store card data
card_names = []
card_types = []
rules_texts = []
mana_costs = []
cmcs = []
power = []
toughness = []
colors = []

MANA_SYMBOLS = {
    'White': 'W', 'Blue': 'U', 'Black': 'B', 'Red': 'R', 'Green': 'G',
    'White or Blue': '(W/U)', 'Blue or Black': '(U/B)', 'Black or Red': '(B/R)', 'Red or Green': '(R/G)', 'Green or White': '(G/W)',
    'White or Black': '(W/B)', 'Blue or Red': '(U/R)', 'Black or Green': '(B/G)', 'Red or White': '(R/W)', 'Green or Blue': '(G/U)',
    'Two or White': '(2/W)', 'Two or Blue': '(2/U)', 'Two or Black': '(2/B)', 'Two or Red': '(2/R)', 'Two or Green': '(2/G)',
    'Phyrexian White': '(W/P)', 'Phyrexian Blue': '(U/P)', 'Phyrexian Black': '(B/P)', 'Phyrexian Red': '(R/P)', 'Phyrexian Green': '(G/P)',
    'Colorless': 'C',
    'Variable Colorless': 'X',
    'Snow': 'S',
    'Energy': 'E'
    }

for page in range(212): # todo: try to make range variable
    url = "https://gatherer.wizards.com/Pages/Search/Default.aspx?page=" + str(page) + "&action=advanced&cmc=+%3E=[0]"

    results = requests.get(url)

    html = BeautifulSoup(results.text, "html.parser")
    
    cards_tr = html.find_all('tr', class_="cardItem")

    for card in cards_tr:
        card_name = card.find('span', class_="cardTitle").text.strip("\n")
        card_names.append(card_name)
        
        card_type = card.find('span', class_="typeLine").text
        card_type = card_type.replace("\r\n","")
        card_type = " ".join(card_type.split())
        card_types.append(card_type)
        
        rules_text_symbols = []
        rules_text = str(card.find('div', class_="rulesText").find_all('p'))
        for img in card.find('div', class_="rulesText").find_all('img', alt=True):
            symbol = img.get('alt')
            rules_text_symbols.append(MANA_SYMBOLS.get(symbol,symbol))
        for symbol in rules_text_symbols:
            rules_text = re.sub('<img.*?/>',symbol,rules_text,1)
        
        rules_text = re.sub('<p>|</p>,|</p>|<i>|</i>|\[|\]','',rules_text)
        rules_texts.append(rules_text)
        
        mana_cost = []
        for img in card.find('span', class_="manaCost").find_all('img', alt=True):
            symbol = img.get('alt')
            mana_cost.append(MANA_SYMBOLS.get(symbol,symbol))
        mana_costs.append(''.join(mana_cost))
        
        cmc = int(card.find('span', class_="convertedManaCost").text)
        cmcs.append(cmc)
    
    for i in range(len(cards_tr)):
        if 'Creature' in card_types[page*100 + i]:
            power_start = card_types[page*100 + i].rfind('(') + 1
            power_end = card_types[page*100 + i].rfind('/')
            
            power.append(card_types[page*100 + i][power_start:power_end])
            toughness.append(card_types[page*100 + i][power_end + 1:-1])
        else:
            power.append(None)
            toughness.append(None)
            
    for i in range(len(cards_tr)):
        color_str = ''
        for color in ['W','U','B','R','G']:
            if color in mana_costs[page*100 + i]:
                color_str += color
        if color_str == '':
            colors.append(None)
        else:
            colors.append(color_str)

cards = pd.DataFrame({
    'Name': card_names,
    'Type': card_types,
    'Rules Text': rules_texts,
    'Mana Cost': mana_costs,
    'Converted Mana Cost': cmcs,
    'Power': power,
    'Toughness': toughness,
    'Color': colors
    })
