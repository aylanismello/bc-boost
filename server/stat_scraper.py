from IPython import embed
import boto3
import time
import csv
import re
import os
import constants
from selenium import webdriver
import selenium

class StatScraper(object):
    def __init__(self, handle):
        self.handle = handle
        self.max_sleep = int(os.environ['MAX_SLEEP_TIME'] or 3)
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.PhantomJS()
        self.soundcloud()
        self.instagram()
        self.facebook()
        self.twitter()
        self.write_to_s3()


    def write_to_s3(self):
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.environ['aws_access_key_id'],
            aws_secret_access_key=os.environ['aws_secret_access_key']
        )

        for service in ['soundcloud', 'twitter', 'instagram', 'facebook']:
            with open(f'{os.getcwd()}/server/data/{self.handle}/{service}.csv', 'rb') as data:
                s3.upload_fileobj(data, 'burn-cartel-content', f'{self.handle}/{service}.csv')

    def write_to_csv(self, service, service_stats):
        with open(f"{os.getcwd()}/server/data/{self.handle}/{service}.csv", 'a+') as csv_file:
            reader = csv.reader(csv_file)
            writer = csv.writer(csv_file)

            if len(list(reader)) == 0:
                writer.writerow(constants.SERVICE_COLUMNS[service])

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
            elif service == 'instagram' or service == 'twitter':
                new_row = [
                    time.strftime(f"{service}_%m/%d/%Y-%H:%M"),
                    service_stats['followers_count'],
                    service_stats['followings_count'],
                    service_stats['post_count']
                ]
            elif service == 'facebook':
                new_row = [
                    time.strftime(f"{service}_%m/%d/%Y-%H:%M"),
                    service_stats['followers_count'],
                    service_stats['likes_count']
                ]
            writer.writerow(new_row)

    def get_insta_val(self, key, html):
        # handle both phatom + chrome?
        result = re.search(f'\d+[\n ]{re.escape(key)}', html).group(0)


        # PHANTOM:
        # result = re.search(f'\d+\n{re.escape(key)}', html).group(0)
        # in Chrome the \n becomes a space
        # result = re.search(f'\d+ {re.escape(key)}', html).group(0)
        result = re.search('\d+', result).group(0)
        return result

    def get_fb_val(self, key, html):
        result = re.search(f'\d+ people {re.escape(key)} this', html).group(0)
        result = re.search('\d+', result).group(0)
        return result

    def facebook(self):
        print('scraping facebook stats')
        stats = {}
        self.driver.get(f'https://facebook.com/{self.handle}')
        time.sleep(self.max_sleep)
        html = self.driver.find_element_by_xpath('//body').text
        stats['likes_count'] = self.get_fb_val('like', html)
        stats['followers_count'] = self.get_fb_val('follow', html)
        self.write_to_csv('facebook', stats)

    def twitter(self):
        print('scraping twitter stats')
        stats = {}
        self.driver.get(f'https://twitter.com/{self.handle}')
        time.sleep(self.max_sleep)

        stats['post_count'] = self.driver.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul/li[1]/a/span[3]')
        stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul/li[3]/a/span[3]')
        stats['followings_count'] = self.driver.find_element_by_xpath('//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/ul/li[2]/a/span[3]')

        for k, v in stats.items():
            stats[k] = v.text.replace(',', '')
        self.write_to_csv('twitter', stats)


    def instagram(self):
        print('scraping instagram stats')
        stats = {}
        self.driver.get(f'https://instagram.com/{self.handle}')
        time.sleep(self.max_sleep)
        html = self.driver.find_element_by_xpath('//body').text
        stats['post_count'] = self.get_insta_val('posts', html)
        stats['followers_count'] = self.get_insta_val('followers', html)
        stats['followings_count'] = self.get_insta_val('following', html)

        for k, v in stats.items():
            stats[k] = v.replace(',', '')

        self.write_to_csv('instagram', stats)


    def catch_soundcloud_error(self, e):
        self.max_sleep += 1
        print(e)
        print(f'messed up trying to scraping Selenium stuff, doubling sleep time to {self.max_sleep}')
        self.soundcloud()


    def soundcloud(self):
        print('scraping soundcloud stats')
        stats = {}
        self.driver.get('https://soundcloud.com')
        time.sleep(self.max_sleep)
        login_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[3]/button[1]')
        login_button.click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//form//div//input').send_keys(self.handle)
        time.sleep(1)
        self.driver.find_elements_by_css_selector('.signinForm__checkIdentifierCTA')[0].click()
        time.sleep(3)

        try:
            self.driver.find_element_by_name('password').send_keys(os.environ['BC_PASSWORD'])
        except Exception as e:
            self.catch_soundcloud_error(e)


        self.driver.find_elements_by_css_selector('.signinWithPassword > button')[0].click()

        time.sleep(1)
        self.driver.get(f'https://soundcloud.com/{self.handle}')
        time.sleep(self.max_sleep)
        try:
            stats['followers_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[1]/a/div')
            stats['followings_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[2]/a/div')
            stats['last_week_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[2]')
            stats['today_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[1]')
            stats['total_plays'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/p/strong')
            stats['track_count'] = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[3]/a/div')
        except selenium.common.exceptions.NoSuchElementException as e:
            self.catch_soundcloud_error(e)

        for k, v in stats.items():
            stats[k] = v.text.replace(',', '')

        self.write_to_csv('soundcloud', stats)
