import discord
import asyncio
import nest_asyncio
from response_handler import handle_response

nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

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

            if isinstance(response, discord.Embed):
                await message.channel.send(embed=response)

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




if __name__ == '__main__':
    with open('token.key') as key_file:
        client.run(str(key_file.read()))

