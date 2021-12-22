from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import configurations as conf
import time
import sqlite3
import contextlib
import os


class Job:
    def __init__(self, location: str, db='properties.db', interval='1'):
        if not self._check_if_db_exist(db):
            self._create_db(db)
        self.db = db
        self._scrape(location, db)



    def _check_if_db_exist(self, db):
        if os.path.exists(db):
            return True
        else:
            return False

    def _create_db(self, db):
        with contextlib.closing(sqlite3.connect(db)) as con:  # auto-closes
            with con:  # auto-commits
                cur = con.cursor()
                cur.execute(conf.QUERY_CREATE_TABLE)
                con.commit()

    def _scrape(self, location,  to_csv: [False, True] = False):
        scraper = Scraper(location, db=self.db)




class Scraper:
    def __init__(self, location: str,  to_csv: [False, True] = True, db=None):
        self._get_location(location)
        self._get_url()
        if db:
            self._connect_to_db(db)
        self._get_data()

        if to_csv:
            self._to_csv()

    def _get_data(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        for i in range(conf.HOW_MANY_SCROLL_DOWN):
            driver.execute_script(f"window.scrollBy(0, {conf.HOW_MANY_PIXELS_SCROLL_DOWN})", "")
            time.sleep(conf.SLEEPING_TIME_BETWEEN_SCROLL)
        delay = 30
        self.results = pd.DataFrame()
        try:
            found_class_name = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                                  "tableRow")))
        except TimeoutException:
            return
        rows = bs(driver.page_source, 'lxml').findAll('div', {'class': 'tableRow'})
        for row in rows:
            columns = row.findAll('div', {'class': ['', 'link']})
            col_index = 0
            row_result = {}
            for column in columns:
                row_result[conf.COLUMNS[col_index]] = column.text.strip()
                col_index += 1
            row_result['location'] = self.loction.replace("%20", "_")
            self.results = self.results.append(row_result, ignore_index=True)
        try:
            self.results = self.results.drop('Change', axis=1)
        except KeyError:
            pass
        str_data = [str(e) for e in list(self.results.itertuples(index=False, name=None))]
        query = conf.INSERT_DATA.format(conf.TABLE_NAME,
                                                         tuple(conf.COLUMNS_TO_INSERT),
                                                         ','.join(str_data))

        self.connection.cursor().execute(query)
        self.connection.commit()

    def _to_csv(self):
        self.results.to_csv(f'result_{self.loction.replace("%20", "_")}.csv', index=False, encoding='utf-8-sig')

    def _get_url(self):
        self.url = conf.BASE_URL + '?search=%20' + self.loction

    def _get_location(self, location):
        self.loction = location.replace(' ', '%20')


    def _connect_to_db(self, db):
        self.connection = sqlite3.connect(db)




if __name__ == "__main__":
    Job('תל-אביב')
    Job('הרצליה פיתוח')
    Job('הרצליה')
    Job('חולון')





