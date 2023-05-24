"""Helpers for other modules."""

import selenium.common.exceptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config

SELECT = config.read('whatsapp')['selectors']

def wait_for(driver, css_selector: str, timeout: int=5):
    """Waits for an element to appear"""

    element_visible = EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))

    try:
        WebDriverWait(driver, timeout).until(element_visible)
    except selenium.common.exceptions.TimeoutException as exc:
        raise TimeoutError(f'Element {css_selector} loading timed out.') from exc
