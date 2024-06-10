import sys
import bot

try:
    bot.app_run(sys.argv[1])
except IndexError:
    print('Provide discord bot token key to run the bot.')