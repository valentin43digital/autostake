import time
import math
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from settings import account_address

# asset apy tvl link график на dexscreener ссылкой и ссылку на маркетплейс типа yieldwolf


class Element:
    def __init__(self, type, value, content):
        self.type = type
        self.value = value
        self.content = content

    def wait(self, _driver):
        element_loaded = False
        while not element_loaded:
            try:
                if self.type == "CLASS_NAME":
                    for element in _driver.find_elements(by=By.CLASS_NAME, value=self.value):
                        if element.text.startswith(self.content):
                            element_loaded = True
                elif self.type == "TAG_NAME":
                    for element in _driver.find_elements(by=By.TAG_NAME, value=self.value):
                        if element.text.startswith(self.content):
                            element_loaded = True
            except Exception as ex:
                pass
            finally:
                time.sleep(1)


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
        executable_path="C:\\Solidity\\autostake\\chromedriver\\chromedriver.exe",
        options=options)
    return _driver


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
    buttons = _driver.find_elements(by=By.TAG_NAME, value="button")
    _submit_button = None
    for button in buttons:
        if button.text.strip().lower() == "search pools":
            _submit_button = button
    return _inputs, _submit_button


def get_pools(**kwargs):
    """
    Search pools by filters
    :param kwargs: token1, token2, min_apy, max_apy, min_tvl, max_tvl
    :return: _results
    """
    url = "https://www.yieldstation.net/pools"
    try:
        driver = get_driver()
        driver.get(url=url)
        element = Element("TAG_NAME", "h1", "Pools Info")
        element.wait(driver)
        # WebDriverWait(driver=driver, timeout=5).until(document_initialised(driver))
        # get inputs
        inputs, submit_button = get_inputs(_driver=driver)

        # entering numbers
        for key, value in kwargs.items():
            inputs[key].clear()
            inputs[key].send_keys(value)
        submit_button.click()
        element = Element("CLASS_NAME", "v-data-footer__pagination", "1-25")
        element.wait(driver)

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
            element = Element("TAG_NAME", "td", str(1+i*25))
            element.wait(driver)
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
                    pass
            i += 1
            if i < pages_number:
                next_page_button.click()
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return result


def get_balance(farms):
    """
    Gets balance from current pools
    :param farms: list of current farms
    :return:
    """
    driver = get_driver()
    page = get_account_page(_driver=driver, farms=farms)
    balance = parse_account_page(page)
    return balance


def get_account_page(_driver, farms):
    url = "https://www.yieldstation.net/v2/account/portfolio"
    _driver.get(url=url)
    try:
        element = Element("CLASS_NAME", "inline-block", "Enter your")
        element.wait(_driver)
        address_input = _driver.find_element(by=By.CLASS_NAME, value="p-inputtext")
        address_input.clear()
        address_input.send_keys(account_address)
        pools = _driver.find_elements(by=By.CLASS_NAME, value="logoLext")
        for pool in pools:
            if pool.text == farms:
                pool.click()
        enter_button = _driver.find_element(by=By.CLASS_NAME, value="enter-button")
        enter_button.click()
    except Exception as ex:
        print(ex)
    finally:
        #print("Page is loaded")
        return _driver
    pass


def parse_account_page(page):
    _balance = []
    element = Element("CLASS_NAME", "p-paginator", "Showing")
    element.wait(page)
    try:
        rows = page.find_elements(by=By.TAG_NAME, value="tr")
        for row in rows:
            try:
                elements = row.find_elements(by=By.TAG_NAME, value="td")
                _balance.append({
                    "Asset": elements[4].text.strip(),
                    "Amount": elements[5].text.strip(),
                    "Total": elements[8].text.strip(),
                    "APY": elements[9].text.strip()
                })
            except Exception as ex:
                print(ex)
    except Exception as ex:
        print(ex)
    finally:
        page.close()
        page.quit()
        return _balance


if __name__ == "__main__":
    # driver = 0
    # get_pools(_driver=driver, min_apy=1000, min_tvl=10)

    # Read searching options
    min_apy = 1000
    min_tvl = 10
    #page = get_account_page(driver)
    #balance = parse_account_page(page)
    #print(balance)

    pools = get_pools(min_apy=min_apy, min_tvl=min_tvl)
    print("Pools =", len(pools))
    print(pools)
