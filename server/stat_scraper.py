from selenium import webdriver
import time
import csv
import os

class StatScraper(object):
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.soundcloud()

    def write_to_csv(self, service, service_stats):
        with open(f"{os.getcwd()}/server/data/{service}.csv", 'a+') as csv_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(csv_file)
            for old_row in reader:
                writer.writerow(old_row)

            new_row = [
                time.strftime(f"{service}_%m/%d/%Y-%H:%M"),
                service_stats['followers_count'],
                service_stats['total_plays'],
                service_stats['last_week_plays'],
                service_stats['today_plays'],
                service_stats['track_count']
            ]
            writer.writerow(new_row)

    def soundcloud(self):
        soundcloud_stats = {}
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
        soundcloud_stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[1]/a/div')
        soundcloud_stats['last_week_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[2]')
        soundcloud_stats['today_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[1]')
        soundcloud_stats['total_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/p/strong')
        soundcloud_stats['track_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[3]/a/div')

        for k, v in soundcloud_stats.items():
            soundcloud_stats[k] = v.text.replace(',', '')

        self.write_to_csv('soundcloud', soundcloud_stats)
