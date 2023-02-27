# GPT-3 Telegram Translation Bot

This Telegram bot translates words from English to Russian using the OpenAI GPT-3 API. The bot provides the meaning of the word, its transcription, popularity, translation variants, and usage examples.

![GPT3-Translate-Bot](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/7f269142-16dc-4e59-ba8c-7823679fe85e/frogly-translates.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230227%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230227T110632Z&X-Amz-Expires=86400&X-Amz-Signature=a412a4bc1087885606d2b746a30d06d65ac923bd0f98f036774464a0d186476c&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22frogly-translates.png%22&x-id=GetObject)


## Requirements
* Python 3.11
* pyTelegramBotAPI module
* psycopg2-binary module
* openai module
* Telegram Bot token
* OpenAI API key
* PostgreSQL DB with word's frequency

## Usage
1. Run the bot by running python bot.py in the terminal.
2. Search for the bot in Telegram and start a chat with it.
3. Send a message containing the English word you want to translate.
4. The bot will reply with the word's meaning, transcription, popularity, translation variants, and usage examples.

Note: The message must contain an English word, and the word must be no more than 45 characters. The bot will not respond to messages that do not comply with these rules.

## Disclaimer
This bot is for educational and experimental purposes only. The accuracy and reliability of the translations provided by the bot may vary. The developer of this bot is not responsible for any errors or inaccuracies in the translations provided.
