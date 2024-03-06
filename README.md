# ChandraBot

This is a Discord bot written in Python that utilizes the `py-cord` and `scrython` libraries to provide Magic: The Gathering (MTG) related functionalities. The bot can fetch card data, including prices, rulings, and card images, from the Scryfall API, and display them in Discord.
Additionally, it can replace mana symbols in text with Discord emojis.

## Features

- **Card Search:** Users can search for MTG cards by name, and the bot will return detailed information about the card, including its mana cost, type, oracle text, flavor text, and more.
- **Price Lookup:** Users can request the current prices of MTG cards in various currencies. The bot fetches this data from the Scryfall API.
- **Rulings Display:** Users can view the official rulings for MTG cards retrieved from Scryfall API.
- **Mana Symbol Replacement:** The bot replaces mana symbols in text messages with Discord emojis, adding them to the server if necessary.
- **Card Image Display:** Users can view the normal-sized card image for the requested MTG card.

## Usage

To use this bot, invite it to your Discord server and prefix your commands within square brackets with a specific character (e.g., `$`, `?`, `@`). Here are some example commands:

- `/help`: Displays help message with examples of usage.
- `[card name]`: Fetches detailed information about the specified MTG, utilizing fuzzy search.
- `[>card name]`: Fetches detailed information about the specified MTG card, utilizing exact search.
- `[@scryfall query]`: Fetches detailed information about first 10 cards from result of scryfall query.
- `[$card name]`: Retrieves the current prices of the specified MTG card in various currencies.
- `[?card name]`: Displays official rulings for the specified MTG card.


## Requirements

- `Python 3.8+`
- `aiohttp` library
- `aiosignal` library
- `asyncio` library
- `attrs` library
- `certifi` library
- `chardet` library
- `charset-normalizer` library
- `cssselect2` library
- `freetype-py` library
- `frozenlist` library
- `idna` library
- `lxml` library
- `multidict` library
- `nest-asyncio` library
- `pillow` library
- `py-cord` library
- `pycairo` library
- `reportlab` library
- `requests` library
- `rlPyCairo` library
- `scrython` library
- `svglib` library
- `tinycss2` library
- `urllib3` library
- `webencodings` library
- `yarl` library



## Setup

1. Clone this repository to your local machine.
2. Install the required Python libraries using pip:
    ```
    pip install -r requirements.txt
    ```
3. Obtain a Discord bot token, create `token.key` file in the base directory and copy the token into it.
4. Run the bot script:
    ```
    python main.py
    ```

## Contributors

- [Jaroslav Němec](https://github.com/jnemec91) - Creator and maintainer

## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Scryfall for providing the API used in this project.
- Special thanks to the Discord community for their support and inspiration.
