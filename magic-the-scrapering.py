# Under Construction
# Add commentary

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

url = "https://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&action=advanced&cmc=+%3E=[0]"

results = requests.get(url)

html = BeautifulSoup(results.text, "html.parser")

card_names = []
card_types = []
rules_texts = []
mana_costs = []
cmcs = []

mana_symbols_dict = {
    'White': 'W',
    'Blue': 'U',
    'Black': 'B',
    'Red': 'R',
    'Green': 'G',
    'Phyrexian White': 'W/P',
    'Phyrexian Blue': 'U/P',
    'Phyrexian Black': 'B/P',
    'Phyrexian Red': 'R/P',
    'Phyrexian Green': 'G/P',
    'Colorless': 'C',
    'Variable Colorless': 'X'
    }

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
        rules_text_symbols.append(mana_symbols_dict.get(symbol,symbol))
    for symbol in rules_text_symbols:
        rules_text = re.sub('<img.*?/>',symbol,rules_text,1)
    
    rules_text = re.sub('<p>|</p>,|</p>|\[|\]','',rules_text)
    rules_texts.append(rules_text)
    # still have italicized text
    # consider replacing paragraph breaks with newlines
    
    mana_cost = []
    for img in card.find('span', class_="manaCost").find_all('img', alt=True):
        symbol = img.get('alt')
        mana_cost.append(mana_symbols_dict.get(symbol,symbol))
    mana_costs.append(''.join(mana_cost))
    
    cmc = int(card.find('span', class_="convertedManaCost").text)
    cmcs.append(cmc)

cards = pd.DataFrame({
    "Name": card_names,
    "Type": card_types,
    "Rules Text": rules_texts,
    "Mana Cost": mana_costs,
    "Converted Mana Cost": cmcs
    })
