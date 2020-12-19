import requests
from bs4 import BeautifulSoup
from unicodedata import normalize
import re

pokemon_dict = {}

def get_names(soup):
    """Retreives the name of the pokemon and additional forms (regional variants, mega, gigantamax, etc.) from the current page."""
    # TO DO: Charizard returns two Gigantamax Charizard. Need to get rid of duplicates. Mega Charizard has hex decimal characters.
    # TO DO: Remove Gigantamax names from list. Gigantamax pokemon don't have unique types or abilities.

    names_list = []

    html_block = soup.find(id='mw-content-text').find('table', class_='roundy', style='background:#FFF;')
    names_html = html_block.find_all(class_=('image'))
    for name in names_html:
        # Gigantamax pokemon don't have altered stats, abilites, or types so they are excluded.
        if name['title'].startswith('Gigantamax'):
            pass
        else:
            names_list.append(name['title'])
    return names_list

def get_types(soup):
    type_list = []

    html_block = soup.find('a', title='Type').parent.find_next('table').find('tr')
    types_html = html_block.find_all('td', {'style': lambda x: x != 'display: none;'}, recursive=False)
    for type_ in types_html:
        type_list.append(type_.find('tr').find('b').text)
        type_list.append(type_.find('tr').find('b').find_next('b').text)
    return type_list

def get_abilities(soup):
    # TO DO: Check to make sure abilities match up with different forms. Slowbro comes to mind.
    html_block = soup.find('a', title='Ability').parent.find_next('table')
    abilities_html = html_block.find_all('td', {'style': lambda x: x != 'display: none'})
    return [ability.find('span').text for ability in abilities_html]

def get_weights(soup):
    weight_list = []

    html_block = soup.find('a', title='Weight').parent.find_next('table')
    weights = html_block.find_all('tr', {'style': lambda x: x != 'display:none;'})
    for weight in weights:
        text = weight.find('td').text
        try:
            re_result = re.findall('[0-9]+.[0-9]+', text)
            if len(re_result) == 0:
                continue
            else:
                weight_list.append(re_result[0])
        except:
            continue
    return weight_list

def get_base_stats(soup):

    stats_list = []

    html_blocks = soup.find_all('a', href='/wiki/Statistic', title='Statistic')

    for html_block in html_blocks: 
        html_block = html_block.parent.parent.parent
        hp = html_block.find('tr', style='background: #FF5959; text-align:center').find('div', style='float:right').string
        attack = html_block.find('tr', style='background: #F5AC78; text-align:center').find('div', style='float:right').string
        defense = html_block.find('tr', style='background: #FAE078; text-align:center').find('div', style='float:right').string
        sp_attack = html_block.find('tr', style='background: #9DB7F5; text-align:center').find('div', style='float:right').string
        sp_def = html_block.find('tr', style='background: #A7DB8D; text-align:center').find('div', style='float:right').string
        speed = html_block.find('tr', style='background: #FA92B2; text-align:center').find('div', style='float:right').string
        stats_list.append((hp, attack, defense, sp_attack, sp_def, speed))

    return stats_list

def get_next_pokemon(soup):
    next_pokemon = soup.find(id='mw-content-text').find(style='text-align: left').a['href']
    return next_pokemon

current_URL = 'https://bulbapedia.bulbagarden.net/wiki/Slowbro_(Pokémon)'
page = requests.get(current_URL)
soup = BeautifulSoup(page.content, 'html.parser')

counter = 0
type_counter = 0
names_list = get_names(soup)

for name in names_list:

    types_list = get_types(soup)
    abilities_list = get_abilities(soup)
    weights_list = get_weights(soup)
    base_stats_list = get_base_stats(soup)

    print(len(abilities_list)-len(names_list)+1)

    try:
        if counter == 0:
            pokemon_dict[name] = types_list[type_counter:type_counter+2], abilities_list[0:len(abilities_list)-len(names_list)+1], weights_list[counter], base_stats_list[counter]
        else:
            pokemon_dict[name] = types_list[type_counter:type_counter+2], abilities_list[counter], weights_list[counter], base_stats_list[counter]
    except Exception:
        continue
    finally:
        counter += 1
        type_counter += 2

print(pokemon_dict)
# pokemon_dict[get_name(soup)] = get_type(soup), get_abilities(soup), get_weight(soup), get_base_stats(soup)
# print(f'{get_name(soup)}: {pokemon_dict[get_name(soup)]}')

# TO DO: Make a way for it to stop at the last pokemon and not loop.
# Maybe use a named tuple instead?
# for x in range(898):
#     try:
#         page = requests.get(current_URL)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         pokemon_dict[get_name(soup)] = get_type(soup), get_abilities(soup), get_weight(soup), get_base_stats(soup)
#         print(f'{get_name(soup)}: {pokemon_dict[get_name(soup)]}')
#         current_URL = 'https://bulbapedia.bulbagarden.net' + get_next_pokemon(soup)

#     except:
#         continue