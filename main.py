from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions as EC
from urllib.parse import quote

with open("queries.txt", "r") as f:
    content=f.read()
    queries=content.split("\n")

i_agree_xpath="/html/body/div[3]/div[3]/span/div/div/div/div[3]/button[2]/div"
result_stats_selector="#result-stats"
title_child_of_regular_result_link_selector="h3"
title_child_of_ad_result_link_selector="span"


chrome_path=ChromeDriverManager().install()
print(chrome_path)

driver=webdriver.Chrome(executable_path=chrome_path)
driver.get("https://google.com/search?q=accept GDPR")
WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, i_agree_xpath)))
element=driver.find_element(by=By.XPATH, value=i_agree_xpath)
element.click()

for query in queries:
    driver.get("https://google.com/search?q="+quote(query))
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, result_stats_selector)))
    link_elements=driver.find_elements(by=By.CSS_SELECTOR, value="a[href]")
    for element in link_elements:
        link = element.get_attribute("href")
        if "google.com" not in link and "google.de" not in link and not link.startswith("/"):
            print(link)
            try:
                title_element = element.find_element(by=By.CSS_SELECTOR, value=title_child_of_regular_result_link_selector)
            except NoSuchElementException:
                title_element = element.find_element(by=By.CSS_SELECTOR, value=title_child_of_ad_result_link_selector)
            print(title_element.text)
            break

    sleep(5)


sleep(100000)

