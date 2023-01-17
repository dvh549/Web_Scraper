from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def get_driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def get_nft_name(driver):
    class_name = 'proRanks_name__Y0IKE'
    nfts = driver.find_elements(By.CLASS_NAME, class_name)
    nft_names = [name.text for name in nfts if name.text != ""]
    print("Titles retrieved!", len(nft_names))
    return nft_names

def get_nft_volume(driver):
    volume = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[4]')
    nft_vols = [v.text for v in volume if v.text != ""]
    print("Volume retrieved!", len(nft_vols))
    return nft_vols

def get_nft_sales(driver):
    sales = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[5]')
    nft_sales = [sale.text for sale in sales if sale.text != ""]
    print("Sales retrieved!", len(nft_sales))
    return nft_sales

def get_nft_floor(driver):
    floor = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[6]')
    nft_floor = [f.text for f in floor if f.text != ""]
    print("Floor retrieved!", len(nft_floor))
    return nft_floor

def get_nft_floor_change(driver):
    floor_change = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[7]')
    nft_floor_change = [fc.text for fc in floor_change if fc.text != ""]
    print("Floor change retrieved!", len(nft_floor_change))
    return nft_floor_change

def get_nft_supply(driver):
    supply = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[8]')
    nft_supply = [s.text for s in supply if s.text != ""]
    print("Owners / Supply retrieved!", len(nft_supply))
    return nft_supply

def get_nft_owner_change(driver):
    owner_change = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[9]')
    nft_owner_change = [oc.text for oc in owner_change if oc.text != ""]
    print("Owner change retrieved!", len(nft_owner_change))
    return nft_owner_change

def get_nft_perc_listed(driver):
    perc_listed = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[10]')
    nft_perc_listed = [pl.text for pl in perc_listed if pl.text != ""]
    print("% listed retrieved!", len(nft_perc_listed))
    return nft_perc_listed

def get_nft_list_change_perc(driver):
    list_change_perc = driver.find_elements(By.XPATH, '//tr[@class="proRanks_rankTableRow__IEn18"]/td[12]/div')
    nft_list_change_perc = [lcp.text for lcp in list_change_perc if lcp.text != ""]
    print("List change % retrieved!", len(nft_list_change_perc))
    return nft_list_change_perc

def get_marketplace_data(driver):
    marketplace_names, volume, traders, sale_count = [], [], [], []
    class_name = 'marketMetrics_left__zxAfj'
    names = driver.find_elements(By.CLASS_NAME, class_name)
    for i in range(1, len(names)):
        name = names[i]
        if name.text != "":
            marketplace_names.append(name.text)
    print("Marketplace names retrieved!", len(marketplace_names))

    class_name = "marketMetrics_table2___NxYa"
    marketplace_table = driver.find_elements(By.CLASS_NAME, class_name)
    rows = marketplace_table[0].find_elements(By.TAG_NAME, "tr")
    for j in range(2, len(rows)):
        row = rows[j]
        volume.append(row.find_elements(By.TAG_NAME, "td")[3].text)
        traders.append(row.find_elements(By.TAG_NAME, "td")[4].text)
        sale_count.append(row.find_elements(By.TAG_NAME, "td")[5].text)
    
    print("Other data retrieved", len(volume), len(traders), len(sale_count))
    compiled_dict = {
        "Name": marketplace_names,
        "Vol USD": volume,
        "Traders": traders,
        "Sale Count": sale_count
    }
    return pd.DataFrame(compiled_dict)

def compiler(driver):
    compiled_dict = {
        "Name": get_nft_name(driver),
        "Volume": get_nft_volume(driver),
        "Sales": get_nft_sales(driver),
        "Floor": get_nft_floor(driver),
        "Floor Change": get_nft_floor_change(driver),
        "Owners / Supply": get_nft_supply(driver),
        "Owners Change": get_nft_owner_change(driver),
        "% Listed": get_nft_perc_listed(driver),
        "List Change %": get_nft_list_change_perc(driver)
    }
    return pd.DataFrame(compiled_dict)

if __name__ == "__main__":
    driver, URL = get_driver(), "https://www.flips.finance/"
    driver.get(URL)
    time.sleep(5)
    # nft_df = compiler(driver)
    # nft_df.to_csv("data/NFT Rankings.csv", index=False)
    marketplace_df = get_marketplace_data(driver)
    marketplace_df.to_csv("data/Marketplace Leaderboard.csv", index=False)
    driver.quit()