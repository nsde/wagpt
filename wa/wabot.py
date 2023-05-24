"""WA Selenium Script"""

import time
import selenium.webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from rich import print
from dotenv import load_dotenv

import chats
import utils
import config

load_dotenv()

class WABot:
    """WA Selenium Bot"""

    def __init__(self) -> None:
        """Prepares the driver"""

        print('[bold green]Welcome to WABot! Starting...[/bold green]')
        browser_config = config.read('browser')
        print(browser_config)

        # main options
        options = FirefoxOptions()
        
        if browser_config['headless']:
            options.add_argument('--headless')

        options.binary_location = browser_config['firefox']['binary'].replace('\\', '\\')

        # stay logged in
        firefox_profile = selenium.webdriver.FirefoxProfile(browser_config['firefox']['profile'].replace('\\', '\\'))

        print('[green]WA Selenium Bot is starting...[/green]')

        self.driver = selenium.webdriver.Firefox(
            firefox_profile=firefox_profile,
            executable_path=browser_config['firefox']['driver'].replace('\\', '\\'),
            options=options
        )

        print('[bold green]WA Selenium Bot started![/bold green]')

        self.driver.get(config.read('whatsapp')['url'])

        utils.wait_for(self.driver, utils.SELECT['sidebar'], 20)

        print('[bold green]WA Selenium Bot is ready![/bold green]')

    @property
    def list_chat_names(self) -> list:
        """Returns a list of chat names"""

        chat_names = self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['chat_names_in_sidebar'])
        return [chat.text for chat in chat_names]

    def check_for_message_from_other_chat(self) -> bool:
        """Opens the chat if there is a new message in another chat."""

        chat_elements = self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['sidebar_chat'])

        for element in chat_elements:
            if element.find_elements(By.CSS_SELECTOR, '[data-testid="icon-unread-count"]'):
                element.click()
                time.sleep(1)
                return True

        return False

    def wait_for_new_message(self):
        """Waits and returns a new message in the current chat or in other chats"""

        last_message_id = None
        chat = chats.WAChat(self.driver)
        if chat.is_open:
            last_message_id = chat.last_message_id

        while True:
            time.sleep(0.1)

            if self.check_for_message_from_other_chat():
                break

            chat = chats.WAChat(self.driver)
            if chat.is_open:
                if not last_message_id:
                    last_message_id = chat.last_message_id

                if chat.last_message_id != last_message_id:
                    break

        chat = chats.WAChat(self.driver)
        return {
            'chat': chat.name,
            'text': chat.last_message,
            'id': chat.last_message_id
        }

    def send(self, message: str, channel: str=None):
        """Sends a message to the current chat"""

        if channel:
            chats.WAChat(self.driver, channel).send_message(message)
        else:
            chats.WAChat(self.driver).send_message(message)

    # let's make a decorator available for receiving messages. optionally, we can pass a channel name
    # and the decorator will only receive messages from that channel

    def on_message(self, func, channel: str=None):
        """Decorator for receiving messages"""

        if channel:
            while True:
                message = self.wait_for_new_message()

                if message['chat'] == channel:
                    func(message)
        else:
            while True:
                func(self.wait_for_new_message())

if __name__ == '__main__':
    wa_bot = WABot()

    while True:
        msg = wa_bot.wait_for_new_message()
        print(msg)
        chats.WAChat(wa_bot.driver, msg['chat']).send_message(msg['text'])
