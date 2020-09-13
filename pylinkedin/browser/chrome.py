from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import random as r

def get_instance(headless=True) -> webdriver:
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage'); # overcome limited resource problems
    options.add_argument('--no-sandbox'); # Bypass OS security model
    
    if headless:
        options.add_argument('--headless')
    
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=options)