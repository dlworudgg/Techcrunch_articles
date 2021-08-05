
import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_articles(n = 1000):
    url = "https://techcrunch.com/startups/"
    # option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    # driver = webdriver.Chrome('chromedriver 3', options=option)
    driver = webdriver.Chrome('chromedriver 3')

    driver.get(url)
    driver.implicitly_wait(15)

    article_link = []
    pause_time = 4

    while True:
        article_number = len(article_link)

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(pause_time)


        # driver.find_element_by_class_name("load-more").click()

        load_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "load-more")))

        load_button.click()

        article_link = [x.get_attribute('href') for x in driver.find_elements_by_class_name("post-block__title__link")
                        if "Extra Crunch" not in x.find_element_by_xpath('../..').text]
        driver.implicitly_wait(pause_time)

        if len(article_link) > n:
            break

        else:
            print(article_number)

    print("Finished Collecting Article Links")

    article_df_list = []
    author_df_list = []
    for link in tqdm(article_link):
        driver.get(link)
        title_object = driver.find_element_by_class_name("article__title")
        title = title_object.text

        article_content = driver.find_element_by_class_name("article-content")
        text_p = article_content.find_elements_by_xpath('./p')
        text = ' '.join([p.text for p in text_p])

        article_info_object = driver.find_element_by_class_name("article__byline")

        try :
            writer = article_info_object.find_element_by_xpath('./a').text
        except :
            try :
                writer_span = article_info_object.find_elements_by_xpath('./span')
                writer = ', '.join([span.a.text for span in writer_span])
            except :
                writer = "None"

        try:
            account =  article_info_object.find_element_by_xpath('./span/a').text
            account_link =  article_info_object.find_element_by_xpath('./span/a').get_attribute('href')
        except :
            account = "None"
            account_link = "None"
        datetime =  article_info_object.find_element_by_xpath('./span/time').get_attribute('datetime')

        article_row = {"Title" : title, "Link" : link , "author" : writer, "time" : datetime, "text" : text}
        author_row = {"author" : writer, "account" : account, "account_link" : account_link}

        article_df_list.append(article_row)
        author_df_list.append(author_row)

    driver.quit()

    article_df = pd.DataFrame(article_df_list)
    author_df = pd.DataFrame(author_df_list).drop_duplicates().reset_index(drop = True)


    return article_df, author_df