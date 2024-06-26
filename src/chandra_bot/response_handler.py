import discord
import scrython
import re
import asyncio
import requests
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import io

# TODO: add more error handling, add MagicCard class wich will hold all the data and methods for card


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
                card_name = card_name.replace(
                    '[', '').replace(']', '').replace(',', ' ')

                if card_name.startswith('$'):
                    card_data = get_card_data(card_name[1:])
                    if isinstance(card_data, scrython.cards.named.Named):
                        card_prices = get_price(card_data)
                        name = get_name(card_data)

                        embed = discord.Embed()
                        embed.title = f'{name} prices'
                        embed.url = get_link(card_data)

                        try:
                            for price in card_prices:
                                embed.add_field(
                                    name=f'> {price[0]}', value=f'> {price[1]}', inline=True)
                        except Exception as e:
                            continue

                        return [f'Here are known prices for card {name}:', [[embed]]]

                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')

                elif card_name.startswith('?'):
                    card_data = get_card_data(card_name[1:])
                    if isinstance(card_data, scrython.cards.named.Named):
                        card_rulings = card_data.rulings_uri()
                        name = get_name(card_data)

                        data = requests.get(card_rulings)
                        data = data.json()
                        data = [
                            f'\n - **{object["comment"]}**' for object in data['data']]
                        if data == []:
                            data = [
                                'ReAdinG ThE cArD, ExPlaIns ThE cArD :point_down::fire:']

                        embed = discord.Embed()
                        embed.title = f'{name} rulings'
                        embed.url = get_link(card_data)
                        embed.description = f'> {"".join(data)}'

                        return [f'Here are rulings for {name}:', [[embed]]]

                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')

                elif card_name.startswith('@'):
                    try:
                        results = search_cards(card_name[1:])
                    except Exception as e:
                        return (f'Sorry, but but there is problem with your search: {e}')

                    for i in results[1]:
                        if len(set_of_embeds) < 1:
                            oracle = emojize(i[-1], client, message)
                            mana_cost = emojize(i[-2], client, message)

                        else:
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

                elif card_name.startswith('!'):
                    card_data = get_card_data(card_name[1:])
                    if isinstance(card_data, scrython.cards.named.Named):
                        card_flavor = card_data.flavor_text()
                        name = get_name(card_data)

                        embed = discord.Embed()
                        embed.title = f'{name}'
                        embed.image = get_card_image(card_data)
                        embed.url = get_link(card_data)

                        embeds.append(embed)

                        if embeds == 10:
                            set_of_embeds.append(embeds)
                            embeds = []

                    else:
                        return (f'Sorry, but but there is problem with your search: {card_data[6:]}')

                else:
                    card_data = get_card_data(card_name)

                    if isinstance(card_data, scrython.cards.named.Named):

                        mana_cost = emojize(
                            card_data.mana_cost(), client, message)
                        oracle = emojize(
                            card_data.oracle_text(), client, message)

                        try:
                            flavor = f'*{card_data.flavor_text()}*'
                        except Exception as e:
                            flavor = ''

                        embed = discord.Embed(title=f'{get_name(card_data)} {mana_cost}',
                                              description=f'\n{card_data.type_line()}\n\n{oracle}\n\n{flavor}', url=get_link(card_data))
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
            # print(e) # for debugging purposes
            return ('Some error occured, i dont feel so good. Contact admin and tell him to help me.')


def get_card_data(card_name):
    """
    Uses scrython module to search cards via scryfall api with exact search or fuzzy search and get card data
    Parameters:
        card_name (str): name of the card to search
    Returns:
        scrython.cards.named.Named: card data object or error message if card not found
    """
    try:
        if card_name[0] == '=':
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
    print(results)
    return (results.total_cards(), [[object['name'], object['related_uris'], object['image_uris']['normal'], object['type_line'], object['mana_cost'], object['oracle_text']] for object in results.data() if 'image_uris' and 'oracle_text' in object.keys()])


def get_name(card_data):
    """Returns name of the card"""
    return card_data.name()


def get_card_image(card_data):
     """Returns url of image of the card"""
     return card_data.image_uris()['normal']

def get_link(card_data):
    """Returns url of the card on gatherer or none if not found"""
    try:
        return card_data.related_uris()['gatherer']
    except Exception:
         return None


def get_price(card_data):
    """Returns list of prices for the card in different currencies"""
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
    """
    Downloads svg image and converts it to png
    Parameters:
        url (str): url of the svg image
    Returns:
        bytes: png image
    """
    img_response = requests.get(url)
    img_response.raise_for_status()

    svg_buffer = io.BytesIO(img_response.content)

    drawing = svg2rlg(svg_buffer)
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