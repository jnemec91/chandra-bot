# ChandraBot

This is a Discord bot written in Python that utilizes the `py-cord` and `scrython` libraries to provide Magic: The Gathering (MTG) related functionalities. The bot can fetch card data, including prices, rulings, and card images, from the Scryfall API, and display them in Discord.
Additionally, it can replace mana symbols in text with Discord emojis.

You can try the bot on my [discord server](https://discord.gg/269FbPXBhR)

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
- `[=card name]`: Fetches detailed information about the specified MTG card, utilizing exact search.
- `[@scryfall query]`: Fetches detailed information about first 10 cards from result of scryfall query.
- `[$card name]`: Retrieves the current prices of the specified MTG card in various currencies.
- `[?card name]`: Displays official rulings for the specified MTG card.
- `[!card name]`: Displays full sized image of the card.

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

## Quick deploy guide on AWS EC2

Since AWS has free tier plan where you can get 12 months for free, it's great platform to deploy and run the bot.

1. **Create an AWS EC2 Instance:**
   - Log in to your AWS Management Console.
   - Navigate to the EC2 dashboard.
   - Click on "Launch Instance" and select a suitable AMI (Amazon Machine Image) for your instance. Choose an instance type, configure instance details, add storage, configure security groups, and review your instance settings.
   - Launch the instance and download the key pair file (.pem) to access your instance.

2. **Connect to Your EC2 Instance:**
   - Use built-in AWS EC2 Instance Connect to ssh to your EC2 instance
   - Or use an SSH client (e.g., Terminal on macOS/Linux, PuTTY on Windows) to connect to your EC2 instance using the downloaded key pair file.

3. **Clone Your Repository:**
   - Once connected to your EC2 instance, clone your repository using Git:
     ```
     git clone <repository-url>
     cd <repository-directory>
     ```

4. **Install Required Python Libraries:**
    - This is always a good idea
      ```
      sudo apt-get update
      ```
    - Install pip
      ```
      sudo apt-get install python3-pip
      ```

   - Navigate to base directory of bot application.
   - Run the following command to install the required Python libraries:
     ```
     sudo pip install -r requirements.txt
     ```

5. **Obtain Discord Bot Token:**
   - Obtain your Discord bot token from the Discord Developer Portal.
   - Create a `token.key` file in the base directory of your repository on the EC2 instance.
   - Copy your Discord bot token into the `token.key` file.

6. **Run the Bot Script as a Service:**
   - You can use `systemd` to manage your bot script as a service on Linux.
   - Create a systemd service file for your bot:
     ```
     sudo nano /etc/systemd/system/chandrabot.service
     ```
     Replace `nano` with your preferred text editor.
   - Add the following content to the `chandrabot.service` file:
     ```
     [Unit]
     Description=Discord Bot

     [Service]
     User=your_user_name
     WorkingDirectory=/path/to/your/repository
     ExecStart=/usr/bin/python3 main.py
     Restart=always
     StandardOutput=syslog
     StandartError=syslog

     [Install]
     WantedBy=multi-user.target
     ```
     Replace `/path/to/your/repository` with the actual path to your bot script.
     Replace `your_user_name` with the actual username of some user.     

7. **Start and Enable the Service:**
   - Reload systemd manager configuration
     ```
     sudo systemctl daemon-reload
     ```
   - Restart the systemd service for your bot:
     ```
     sudo systemctl restart chandrabot.service
     ```
   - Enable the service to start on boot:
     ```
     sudo systemctl enable chandrabot
     ```

8. **Monitor the Service:**
   - You can monitor the status of your bot service using the following command:
     ```
     sudo systemctl status chandrabot
     ```
   - You can check syslog messages to confirm bot runs using this command:
     ```
     sudo cat /var/log/syslog
     ```

Your bot should now be running as a service on your AWS EC2 instance. You can verify its functionality by checking its status or interacting with it on Discord.

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

## Contributors

- [Jaroslav Němec](https://github.com/jnemec91) - Creator and maintainer

## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to Scryfall for providing the API used in this project.
- Special thanks to the Discord community for their support and inspiration.
