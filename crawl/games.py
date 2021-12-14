from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from pandas import DataFrame
from tqdm import tqdm
import time
import csv

START_YEAR = 2002
NUM_YEAR = 20
NUM_LOAD_PER_REQUEST = 10


def initialFetch():
    driver = webdriver.Safari()
    driver.get("http://m.baduk.or.kr/record/C01_list.asp#none")

    for i in range(NUM_YEAR):
        # Fill out form values
        select = Select(driver.find_element_by_id("s_yyyy"))
        select.select_by_visible_text(str(START_YEAR - i) + " 년")

        select = Select(driver.find_element_by_id("s_win_appy_yn"))
        select.select_by_visible_text("공식")

        button = driver.find_element_by_id("btn_search").click()

        # Wait for tables to update
        time.sleep(1)

        # Total rows to crawl
        total = driver.find_element_by_id("lblTotal")
        total = int(total.text.replace(",", ""))

        # Current count
        count = len(driver.find_elements_by_class_name("winner"))

        pbar = tqdm(total=total)
        winners = []
        losers = []
        while count <= total:
            button = driver.find_element_by_id("AddList")
            button.click()

            # Wait for new rows to be added
            WebDriverWait(driver, 10).until(lambda browser: len(
                browser.find_elements_by_class_name("winner")) > count)

            count += NUM_LOAD_PER_REQUEST
            pbar.update(NUM_LOAD_PER_REQUEST)
        pbar.close()

        elems = driver.find_elements_by_class_name("tb-date")
        dates = [elem.text for elem in elems]

        elems = driver.find_elements_by_class_name("winner")
        winners = [elem.text for elem in elems]

        elems = driver.find_elements_by_class_name("loser")
        losers = [elem.text for elem in elems]

        data = []
        for j in range(len(dates)):
            data.append([dates[j], winners[j], losers[j]])
        games_df = DataFrame(data, columns=["date", "winner", "loser"])

        games_df.to_csv("../data/{}_games.csv".format(START_YEAR-i),
                        index=False,
                        encoding="utf-8-sig",
                        quotechar='"',
                        quoting=csv.QUOTE_ALL,)

        driver.refresh()

    driver.close()


if __name__ == "__main__":
    initialFetch()
