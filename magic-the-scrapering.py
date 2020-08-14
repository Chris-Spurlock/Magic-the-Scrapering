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

cards_tr = html.find_all('tr', class_="cardItem")

for container in cards_tr:
    card_name = container.find('span', class_="cardTitle").text.strip("\n")
    card_names.append(card_name)
    
    card_type = container.find('span', class_="typeLine").text
    card_type = card_type.replace("\r\n","")
    card_type = " ".join(card_type.split())
    card_types.append(card_type)
    
    rules_text = str(container.find('div', class_="rulesText").find_all('p'))
    rules_text = re.sub('<p>|</p>,|</p>|\[|\]','',rules_text)
    rules_texts.append(rules_text)
    
    mana_cost = []
    for img in container.find('span', class_="manaCost").find_all('img', alt=True):
        mana_cost.append(img.get('alt'))
    mana_costs.append(mana_cost)
    
    cmc = container.find('span', class_="convertedManaCost").text
    cmcs.append(cmc)

cards = pd.DataFrame({
    "Name": card_names,
    "Type": card_types,
    "Rules Text": rules_texts,
    "Mana Cost": mana_costs,
    "Converted Mana Cost": cmcs
    })
