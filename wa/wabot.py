"""WhatsApp Selenium Script"""

import os
import bs4
import time
import selenium.webdriver
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

SELECT = {
    'sidebar': '#pane-side',
    'current_chat_name': '._21nHd > span:nth-child(1)',
    'chat_names_in_sidebar': '._21S-L span',
    'sidebar_chat': '._8nE1Y',
    'message_input': '._3Uu1_ > div:nth-child(1) > div:nth-child(1)',
    'message': '._21Ahp>span[dir="ltr"]>span',
    'delivered': 'span[aria-label=" Delivered "]',
}

# USER_DATA_DIR = r'C:\Users\User\AppData\Local\Google\Chrome\User Data\Default'.replace('User', os.getlogin())

CONFIG = {
    'firefox_driver': r'C:\Users\Lynx\Documents\Apps\selenium\geckodriver.exe',
    'firefox_profile': r'C:\\Users\\Lynx\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\zi5uozpw.default-release'
}

class WhatsAppBot:
    """WhatsApp Selenium Bot"""

    def __init__(self) -> None:
        """Prepares the driver"""

        options = FirefoxOptions()
        #options.add_argument('--headless')
        # options.add_argument(f'--user-data-dir={USER_DATA_DIR}')
        options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

        # stay logged in
        options.add_argument(f'--user-data-dir={CONFIG["firefox_profile"]}')
        options.add_argument('--profile-directory=Default')

        # make it undetectable
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')

        firefox_profile = selenium.webdriver.FirefoxProfile(CONFIG['firefox_profile'])

        self.driver = selenium.webdriver.Firefox(firefox_profile=firefox_profile, executable_path=CONFIG['firefox_driver'], options=options)
        self.driver.get('https://web.whatsapp.com')

        self.wait_for(SELECT['sidebar'], 20)

    def wait_for(self, css_selector: str, timeout: int=5):
        """Waits for an element to appear"""

        element_visible = EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))

        try:
            WebDriverWait(self.driver, timeout).until(element_visible)
        except selenium.common.exceptions.TimeoutException as exc:
            raise TimeoutError(f'Element {css_selector} loading timed out.') from exc

    @property
    def chats(self) -> list:
        """Returns a list of chat names"""

        soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        return [chat.text for chat in soup.select(SELECT['chat_names_in_sidebar'])]

    def open_chat(self, chat: str) -> None:
        """Sets the current chat"""

        chat_name_elements = self.driver.find_elements(By.CSS_SELECTOR, SELECT['chat_names_in_sidebar'])

        for element in chat_name_elements:
            if element.text == chat:
                element.click()
                break

        self.wait_for(SELECT['message_input'], 3)

    def send_message(self, message: str) -> None:
        """Sends a message to the current chat"""

        if not message:
            return

        old_amount_of_sent_messages = self.sent_messages

        element = self.driver.find_element(By.CSS_SELECTOR, SELECT['message_input'])
        element.send_keys(message)

        time.sleep(0.1)
        element.send_keys(Keys.ENTER)

        for _ in range(500):
            if self.sent_messages > old_amount_of_sent_messages:
                break
            else:
                time.sleep(0.1)
        else:
            raise TimeoutError('Message was not sent.')

    def send_message_to(self, chat: str, message: str) -> None:
        """Sends a message to a chat"""

        self.open_chat(chat)
        self.send_message(message)

    def check_for_message_from_other_chat(self) -> bool:
        """Opens the chat if there is a new message in another chat."""

        chat_elements = self.driver.find_elements(By.CSS_SELECTOR, SELECT['sidebar_chat'])

        for element in chat_elements:
            if element.find_elements(By.CSS_SELECTOR, '[data-testid="icon-unread-count"]'):
                element.click()
                return True

        return False

    @property
    def message_count(self) -> bool:
        """Returns the amount of messages in the current chat"""

        try:
            self.wait_for(SELECT['message'], 1)
        except TimeoutError:
            return 0

        return len(self.driver.find_elements(By.CSS_SELECTOR, SELECT['message']))

    @property
    def last_message(self) -> str:
        """Returns the last message in the current chat"""

        self.wait_for(SELECT['message'])

        messages = self.driver.find_elements(By.CSS_SELECTOR, SELECT['message'])
        return messages[-1].text

    def wait_for_new_message(self) -> str:
        """Waits and returns a new message in the current chat or in other chats"""

        while True:
            old_amount_of_messages = self.message_count
            time.sleep(0.1)

            if not self.check_for_message_from_other_chat():
                print('no new message in other chats')
                amount_of_messages = self.message_count

                if amount_of_messages > old_amount_of_messages:
                    break
            else:
                break

        print('new message')
        return self.last_message

class Chat:
    def __init__(self, bot: WhatsAppBot):
        self.bot = bot
        self.driver = bot.driver

    @property
    def name(self):
        """Current chat name"""
        return self.bot.driver.find_element_by_css_selector(SELECT['current_chat_name']).text

    @property
    def count_messages_sent(self) -> int:
        """Returns amount of sent messages in the current chat"""

        soup = bs4.BeautifulSoup(self.driver.page_source, 'html.parser')
        return len(soup.select(SELECT['delivered']))


if __name__ == '__main__':
    bot = WhatsAppBot()

    while True:
        print(bot.wait_for_new_message())

    # send_message_to('AaNewNumber', 'diese nachricht habe ich mit python gesendet lel')

    time.sleep(999999)
