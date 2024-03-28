import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncio
import nest_asyncio
from response_handler import handle_response

nest_asyncio.apply()

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    """
    Main event handler for messages. It checks if the message is from the bot itself and if not, it passes the message to the response handler.
    """
    if message.author == client.user:
        return
    
    else:
        response = handle_response(message, client)

        if response != None:

            if isinstance(response, list) and len(response) <= 1:
                await message.channel.send(embeds=response)


            elif isinstance(response, list) and len(response) > 1:
                await message.channel.send(f'{response[0]}')

                for set_of_embeds in response[1]:
                    await message.channel.send(embeds=set_of_embeds)
                    
            else:
                await message.channel.send(f'{response}')

            for e in message.guild.emojis:
                if 'symbol' in e.name:
                    await message.guild.delete_emoji(e)


@client.slash_command(name="help", description="Display ChandraBot ussage info.")
async def help(ctx):
    """
    Display ChandraBot ussage info.
    """

    await ctx.respond(
"""Hello, im ChandraBot, blazingly fast card search helper. Just write a message in right format and I'll fetch all info needed about a card for you!
These are commands you might be interested in:
`Search a card by name or part of it: [card name]`
`Search a card by exact name: [=card name]`
`Search cards with using scryfall query, due to chance of really large results comming back, limited number of results will be displayed: [@query]`
`Scryfall query reference: https://scryfall.com/docs/reference`

Every of theese commands is possible to use alone or in context of a sentence. Chaining commands is also possible to some extent. For example:
`'This is really cool card and my personal pet pick to every white deck [aegis gods]'`
`'[@cmc:6 and t:creature and type:elf and type:shaman and c:gb]'`
`'I want to play [aegis gods] in my competetive deck, but it dies to [=Lightning Bolt] every time.'`

If you want ot know more about cards, you can use the following commands:
`Search card prices by its name or part of it: [$card name]`
`Search card rules by its name or part of it: [?card name]`

Theese are not chainable, so no other commands will be resolved in the same message.

I'm here to help you! :fire:

""",
ephemeral=True
)

if __name__ == '__main__':
    with open('token.key') as key_file:
        client.run(str(key_file.read()))

