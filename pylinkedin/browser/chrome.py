from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import random as r
import itertools
import time

def get_instance(headless=True) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage'); # overcome limited resource problems
    options.add_argument('--no-sandbox'); # Bypass OS security model
    
    if headless:
        options.add_argument('--headless')
    
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)


def scroll_down(driver):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')


def scroll_down_bottom(driver, scroll_increment=300, timeout=10):
    expandable_button_selectors = [
        'button[aria-expanded="false"].pv-skills-section__additional-skills',
        'button[aria-expanded="false"].pv-profile-section__see-more-inline',
        'button[aria-expanded="false"].pv-top-card-section__summary-toggle-button',
        'button[data-control-name="contact_see_more"]'
    ]

    current_height = 0

    while True:
        for name in expandable_button_selectors:
            try:
                driver.find_element_by_css_selector(name).click()
            except Exception as e:
                # print(f'WARNING: Something wrong but OK with message: {str(e)}')
                pass

        # Use JQuery to click on invisible expandable 'see more...' elements
        driver.execute_script('document.querySelectorAll(".lt-line-clamp__ellipsis:not(.lt-line-clamp__ellipsis--dummy) .lt-line-clamp__more").forEach(el => el.click())')

        # Scroll down to bottom
        new_height = driver.execute_script('return Math.min({}, document.body.scrollHeight)'.format(current_height + scroll_increment))
        if (new_height == current_height):
            break
        driver.execute_script('window.scrollTo(0, Math.min({}, document.body.scrollHeight));'.format(new_height))
        current_height = new_height

        # Wait to load page
        time.sleep(r.randrange(start=0, stop=30, step=1) / 1000)


def browse(driver, element_id) -> webdriver:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))

    for _ in itertools.repeat(object=None, times=3):
        scroll_down(driver)
        time.sleep(r.randrange(start=30, stop=100, step=1) / 100)

    scroll_down_bottom(driver)

def get_page_source(driver) -> str:
    return driver.page_source