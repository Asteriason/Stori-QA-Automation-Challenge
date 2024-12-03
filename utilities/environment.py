from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_browser():
    """
    Sets up the Selenium WebDriver with Chrome.
    Returns the WebDriver instance.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open browser in full screen
    chrome_options.add_argument("--disable-notifications")  # Disable browser notifications
    chrome_options.add_argument("--incognito")  # Open browser in incognito mode
    chrome_options.add_argument("--disable-infobars")  # Disable 'Chrome is being controlled by automated test software'

    # Initialize WebDriver with WebDriver Manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def teardown_browser(driver):
    """
    Tears down the WebDriver instance.
    """
    if driver:
        driver.quit()
