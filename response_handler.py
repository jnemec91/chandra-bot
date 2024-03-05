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
    """
    Handles all the responses to the user
    Parameters:
        message (discord.Message): message from the user
        client (discord.Client): client object
    Returns:
        list: message on index 1, list of embeds on index 2
        or
        str: message
    """
    card_names = re.findall(r'\[(.*?)\]', message.content)

    if card_names != []:
        set_of_embeds = []       
        embeds = []

        try:
            for card_name in card_names:
                card_name = card_name.replace('[', '').replace(']','').replace(',',' ')

                if card_name.startswith('$'):
                    card_data = get_card_data(card_name[1:])
                    if isinstance(card_data, scrython.cards.named.Named):
                        card_prices = get_price(card_data)
                        name = get_name(card_data)

                        embed = discord.Embed()
                        embed.title = f'{name} prices'

                        try:
                            for price in card_prices:
                                embed.add_field(name=price[0], value=price[1], inline=True)
                        except Exception as e:
                            continue

                        return [f'Here are known prices for card {name}:', [[embed]]]
                    
                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')


                elif card_name.startswith('?'):
                    card_data = get_card_data(card_name[1:])
                    if isinstance(card_data, scrython.cards.named.Named):
                        card_rulings = get_rulings(card_data)
                        name = get_name(card_data)
                        data = requests.get(card_rulings)
                        data = data.json()
                        data = [object['comment'] for object in data['data']]
                        if data == []:
                            data = ['ReAdinG ThE cArD, ExPlaIns ThE cArD :point_down::fire:']
                        embed = discord.Embed()
                        embed.title = f'{name} rulings'
                        embed.url = get_link(card_data)
                        embed.description = '\n\n'.join(data)

                        return [f'Here are rulings for {name}:', [[embed]]]
                    
                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')                    


                elif card_name.startswith('@'):
                    try:
                        results = search_cards(card_name[1:])
                    except Exception as e:
                        return (f'Sorry, but but there is problem with your search: {e}')

                    for i in results[1]:

                        # oracle = emojize(i[-1],client, message)[1]
                        # mana_cost = emojize(i[-2],client, message)[1]

                        # emojizing long lists of cards is too slow, so i commented it out, but it works
                        # TODO: add emojis in baches instead of one by one, to speed up the process, find a way to speed up emojize function

                        oracle = i[-1]
                        mana_cost = i[-2]
                        card_type = i[-3]

                        embed = discord.Embed()
                        embed.title = i[0]
                        embed.set_thumbnail(url=i[2])
                        embed.description = f'{mana_cost}\n{card_type}\n{oracle}'

                        if 'gatherer' in i[1].keys():
                            embed.url = i[1]['gatherer']

                        elif 'edhrec' in i[1].keys():
                            embed.url = i[1]['edhrec']
                        
                        embeds.append(embed)

                        if len(embeds) == 10:
                            set_of_embeds.append(embeds)
                            embeds = []


                else:
                    card_data = get_card_data(card_name)

                    if isinstance(card_data, scrython.cards.named.Named):

                        mana_cost = emojize(get_mana_cost(card_data), client, message)
                        oracle = emojize(get_oracle(card_data), client, message)
                                    
                        embed = discord.Embed(title=get_name(card_data), description=f'{mana_cost}\n{get_type(card_data)}\n{oracle}', url=get_link(card_data))
                        embed.set_thumbnail(url=get_card_image(card_data))

                        embeds.append(embed)

                        if len(embeds) == 10:
                            set_of_embeds.append(embeds)
                            embeds = []


                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')
                    
            set_of_embeds.append(embeds)

            if len(set_of_embeds) <= 10:
                variable_message = 'Here you go:\n'
            else:
                variable_message = f'Here is first {len(set_of_embeds[0])}:\n'

            return [f'I found total {sum([len(i) for i in set_of_embeds])} cards with this parameters. {variable_message}', [set_of_embeds[0]]]
                
        except Exception as e:
            #print(e) # for debugging purposes
            return('Some error occured, i dont feel so good. Contact admin and tell him to help me.')
        








def get_card_data(card_name):
    """
    Uses scrython module to search cards via scryfall api with exact search or fuzzy search and get card data
    Parameters:
        card_name (str): name of the card to search
    Returns:
        scrython.cards.named.Named: card data object or error message if card not found
    """
    try:
        if card_name[0] == '>':
            card_data = scrython.cards.Named(exact=card_name[1:])
        else:
            card_data = scrython.cards.Named(fuzzy=card_name)
        return (card_data)

    except Exception as e:
            return f"Error: {e}"


def search_cards(query):
    """
    Uses scrython module to search cards via scryfall api with scryfall query
    Parameters:
        query (str): scryfall query
    Returns:
        tuple: total number of cards found, list of lists with card data
    """
    results = scrython.cards.Search(q=query, order='name', unique='cards')
    return (results.total_cards(),[[object['name'], object['related_uris'], object['image_uris']['normal'], object['type_line'], object['mana_cost'], object['oracle_text']]  for object in results.data() if 'image_uris' in object.keys()])

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

def get_price(card_data):
    prices = []
    for currency in ['usd', 'usd_foil', 'usd_etched', 'usd_glossy', 'eur', 'tix']:
        try:
            price = card_data.prices(currency)
            if price == None:
                price = 'N/A'
        except KeyError:
            price = 'N/A'
        prices.append([currency,price])
    return prices

def get_rulings(card_data):
    return card_data.rulings_uri()

def emojize(text, client, message):
    """
    Replaces all mana symbols in text with discord emojis and adds them to server,
    if they are not already there.
    Parameters:
        text (str): text to replace mana symbols in
        client (discord.Client): client object
        message (discord.Message): message from the user
    Returns:
        str: text with replaced mana symbols
    """
    try:
        guild = client.get_guild(message.guild.id)

        all_symbols = re.findall(r'{.[^}]*}', text)
        symbol_data = scrython.symbology.Symbology().data()

        for i in all_symbols:
            symbol_object = next((obj for obj in symbol_data if obj['symbol'] == i), False)

            if symbol_object:
                name = i.replace('}','symbol').replace('{','').replace('/','')

                if name not in [e.name for e in message.guild.emojis]: 
                    img_byte_arr = download_emoji(symbol_object['svg_uri'])
                    asyncio.run(add_moji(guild, name, img_byte_arr))

                emoji = next((obj for obj in message.guild.emojis if obj.name == name), i)
                text = text.replace(i, str(emoji))

        return text
    
    except Exception as e:
        print(e)



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