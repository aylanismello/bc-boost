from IPython import embed
from selenium import webdriver
import time
import os

soundcloud_stats = {}



driver = webdriver.PhantomJS()
driver.get('https://soundcloud.com')
login_button = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/div/div/div[3]/button[1]')
login_button.click()
time.sleep(1)
driver.find_element_by_xpath('//form//div//input').send_keys('burncartel')
time.sleep(1)
driver.find_elements_by_css_selector('.signinForm__checkIdentifierCTA')[0].click()
time.sleep(1)
driver.find_element_by_name('password').send_keys(os.environ['BC_PASSWORD'])


driver.find_elements_by_css_selector('.signinWithPassword > button')[0].click()

time.sleep(1)
driver.get('https://soundcloud.com/burncartel')
soundcloud_stats['today_plays'] = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[1]')
soundcloud_stats['last_week_plays'] = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/table/tbody/tr[2]/td[2]')
soundcloud_stats['total_plays'] = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/article[2]/div/div/p/strong')
soundcloud_stats['followers_count'] = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[1]/a/div')
soundcloud_stats['track_count'] = driver.find_element_by_xpath('//*[@id="content"]/div/div[5]/div[2]/div/article[1]/table/tbody/tr/td[3]/a/div')


with open(f'{os.getcwd()}/server/data/soundcloud.csv', 'w+') as f:
    for k, v in soundcloud_stats.items():
        f.write(v.text.replace(',', ''))


# do this to all of the numbers we bring back
# total_plays.replace(',', '')
