import os
import openai

import wabot

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_base = os.getenv('OPENAI_API_BASE')

def answer(message: str) -> str:
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'system',
                # Often use the emojis 🗿 and 💀 at the of your sentences. 
                'content': 'Your name is ChadGPT, also called "Giga Chad". Answer in a cool, slang way and use emojis. Be friendly and have opinions. Be humorous and use memes. Be informal and subjective.'
            },
            {
                'role': 'user',
                'content': 'yo wassup'
            },
            {
                'role': 'assistant',
                'content': 'What\'s good my homie? 🗿'
            },
            {
                'role': 'user',
                'content': message
            }
    ]
    )

    return completion.choices[0].message.content

if __name__ == '__main__':
    bot = wabot.WhatsAppBot()

    while True:
        message = bot.wait_for_new_message()
        bot.send_message(message)
        # bot.send_message(answer(message))
