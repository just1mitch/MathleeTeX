import unittest
import sys
from os import path, makedirs
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# https://googlechromelabs.github.io/chrome-for-testing/

# Test the Home Page functionality
class TestHomePage(unittest.TestCase):

    def setUp(self) -> None:
        # Create driver and set config
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")

    # Make sure home page is reachable
    def test_reach_homepage(self):
        driver = self.driver
        self.assertEqual(driver.current_url, 'http://127.0.0.1:5000/', "Home page not reached.")
        driver.quit()
        
    # Test Start Quiz redirect
    def test_start_button(self):
        driver = self.driver
        button = driver.find_element(By.ID, 'startPlay')
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        sleep(0.5) # Wait for webpage to change
        self.assertEqual(driver.current_url, 'http://127.0.0.1:5000/play', "Start Button does not lead to play page.")
        driver.quit()
    
    # Test Homepage Leaderboard redirect
    def test_leaderboard_button(self):
        driver = self.driver
        driver.execute_script("document.getElementById('footer').style.display = 'none';")
        button = driver.find_element(By.ID, 'startLeaderboard')
        button.click()
        sleep(0.5) # Wait for webpage to change
        self.assertEqual(driver.current_url, 'http://127.0.0.1:5000/leaderboard', "Leaderboard Button does not lead to leaderboard page.")
        driver.quit()

class TestHeaderLinks(unittest.TestCase):
    def setUp(self) -> None:
        # Create driver and set config
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5000/")

    # Test all header links to make sure they reach the correct link
    def test_header_links(self):
        driver = self.driver
        buttons = driver.find_elements(By.CLASS_NAME, 'nav-item')
        links = []
        for button in buttons:
            link = button.find_element(By.TAG_NAME, 'a')
            text = link.text
            href = link.get_attribute('href')
            links.append((text, href))

        for text, href in links:
            driver.get(href)
            sleep(0.5)
            if text != 'askQuestion':
                self.assertEqual(driver.current_url, href, f"Button for {text} does not lead to link {href}")
            else:
                # Create link should redirect to login page with 'next' set to create so when user logs in they redirect back to create
                self.assertEqual(driver.current_url, "http://127.0.0.1:5000/login?next=%2Fcreate", f"Button for {text} does not lead to link {href}")
            driver.get("http://127.0.0.1:5000/")



def main(out = sys.stderr, verbosity=2):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity).run(suite)

if __name__ == '__main__':
    # https://www.geeksforgeeks.org/python-logging-test-output-to-a-file/
    # For sending the test outputs to a logfile
    dirname = path.dirname(__file__)
    dirpath = path.join(dirname, 'logs')
    makedirs(dirpath, exist_ok=True)
    filepath = path.join(dirpath, 'chrome.txt')
    
    with open(filepath, 'w+', encoding='utf-8') as logfile:
        main(logfile)
