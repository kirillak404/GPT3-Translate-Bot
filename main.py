import config
import telebot
import openai
import ast
import re

bot = telebot.TeleBot(config.telegram_api_key)
openai.api_key = config.openai_api_key


def message_checker(message):
    if len(message) > 45 or not re.match("^[A-Za-z0-9 .,!?'\";:-]+$", message):
        return False
    else:
        return True


#  Requesting OpenAI translation in dictionary format with keys: 'definition', 'translations', 'emoji', 'examples'
def request_openai_translation(word):
    word = 'Explain to me the meaning of the word ' + f"\"{word}\"" + """ in simple words. Add 3 different examples of usage. Add an emoji that esembles this word as much as possible. Add 1 or more different translations into Russian. Add the transcription of this word. Add the frequency of the word's use in English on a scale of 1 to 100. Return the answer to me in Python dictionary format, like this: {\"word\": \"Gecko\", \"transcription\": \"[ˈgekəʊ]\", \"frequency\": \"34\",
	# \"emoji\": \"🦎\", \"definition\": \"Gecko is a type of small, usually nocturnal, lizard found in warm climates around the world.\", \"translations\": \"геккон, ящер, ящерица\", \"examples\": (\"My pet gecko loves to roam around the house at night.\", \"I saw a gecko in the garden this morning.\", \"The gecko has unique adhesive pads on its feet that allow it to climb walls.\")}"""
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
        return ast.literal_eval(response.choices[0].text)  # return dictionary

    except Exception as e:
        print(e)
        return False


# Requesting OpenAI generate picture
def generate_picture(word):
    try:
        response = openai.Image.create(
            prompt=word,
            n=1,
            size="256x256"
        )
        return response['data'][0]['url']
    except Exception as e:
        print(e)
        return False


# Inbound telegram commands (/start and /help)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, f'👋 Привет, {message.from_user.first_name}!\n\nЯ бот, который переводит слова с английского на русский с помощью ChatGPT. Пришли мне любое слово, а я его переведу!')


# Inbound telegram messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message_checker(message.text):  # if message OK - send answer
        bot.send_chat_action(message.chat.id, 'typing')
        translation = request_openai_translation(message.text)

        if translation:  # if correct translation returned form openAI func
            bot.send_chat_action(message.chat.id, 'typing')
            image_url = generate_picture(translation['definition'])
            examples = "".join([f'- _{example}_\n' for example in translation['examples']])
            answer = f"""{translation['emoji']} *{translation['word']}* [{translation['transcription']}] – {translation['definition']}\n\n*Popularity:* {translation['frequency']} of 100\n*Translation:* {translation['translations']}\n\n*Examples*\n{examples}"""

            if image_url:  # if picture returned from OpenAI pic func, then send photo+text
                bot.send_photo(message.chat.id, image_url, caption=answer, parse_mode="markdown")
            else:  # if no picture send only text
                bot.send_message(message.chat.id, answer, parse_mode="markdown")

        else:  # if False returned form openAI text func
            bot.send_message(message.chat.id, 'Сорри йа, что-то пошло не так, попробуйте еще разок...')

    else:
        bot.send_message(message.chat.id, "Введите слово или фразу на английском языке и не более 45 символов")  # if message to long or not only EN symbols send - send error


bot.polling()