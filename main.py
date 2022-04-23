# import requests
import time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
# asset apy tvl link график на dexscreener ссылкой и ссылку на маркетплейс типа yieldwolf


def get_driver():
    """
    Inits driver with user-agent
    :return: driver ready to open page
    """
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/100.0.4896.127 Safari/537.36"
    }
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={headers['User-Agent']}")
    _driver = webdriver.Chrome(
        executable_path="C:\\Projects\\autostake\\chromedriver\\chromedriver.exe",
        options=options)
    return _driver


def document_initialised(_driver):
    return _driver.execute_script("return initialised")


def get_inputs(_driver):
    """

    :param _driver: webdriver
    :return: _inputs, _submit_button
    """
    data = _driver.find_elements(by=By.CLASS_NAME, value="v-text-field__slot")
    _inputs = {
        "token1": data[0].find_element(By.TAG_NAME, 'input'),
        "token2": data[1].find_element(By.TAG_NAME, 'input'),
        "min_apy": data[2].find_element(By.TAG_NAME, 'input'),
        "max_apy": data[3].find_element(By.TAG_NAME, 'input'),
        "min_tvl": data[4].find_element(By.TAG_NAME, 'input'),
        "max_tvl": data[5].find_element(By.TAG_NAME, 'input')
    }
    buttons = driver.find_elements(by=By.TAG_NAME, value="button")
    _submit_button = None
    for button in buttons:
        if button.text.strip().lower() == "search pools":
            _submit_button = button
    return _inputs, _submit_button


def get_pools(_driver, **kwargs):
    """
    Search pools by filters
    :param _driver: webdriver
    :param kwargs: token1, token2, min_apy, max_apy, min_tvl, max_tvl
    :return: _results
    """
    url = "https://www.yieldstation.net/pools"
    try:
        driver.get(url=url)
        time.sleep(6)
        # WebDriverWait(driver=driver, timeout=5).until(document_initialised(driver))

        # get inputs
        inputs, submit_button = get_inputs(_driver=driver)

        # entering numbers
        for key, value in kwargs.items():
            inputs[key].clear()
            inputs[key].send_keys(value)
        time.sleep(1)
        submit_button.click()

        # waiting for page loading
        time.sleep(10)

        # pagination
        result_number = int(driver.find_element(by=By.CLASS_NAME, value="v-data-footer__pagination").text.split()[-1])
        pages_number = math.ceil(result_number/25)
        print("pages =", pages_number)
        if pages_number > 1:
            next_page_button = driver.find_elements(by=By.CLASS_NAME, value="v-pagination__navigation")[1]

        # saving results
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
            if i < pages_number:
                next_page_button.click()
                time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return result


if __name__ == "__main__":
    # driver = 0
    # get_pools(_driver=driver, min_apy=1000, min_tvl=10)

    # Read searching options
    min_apy = 1000
    min_tvl = 10

    # Init driver and open web page
    driver = get_driver()
    pools = get_pools(_driver=driver, min_apy=min_apy, min_tvl=min_tvl)
    print("Pools =", len(pools))
    print(pools)
