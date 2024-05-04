eBay scraper with Telegram integration allows users to track price changes for items on the eBay website and receive notifications of changes through Telegram. Users input their Telegram bot token, chat ID, and the eBay item link, and then the script automatically monitors the price and notifies the user of any changes.

     Features
User Interface: Users can easily configure tracking parameters by entering the required data in the application's graphical interface.
Price Tracking: The script periodically checks the price of the specified eBay item and saves the last known price in a JSON file for subsequent comparison.
Telegram Integration: Users receive notifications of price changes for items through Telegram. The bot sends messages with information about how much the price has changed.
     
     Usage
Make sure to install:
PyQt5, BeautifulSoup4, fake_useragent, requests, python-telegram-bot

     
Install Dependencies: Make sure you have the PyQt5, beautifulsoup4, fake-useragent, and python-telegram-bot libraries installed. You can install them using pip: pip install PyQt5 beautifulsoup4 fake-useragent python-telegram-bot.
Launch the Application: Run the main.py file to open the graphical interface.
Configure Parameters:
Enter your Telegram bot token in the corresponding field.
Enter your chat ID for the bot in the corresponding field.
Paste the link to the item on eBay in the corresponding field.
Start Tracking: Click the "Start" button to begin monitoring the item's price. The script will periodically check the price and send notifications of any changes.

Note: Ensure you have an active internet connection and correctly specify the Telegram bot and chat parameters to receive notifications.

Telegram Bot Setup:

Create a Telegram bot using BotFather (https://core.telegram.org/bots#botfather).
Obtain the bot token provided by BotFather.
Find your chat ID by sending a message to your bot and visiting the following URL: https://api.telegram.org/botYourBotToken/getUpdates. Look for the "chat" section to find your chat ID.
