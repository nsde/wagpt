import nltk

import ai
import sys
import wabot
import atexit
import signal

bot = wabot.WABot()

@bot.on_message
def receive(message):
    """Receives a message and sends an answer."""

    resp = ai.answer(message['text'], message['chat'])

    sentences = nltk.sent_tokenize(resp) # split the response into sentences

    for sentence in sentences:
        if sentence.endswith('.'):
            sentence = sentence[:-1]

        bot.send(sentence.strip().lower(), message['chat'])

def cleanup():
    bot.driver.quit()
    print('Bye!')

def handle_interrupt(*args, **kwargs):
    cleanup()
    sys.exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGINT, handle_interrupt)
