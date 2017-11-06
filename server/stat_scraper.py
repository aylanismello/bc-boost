from selenium import webdriver
from IPython import embed
import time
import csv
import re
import os

class StatScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        # self.soundcloud()
        self.instagram()

    def write_to_csv(self, service, service_stats):
        with open(f"{os.getcwd()}/server/data/{service}.csv", 'a+') as csv_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(csv_file)
            for old_row in reader:
                writer.writerow(old_row)
            if service == 'soundcloud':
                new_row = [
                    time.strftime(f"{service}_%m/%d/%Y-%H:%M"),
                    service_stats['followers_count'],
                    service_stats['followings_count'],
                    service_stats['total_plays'],
                    service_stats['last_week_plays'],
                    service_stats['today_plays'],
                    service_stats['track_count']
                ]
            elif service == 'instagram':
                new_row = [
                    time.strftime(f"{service}_%m/%d/%Y-%H:%M"),
                    service_stats['followers_count'],
                    service_stats['followings_count'],
                    service_stats['post_count']
                ]
            writer.writerow(new_row)

    def get_value_from_key(self, key, html):
        result = re.search(f'\d+\n{re.escape(key)}', html).group(0)
        result = re.search('\d+', result).group(0)
        return result

    def instagram(self):
        stats = {}
        self.driver.get('https://instagram.com/burncartel')
        html = self.driver.find_element_by_xpath('//body').text
        # followers_count = self.get_value_from_key('followers_count', response.text)
        # result = re.search(f'{re.escape(key)}":\d+', html).group(0)
        # result = re.search('\d+', result).group(0)

        # embed()
        # embed()
        stats['post_count'] = self.get_value_from_key('posts', html)
        stats['followers_count'] = self.get_value_from_key('followers', html)
        stats['followings_count'] = self.get_value_from_key('following', html)
        # stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span')
        # stats['followings_count'] = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a/span')
        # stats['post_count'] = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[1]/span/span')
        # stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span')
        # stats['followings_count'] = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[3]/a/span')
        for k, v in stats.items():
            stats[k] = v.replace(',', '')

        self.write_to_csv('instagram', stats)

    def soundcloud(self):
        stats = {}
        self.driver.get('https://soundcloud.com')
        login_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[3]/button[1]')
        login_button.click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//form//div//input').send_keys('burncartel')
        time.sleep(1)
        self.driver.find_elements_by_css_selector('.signinForm__checkIdentifierCTA')[0].click()
        time.sleep(1)
        self.driver.find_element_by_name('password').send_keys(os.environ['BC_PASSWORD'])


        self.driver.find_elements_by_css_selector('.signinWithPassword > button')[0].click()

        time.sleep(1)
        self.driver.get('https://soundcloud.com/burncartel')
        stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[1]/a/div')
        stats['followings_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[2]/a/div')
        stats['last_week_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[2]')
        stats['today_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[1]')
        stats['total_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/p/strong')
        stats['track_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[3]/a/div')

        for k, v in stats.items():
            stats[k] = v.text.replace(',', '')

        self.write_to_csv('soundcloud', stats)
