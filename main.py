import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncio
import nest_asyncio
from response_handler import handle_response

nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    else:
        response = handle_response(message, client)

        if response != None:

            if isinstance(response, list):
                await message.channel.send(embeds=response)

                for e in message.guild.emojis:
                    if 'symbol' in e.name:
                        await message.guild.delete_emoji(e)

            elif isinstance(response, tuple):
                await message.channel.send(f'{response[0]}')
                embeds = []
                for i in response[1]:
                    # print(i)
                    embed = discord.Embed()
                    embed.title = i[0]
                    embed.set_thumbnail(url=i[2])

                    if 'gatherer' in i[1].keys():
                        embed.url = i[1]['gatherer']

                    elif 'edhrec' in i[1].keys():
                        embed.url = i[1]['edhrec']
                    
                    embeds.append(embed)

                    if len(embeds) == 10:
                        await message.channel.send(embeds=embeds)
                        embeds = []
                        
                if len(embeds) > 0:
                    await message.channel.send(embeds=embeds)

            else:
                await message.channel.send(f'{response}')


@client.slash_command(name="help", description="Display Chandrabot ussage info.")
async def test(ctx):
    await ctx.respond(
"""Hello, im ChandraBot, blazingly fast card search helper. Just write a message in right format and I'll fetch all info needed about a card for you!
These are commands you might be interested in:
`Search a card by name or part of it: [ card name ]
Search a card by exact name: [^ card name ]
Search cards with using scryfall query: [@ query ]
Scryfall query reference: https://scryfall.com/docs/syntax`

Every of theese commands is possible to use alone or in context of a sentence. For example:
`'This is really cool card and my personal pet pick to every white deck [aegis gods]'`
`'[@cmc:6 and t:creature and type:elf and type:shaman]'`
`'I want to play [aegis gods] in my competetive deck, but it dies to [^Lightning Bolt] every time.'`

But note that query command (one that starts with @) is only possible to use alone, not in combination with other commands. If you use it in combination, only the query will be processed.
"""
)

if __name__ == '__main__':
    with open('token.key') as key_file:
        client.run(str(key_file.read()))

