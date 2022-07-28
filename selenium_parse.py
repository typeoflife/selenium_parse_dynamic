from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import time


def get_data_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    s = Service('chromedriver.exe')

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(service=s, options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    driver.get(url)

    #Прокручиваем страницы до посделней
    scroll_pause_time = 3

    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")

        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            print("break")
            break
        last_height = new_height

    # Находим нужные блоки и отфильтровываем только бесплатные обьявления
    blocks = driver.find_element(By.CLASS_NAME, "native")
    items = blocks.find_elements(By.XPATH,
                                 "//tr[@class='bull-item bull-item_inline -exact bull-item bull-item_inline']")

    items_list = []
    for item in items:
        temp_list = []
        try:
            item.find_element(By.CLASS_NAME, "bull-image-container").find_element(By.TAG_NAME, "i")
        except NoSuchElementException:
            href = item.find_element(By.CLASS_NAME, "bull-item-content__subject-container"). \
                find_element(By.TAG_NAME, "a").get_attribute("href")
            text = item.find_element(By.CLASS_NAME, "bull-item-content__subject-container"). \
                find_element(By.TAG_NAME, "a").text
            temp_list.append(href)
            temp_list.append(text)
            try:
                price = item.find_element(By.CLASS_NAME, "price-block__price").text
                temp_list.append(price)
            except NoSuchElementException:
                temp_list.append('Нет цены')
            items_list.append(temp_list)

    time.sleep(5)
    driver.quit()
    print(f'Quantity: {len(items_list)} items')
    print(items_list)
    return items_list


if __name__ == '__main__':
    get_data_selenium(
        url="https://www.farpost.ru/vladivostok/tech/computers/notebooks/?condition%5B%5D=used#tab=dopolnitelno")
