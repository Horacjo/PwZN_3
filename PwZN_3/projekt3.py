import argparse
import requests
import json
import gzip
from rich.console import Console
import rich.traceback
from bs4 import BeautifulSoup

console = Console()
console.clear()
rich.traceback.install()

parser = argparse.ArgumentParser(description="Opis:")
parser.add_argument('file', help = "Użytkowniku podaj nazwę pliku do zapisu")
args = parser.parse_args()

req = requests.get('https://www.plusliga.pl/teams/id/2100016.html')
soup = BeautifulSoup(req.text, "html.parser")

player_names = soup.find_all('div', class_="playerinfo")
table = []
i = 0

for names in player_names:
    name = names.find('a').text.strip()
    position = names.find('p').text.strip()
    number = names.find('span').text
    
    table.append([name, position, number])

with gzip.open(args.file + '.json.gzip', 'wt', encoding = 'utf-8') as f:
    json.dump(table, f)

with gzip.open(args.file + '.json.gzip', 'rt', encoding = 'utf-8') as f:
    y = json.load(f)
    console.print(y)
