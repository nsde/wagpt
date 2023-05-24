import os
import openai

from dotenv import load_dotenv

import system
import config

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

if os.getenv('OPENAI_API_BASE'):
    openai.api_base = os.getenv('OPENAI_API_BASE')

def answer(input_message: str, user: str) -> str:
    """Uses AI to answer an message."""

    ai_config = config.read('ai')

    try:
        conversation = system.prepare_ai_chat(input_message, user)
        completion = openai.ChatCompletion.create(
            model=system.MODEL,
            messages=conversation,
            temperature=ai_config['temperature'],
            max_tokens=ai_config['max_tokens'],
            presence_penalty=ai_config['presence_penalty'],
            frequency_penalty=ai_config['frequency_penalty']
        )

    except Exception as exc:
        error_msg = str(exc)

        if 'sk-' in error_msg:
            error_msg = 'Invalid API key. Please check your .env file. If you\'re not the developer, please contact them.'

        return f'*Error:* ```{error_msg}```'

    response = completion.choices[0].message.content

    system.add_to_log({
        'role': 'user',
        'content': input_message,
    }, user)
    system.add_to_log({
        'role': 'assistant',
        'content': response,
    }, user)

    return response
