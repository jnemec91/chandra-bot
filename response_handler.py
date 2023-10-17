import discord
import scrython
import re
import asyncio
import requests
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io

def handle_response(message, client):
    card_names = re.findall(r'\[[@\w\s\D]+\]', message.content)
    print(card_names)
    if message.content.startswith('[') and message.content.endswith(']') or card_names != []:        
        
        try:
            card_name = card_names[0].replace('[', '').replace(']','').replace(',',' ')
            print(card_name)
            if card_name.startswith('@'):
                results = search_cards(card_name[1:])
                print(results)
                return(f'I found total {results[0]} cards with this name. Here you go:\n', results[1])
            else:
                card_data = get_card_data(card_name)
                if isinstance(card_data, scrython.cards.named.Named):
                    
                    print(card_data, 'card data')

                    mana_cost = emojize(get_mana_cost(card_data),client, message)
                    oracle = emojize(get_oracle(card_data),client, message)
                                
                    embed = discord.Embed(title=get_name(card_data), description=f'{mana_cost[0]}\n{get_type(card_data)}\n{oracle[0]}', url=get_link(card_data))
                    embed.set_image(url=get_card_image(card_data))

                    return embed
                
                elif card_data.startswith('Error:'):
                    return (f'Sorry, but but there is problem with your search: {card_data[6:]}')
                
        except Exception as e:
            return('I cant find any cards with this name... Try adjusting your input.')
        
    elif message.content == '!help':
        return ("Hello, im ChandraBot, blazingly fast card search helper. Just write a message in right format and I'll fetch all info needed about a card for you!\nThese are commands you might be interested in:\n`Search a card by name or part of it: [card name]`\n`Search a card by exact name: [^card name]`\n`Search cards with using scryfall query: [@query]`\n`Scryfall query reference: https://scryfall.com/docs/syntax`")
    

def get_card_data(card_name):
    """Uses scrython module to search cards via scryfall api"""
    try:
        if card_name[0] == '^':
            card_data = scrython.cards.Named(exact=card_name[1:])
        else:
            card_data = scrython.cards.Named(fuzzy=card_name)
        return (card_data)

    except Exception as e:
            return f"Error: {e}"


def search_cards(query):
    results = scrython.cards.Search(q=query, order='name', unique='cards')
    return (results.total_cards(),[[object['name'], object['related_uris'], object['image_uris']['normal']]  for object in results.data() if 'image_uris' in object.keys()])

def get_name(card_data):
     return card_data.name()

def get_mana_cost(card_data):
     return card_data.mana_cost()

def get_card_image(card_data):
     return card_data.image_uris()['normal']

def get_type(card_data):
     return card_data.type_line()

def get_oracle(card_data):
     return card_data. oracle_text()

def get_link(card_data):
    try:
        return card_data.related_uris()['gatherer']
    except Exception:
         return None

def emojize(text, client, message):
    emojis =  message.guild.emojis
    result = []
    guild = client.get_guild(message.guild.id)

    symbol = scrython.symbology.Symbology()
    all_symbols = re.findall(r'{.[^}]*}', text)

    for obj in symbol.data():
        for i in all_symbols:
            if obj['symbol'] == i:
                name = i.replace('}','symbol').replace('{','').replace('/','')

                if name not in [e.name for e in emojis]: 
                    img_byte_arr = download_emoji(obj['svg_uri'])
                    asyncio.run(add_moji(guild, name, img_byte_arr)) 
                emojis =  message.guild.emojis
                for e in emojis:
                    if e.name == name:
                        text = text.replace(i, str(e))

                result.append({name: obj['svg_uri']})

    return (text, result)


def download_emoji(url):
    img_response = requests.get(url).text
    with open('media/swap_pic.svg', 'w+') as file:
        file.write(img_response)
    
    drawing = svg2rlg('media/swap_pic.svg')
    img = renderPM.drawToPIL(drawing)

    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr

async def add_moji(guild, name, image):
    await guild.create_custom_emoji(name=name, image=image)