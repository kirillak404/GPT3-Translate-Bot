import config
import telebot
import openai
import ast
import re

bot = telebot.TeleBot(config.telegram_api_key)
openai.api_key = config.openai_api_key


def message_checker(message):
    # This function checks the message for compliance with the rules
    if len(message) > 45 or not re.match("^[A-Za-z0-9 .,!?'\";:-]+$", message):
        return False
    else:
        return True


def request_openai_translation(word):
    # This function takes a word, sends it to OpenAI, and returns a dictionary with the translation.
    word = f"Explain to me the meaning of the word \"{word}\" in simple words. " \
           "Add 3 different examples of usage. Add an emoji that resembles this word as much as possible. " \
           "Add 1 or more different translations into Russian. Add the transcription of this word. " \
           "Add the frequency of the word's use in English on a scale of 1 to 100. " \
           "Return the answer to me in Python dictionary format, like this: " \
           "{\"word\": \"Gecko\", \"transcription\": \"[ˈgekəʊ]\", \"frequency\": \"34\", " \
           "\"emoji\": \"🦎\", \"definition\": \"Gecko is a type of small, usually nocturnal, " \
           "lizard found in warm climates around the world.\", " \
           "\"translations\": \"геккон, ящер, ящерица\", \"examples\": " \
           "(\"My pet gecko loves to roam around the house at night.\", " \
           "\"I saw a gecko in the garden this morning.\", " \
           "\"The gecko has unique adhesive pads on its feet that allow it to climb walls.\")}"
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=word,
            temperature=0.5,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ast.literal_eval(response.choices[0].text)

    except Exception as e:
        print(e)
        return False


# def generate_picture(word):
# # This function takes a word, sends it to OpenAI, and returns a link to the picture.
#     try:
#         response = openai.Image.create(
#             prompt=word,
#             n=1,
#             size="256x256"  # 256x256, 512x512, 1024x1024
#         )
#         return response['data'][0]['url']
#     except Exception as e:
#         print(e)
#         return False


@bot.message_handler(commands=['start', 'help'])
# Handling incoming Telegram commands
def send_welcome(message):
    print(message)
    bot.reply_to(message,
                 f'👋 Привет, {message.from_user.first_name}!\n\nЯ бот, '
                 f'который переводит слова с английского на русский с помощью ChatGPT. '
                 f'Пришли мне любое слово, а я его переведу!')


@bot.message_handler(func=lambda message: True)
# Handling incoming Telegram messages
def echo_all(message):
    if message_checker(message.text):  # checks the message for compliance with the rules
        bot.send_chat_action(message.chat.id, 'typing')
        translation = request_openai_translation(message.text)

        if translation:  # if received translation from openAI func – send it to user
            examples = "".join([f'- _{example}_\n' for example in translation['examples']])
            answer = f"{translation['emoji']} *{translation['word']}* [{translation['transcription']}] " \
            f"– {translation['definition']}\n\n*Popularity:* {translation['frequency']} of 100\n" \
            f"*Translation:* {translation['translations']}\n\n*Examples*\n{examples}"

            bot.send_message(message.chat.id, answer, parse_mode="markdown")

        else:  # if not received translation from openAI func – send error message
            bot.send_message(message.chat.id, 'Сорри йа, что-то пошло не так, попробуйте еще разок...')

    else:  # if message not compliance with the rules – send error message
        bot.send_message(message.chat.id, "Введите слово или фразу на английском языке и не более 45 символов")


bot.infinity_polling()
