"""System module for logs, prompts, configs,... for the AI."""

import os
import yaml
import datetime

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv('OPENAI_MODEL') or 'gpt-3.5-turbo'

def read_log(user: str) -> list:
    """Returns the log for a user."""

    if os.path.exists(f'conversations/{user}.yml'):
        with open(f'conversations/{user}.yml', 'r', encoding='utf8') as log_file:
            return yaml.load(log_file, Loader=yaml.FullLoader)

    return []

def add_to_log(content: dict, user: str) -> None:
    """Adds a message to the log of a user."""

    assert content['role'] in ['user', 'system', 'assistant'], 'Invalid AI conversation role'

    if os.path.exists(f'conversations/{user}.yml'):
        with open(f'conversations/{user}.yml', 'r', encoding='utf8') as log_file:
            log = yaml.load(log_file, Loader=yaml.FullLoader)
    else:
        log = []

    log.append(content)

    with open(f'conversations/{user}.yml', 'w', encoding='utf8') as log_file:
        yaml.dump(log, log_file)

def prepare_ai_chat(input_message: str, user: str) -> list:
    """Returns messages which can be used to prompt the AI."""

    assert input_message, 'Input message cannot be empty'

    base_vars = {
        'USER': user,
        'MODEL': MODEL,
        'TIME': datetime.datetime.now().strftime('%H:%M'),
        'DATE': datetime.datetime.now().strftime('%d/%m/%Y'),
        'DAY': datetime.datetime.now().strftime('%A')
    }

    # the base conversation is the same for all users.
    # it outlines the AI's personality and how it should respond to certain messages.
    with open('config/base-conversation.yml', 'r', encoding='utf8') as conv_file:
        conv_str = conv_file.read()
    
        for k, v in base_vars.items():
            conv_str = conv_str.replace(f'{k}', v)

        conversation = yaml.load(conv_str, Loader=yaml.FullLoader)

    # if the user has already had a conversation with the AI, add it to the conversation
    # so it can have context for the next message
    conversation.extend(read_log(user))

    # add the user's (new) message to the conversation
    conversation.append({
        'role': 'user',
        'content': input_message,
    })

    # now this can be passed to the AI
    return conversation
