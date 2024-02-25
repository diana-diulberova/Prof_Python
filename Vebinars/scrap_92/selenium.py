from urllib.parse import urlencode, urljoin

from selenium.webdriver import ActionChains, Chrome, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def wait_element(browser, delay_seconds=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


base_url = "https://yandex.ru/search/"
qs = {
    "text": "что нибудь",
    "search_source": "dzen_desktop_safe",
    "lr": "21159",
    "src": "suggest_Recs",
}
url = urljoin(base_url, f"?{urlencode(qs)}")  # строим url с параметрами поиска

path = ChromeDriverManager().install()
browser_service = Service(executable_path=path)
service = Service(executable_path=path)
browser = Chrome(service=service)

browser.get(url) # открываем страницу
wait_element(browser, 5, By.ID, "search-result") # ждем пока загрузится результат поиска
li_tags = browser.find_elements(
    By.XPATH, '//*[@id="search-result"]/li[@class="serp-item serp-item_card "]'
)  # ищем все элементы списка результатов поиска

# https://bugbug.io/xpath-selector-builder/ поможет составить xpath


for li in li_tags:
    span = li.find_element(By.TAG_NAME, "span")
    a = li.find_element(By.TAG_NAME, "a")

    text = span.text
    link = a.get_attribute("href")
    print(text, link)


next_page_xpath = '//div[@class="Pager-ListItem Pager-ListItem_type_next"]'

next_page = browser.find_element(By.XPATH, next_page_xpath) # низ страницы

ActionChains(browser).scroll_to_element(next_page).perform()  # прокрутка до конца страницы
