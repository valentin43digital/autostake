import requests
import time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

#options
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={headers['User-Agent']}")


url = "https://www.yieldstation.net/pools"

#init driver
driver = webdriver.Chrome(executable_path="C:\\Users\\Valentin\\PycharmProjects\\autostake\\chromedriver\\chromedriver.exe", options=options)

#req = requests.get(url, headers=headers)
#src = req.text
#soup = BeautifulSoup(src, "lxml")


def document_initialised(driver):
    return driver.execute_script("return initialised")





if __name__ == "__main__":
    # Searching options
    min_apy = 1000
    min_tvl = 10

    try:
        driver.get(url=url)
        time.sleep(6)
        #WebDriverWait(driver=driver, timeout=5).until(document_initialised(driver))

        #get inputs
        inputs = driver.find_elements(by=By.CLASS_NAME, value="v-text-field__slot")
        token1_input = inputs[0].find_element(By.TAG_NAME,'input')
        token2_input = inputs[1].find_element(By.TAG_NAME,'input')
        min_apy_input = inputs[2].find_element(By.TAG_NAME,'input')
        max_apy_input = inputs[3].find_element(By.TAG_NAME, 'input')
        min_tvl_input = inputs[4].find_element(By.TAG_NAME, 'input')
        max_tvl_input = inputs[5].find_element(By.TAG_NAME, 'input')
        buttons = driver.find_elements(by=By.TAG_NAME, value="button")
        for button in buttons:
            if button.text.strip().lower() == "search pools":
                search_button = button

        #entering numbers
        min_apy_input.clear()
        min_apy_input.send_keys(min_apy)
        min_tvl_input.clear()
        min_tvl_input.send_keys(min_tvl)
        time.sleep(1)
        search_button.click()
        time.sleep(5)

        #pagination
        result_number = int(driver.find_element(by=By.CLASS_NAME, value="v-data-footer__pagination").text.split()[-1])
        pages_number = math.ceil(result_number/25)
        print("pages =", pages_number)
        if pages_number > 1:
            next_page_button = driver.find_elements(by=By.CLASS_NAME, value="v-pagination__navigation")[1]
        #saving results
        result = []
        i = 0
        while i < pages_number:
            rows = driver.find_elements(by=By.TAG_NAME, value="tr")
            print("rows = ", rows)
            for row in rows:
                try:
                    elements = row.find_elements(by=By.TAG_NAME, value="td")
                    result.append({
                        "Asset": elements[3].text.strip(),
                        "APY": elements[4].text.strip(),
                        "TVL": elements[5].text.strip()
                    })
                except Exception as ex:
                    print(ex)
            i += 1
            if (i < pages_number):
                next_page_button.click()
                time.sleep(5)

        print("Results =", len(result))
        print(result)

        #time.sleep(30)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
