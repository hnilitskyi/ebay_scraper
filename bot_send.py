import sys
import json
import asyncio
from telegram import Bot


async def send_telegram_message(chat_id, token_for_chatbot, message):
    bot = Bot(token=token_for_chatbot)
    await bot.send_message(chat_id=chat_id, text=message)


async def main():
    try:
        with open('scrap.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print('no data')

    bot_token = data['token']
    id_chat = data['chatid']
    value_current = float(sys.argv[1])
    value_last = float(sys.argv[2])
    if value_current != value_last:
        value_change = value_current - value_last
        if value_change > 0:
            mess = f'Price is growing for: +{round(value_change, 2)}'
            await send_telegram_message(id_chat, bot_token, mess)
        else:
            mess = f'Price is reduce for: {round(value_change, 2)}'
            await send_telegram_message(id_chat, bot_token, mess)


if __name__ == "__main__":
    asyncio.run(main())
