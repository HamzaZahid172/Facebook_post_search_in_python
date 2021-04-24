import warnings
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from selenium.common.exceptions import NoSuchElementException 


chromedriver_path = r'/home/hamza/Desktop/Selenium_project/chromedriver_linux64/chromedriver'
EMAIL = '-----'
PASSWORD = '-------'
keywords_list = ["Highmark Stadium"]
#, "BlueShield", "Highmark", "BlueCross", "Highmark Stadium", "BCBSWNY", "Healthnow", "Bills Stadium"


warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
wait = WebDriverWait(driver, 10)

driver.get('https://m.facebook.com/login/')

(wait.until(EC.presence_of_element_located((By.ID, 'm_login_email')))).send_keys(EMAIL)
time.sleep(3)
(wait.until(EC.presence_of_element_located((By.ID, 'm_login_password')))).send_keys(PASSWORD)
time.sleep(3)
(wait.until(EC.presence_of_element_located((By.NAME, 'login')))).click()
time.sleep(5)
driver.get('https://m.facebook.com/login/save-device/cancel/?flow=interstitial_nux_retry&nux_source=regular_login')

data = []
def check_detail_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output.text
    except NoSuchElementException:
        return " "

def check_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output.text
    except NoSuchElementException:
        return "0"

def check_post_emotion_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        return output
    except NoSuchElementException:
        return " "


def check_emotion_exists_by_css(driver,css_selector):
    try:
        output = driver.find_element_by_css_selector(css_selector)
        check_output = driver.find_element_by_css_selector(str(css_selector) + '>span[class="_14va"]').text
        if len(check_output) <= 0:
            return "0"
        else:
            return output
    except NoSuchElementException:
        return "0"


for key in keywords_list:
    time.sleep(2)
    u = 'https://m.facebook.com/search/posts/?q='+ key.replace(' ', '%20')

    driver.get(u)
    posts = []
    for i in range(0,1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.findAll('a', {'class': '_15kq _77li _l-a'})
        print(len(posts))

    for post in posts[:1]:
        post_url = "https://m.facebook.com"+ post['href']
        driver.get('https://m.facebook.com' + post['href'])
        comments_exact = []
        comment_exact_reply = []
        for i in range(0, 1):
            time.sleep(4)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(2)
            post_time = check_detail_exists_by_css(driver,'div[class="_52jc _5qc4 _78cz _24u0 _36xo"] abbr')
            post_des = check_detail_exists_by_css(driver,'div[class="_5rgt _5nk5"]')
            if post_des == " ":
                post_des = check_detail_exists_by_css(driver,'div[class="msg"]')
            emotion_result_post = check_post_emotion_exists_by_css(driver,'a[class="_45m8"]')
            emotion_result_post.click()
            time.sleep(10)
            count_like_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Like"]>span')
            count_love_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Love"]>span')
            count_care_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Care"]>span')
            count_haha_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Haha"]>span')
            count_sad_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Sad"]>span')
            count_angry_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Angry"]>span')
            count_wow_post = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Wow"]>span')
            time.sleep(3)
            driver.find_element_by_css_selector('a[class="_6j_c"]').click()
            time.sleep(6)
            
            comments = soup.findAll('div', {'class': '_2b06'})
            comments_exact.extend(comments)
            if len(comments) == 1:
                ass = soup.find('a', {'class': '_108_'}).get('href')
            else:
                break
            comment_url = 'https://m.facebook.com' + str(ass)
            driver.get('https://m.facebook.com' + ass)
            print(comment_url)
            #print(comments_exact)
        reply_exist = []
        for x in range(len(comments_exact)):
            com_reply = check_post_emotion_exists_by_css(driver,'div[class="_333v _45kb"]>div:nth-child('+ str(x+1) +') div[class="_2a_m"] div[data-sigil*="replies"]>a')
            
            if com_reply != " ":
                com_reply.click()
                reply_exist.append('Yes')
            else:
                reply_exist.append('No')
            time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        comment_reply = soup.findAll('div', { 'class' : '_2b1k' })
        comment_exact_reply.extend(comment_reply)
        print(comment_exact_reply)
        print(len(comment_exact_reply))
        print(comments_exact)
        print(len(comments_exact))
        x=1
        for comment,reply_num in zip(comments_exact,range(len(reply_exist))):
            comment_time = check_detail_exists_by_css(driver,'div[class="_333v _45kb"]>div:nth-child('+ str(x) +') div[data-sigil="ufi-inline-comment-actions"]>abbr')
            emotion_result_comment = check_emotion_exists_by_css(driver,'div[class="_333v _45kb"]>div:nth-child('+ str(x) +')>div[class="_2b04"]>div:nth-child(1)>a')
            if emotion_result_comment != '0':
                time.sleep(2)
                emotion_result_comment.click()
                time.sleep(10)
                count_like_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Like"]>span')
                count_love_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Love"]>span')
                count_care_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Care"]>span')
                count_haha_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Haha"]>span')
                count_sad_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Sad"]>span')
                count_angry_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Angry"]>span')
                count_wow_comment = check_exists_by_css(driver,'div[class="scrollAreaColumn"] span[aria-label*="Wow"]>span')
                time.sleep(3)
                driver.find_element_by_css_selector('a[class="_6j_c"]').click()
                time.sleep(6)
            else:
                count_like_comment = " "
                count_love_comment = " "
                count_care_comment = " "
                count_haha_comment = " "
                count_sad_comment = " "
                count_angry_comment = " "
                count_wow_comment = " "
            d = {}
            d['url'] = u
            d['post_url'] = post_url
            d['post_des'] = post_des
            d['keyword'] = key
            d['comment'] = comment.findAll('div')[1].text
            if(reply_exist[reply_num] == 'yes'):
                d['comment_reply'] = comment_reply.findAll('div','data-sigil="comment-body"')[1].text
            else:
                d['comment_reply'] = ""
            d['post_time'] = post_time
            d['post_like'] = count_like_post
            d['post_love'] = count_love_post
            d['post_care'] = count_care_post
            d['post_haha'] = count_haha_post
            d['post_sad'] = count_sad_post
            d['post_angry'] = count_angry_post
            d['post_wow'] = count_wow_post
            d['comment_time'] = comment_time
            d['comment_like'] = count_like_comment
            d['comment_love'] = count_love_comment
            d['comment_care'] = count_care_comment
            d['comment_haha'] = count_haha_comment
            d['comment_sad'] = count_sad_comment
            d['comment_angry'] = count_angry_comment
            d['comment_wow'] = count_wow_comment
            data.append(d)
            print(d)
            x = x+1
            
    print(data)
    df = pd.DataFrame(data)
    df.to_csv('fb_comments_1.csv')
