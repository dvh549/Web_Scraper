from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def get_nft_title(driver, URL):
    class_name = 'proRanks_name__Y0IKE'
    driver.get(URL)
    time.sleep(5)
    nfts = driver.find_elements(By.CLASS_NAME, class_name)
    nft_titles = [title.text for title in nfts if title.text != ""]
    return nft_titles

if __name__ == "__main__":
    driver = get_driver()
    URL = "https://www.flips.finance/"
    print(get_nft_title(driver, URL))
    driver.quit()