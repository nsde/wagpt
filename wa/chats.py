import time
import time
import emoji
import requests
import selenium
import pyperclip

from PIL import ImageGrab, Image
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import utils

class WAChat:
    """Represents a chat. If no name is given, the current chat is used."""

    def __init__(self, driver, name: str=None):
        self.driver = driver

        if name and (self.name != name): # If the current chat is not the chat we want to open
            chat_name_elements = self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['chat_names_in_sidebar'])

            for element in chat_name_elements:
                if element.text == name:
                    element.click()
                    break

        if self.is_open:
            utils.wait_for(self.driver, utils.SELECT['message_input'], 3)

    @property
    def is_open(self):
        """Returns True if the chat is open"""
        return bool(self.name)

    @property
    def name(self):
        """Current chat name"""

        try:
            return self.driver.find_element(By.CSS_SELECTOR, utils.SELECT['current_chat_name']).text
        except selenium.common.exceptions.NoSuchElementException:
            return None

    @property
    def count_messages_sent(self) -> int:
        """Returns amount of sent messages in the current chat"""

        sel = utils.SELECT['delivered']

        try:
            utils.wait_for(self.driver, sel, 2)
            return len(self.driver.find_elements(By.CSS_SELECTOR, sel))

        except TimeoutError:
            return 0

    @property
    def message_count(self) -> bool:
        """Returns the amount of messages in the current chat"""

        try:
            utils.wait_for(self.driver, utils.SELECT['message_text'], 2)
        except TimeoutError:
            return 0

        return len(self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['message_text']))

    @property
    def last_message(self) -> str:
        """Returns the last message in the current chat"""

        utils.wait_for(self.driver, utils.SELECT['message_text'])

        messages_texts = self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['message_text'])
        return messages_texts[-1].text

    @property
    def last_message_id(self) -> str:
        """Returns the id of the last message in the current chat"""

        messages = self.driver.find_elements(By.CSS_SELECTOR, utils.SELECT['message'])
        utils.wait_for(self.driver, utils.SELECT['message'], 2)

        for message in reversed(messages):
            if message.get_attribute('data-id').startswith('false_'):
                return message.get_attribute('data-id')

    def _fallback_send_message(self, element, message_text: str) -> None:
        for char in message_text:
            if emoji.emoji_count(char): # is an emoji
                emoji_unicode = emoji.demojize(char)[:-1]

                for char in emoji_unicode:
                    element.send_keys(char)
                time.sleep(0.1)
                element.send_keys(Keys.TAB)
                time.sleep(0.1)

            else:
                element.send_keys(char)

    def send_message(self, message_text: str) -> None:
        """Sends a message to the current chat"""

        if not message_text:
            return

        old_amount_of_sent_messages = self.count_messages_sent

        element = self.driver.find_element(By.CSS_SELECTOR, utils.SELECT['message_input'])
        utils.wait_for(self.driver, utils.SELECT['message_input'], 3)

        try:
            pyperclip.copy(message_text)
        except pyperclip.PyperclipWindowsException as exc: # exception is raised when the PC is locked (https://github.com/asweigart/pyperclip/issues/119#issuecomment-572159273)
            if 'success' in str(exc): # not actually success, but it's the only way to check if the exception is raised because the PC is locked
                self._fallback_send_message(element, message_text)
        else:
            element.send_keys(Keys.CONTROL, 'v')
            element.send_keys(Keys.ENTER)

        for _ in range(500):
            if self.count_messages_sent > old_amount_of_sent_messages:
                break
            else:
                time.sleep(0.1)
        else:
            raise TimeoutError('Message was not sent.')

    def send_image(self, image):
        """Downloads an image and sends it to the current chat"""
        raise NotImplementedError

        assert '://' in image, 'Image must be a URL'

        resp = requests.get(image, stream=True, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        requests.raise_for_status()


        temp_image_path = 'temp.png'

        with open('temp.png', 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)

            image = Image.open(image_path)

        # Create a BytesIO object to hold the image data
        image_data = io.BytesIO()
        image.save(image_data, format='PNG')  # Save the image as PNG format in the BytesIO object
