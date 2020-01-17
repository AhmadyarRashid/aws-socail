from selenium import webdriver
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import dateutil.parser

def getPostData(url, driver):
    url = 'https://www.instagram.com' + url
    driver.get(url)
    more_buttons_inner = driver.find_elements_by_class_name("moreLink")
    for x in range(len(more_buttons_inner)):
        if more_buttons_inner[x].is_displayed():
            driver.execute_script("arguments[0].click();", more_buttons_inner[x])
            time.sleep(1)
    page_source_inner = driver.page_source
    modalPage = BeautifulSoup(page_source_inner, 'html.parser')

    comments = modalPage.find_all('ul', attrs={"class": "Mr508"})
    # print('comments = ', len(comments))

    nested_comments = modalPage.find_all('div', attrs={"class": "ZyFrc"})
    # print('nested comment = ', len(nested_comments))

    likes = modalPage.find('button', attrs={"class": "sqdOP yWX7d _8A5w5"})
    viewers = modalPage.find('span', attrs={'class': 'vcOH2'})

    if likes != None:
        likes = likes.span.text
    elif viewers != None:
        likes = viewers.span.text
    else:
        likes = 0
    # print('likes = ', likes)

    posted_time = modalPage.find('time', attrs={"class": "_1o9PC Nzb55"})['datetime']
    simple_date = modalPage.find('time', attrs={"class": "_1o9PC Nzb55"})['title']
    exist_time = modalPage.find('time', attrs={"class": "_1o9PC Nzb55"}).text
    time_array = exist_time.split(' ')

    dateTimeSplit = posted_time.split('T');
    date = dateTimeSplit[0]
    time = dateTimeSplit[1].split('.')[0]
    # print('split date -----', posted_time, date, time)
    date_format = date + ' ' + time
    # print('proper format -----', date_format)
    insertion_date = dateutil.parser.parse(date_format)
    time_between_insertion = datetime.now() - insertion_date
    # print('posted date = ', posted_time, simple_date, time_array)

    if time_between_insertion.days > 30:
        # print("The insertion date is older than 30 days")
        return None
    else:
        # print("The insertion date is not older than 30 days")
        return {
            "likes": likes,
            "comments": len(comments),
            "posted_time": posted_time,
            "posted_date": simple_date
        }


def main(url, driver):
    driver.get(url)
    more_buttons = driver.find_elements_by_class_name("moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
            driver.execute_script("arguments[0].click();", more_buttons[x])
            time.sleep(1)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    data = {}
    title = soup.find('h1', attrs={"class": "_7UhW9 fKFbl yUEEX KV-D4 fDxYl"})
    data['username'] = title.text
    a = soup.find_all('span', attrs={'class': 'g47SY'})
    data['total_post'] = a[0].text
    data['total_followers'] = a[1].text
    data['total_followings'] = a[2].text

    avatar_0 = soup.find('img', attrs={'class': 'be6sR'})
    avatar_1 = soup.find('img', attrs={'class': '_6q-tv'})
    if avatar_0 != None:
        data['avatar'] = avatar_0['src']
    elif avatar_1 != None:
        data['avatar'] = avatar_1['src']
    else:
        data['avatar'] = 'Some thing went wrong'

    list_of_post = [main.a for main in soup.find_all('div', attrs={'class': 'v1Nh3 kIKUG _bz0w'})]

    post_details = []
    for post in list_of_post:
        details = getPostData(post['href'], driver)
        # print('--- details ----' , details)
        if details == None:
            break
        else:
            post_details.append(details)

    data['post_details'] = post_details
    print(data)
    # driver.quit()
    return data

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
#
# driver = webdriver.Chrome("./chromedriver", chrome_options=options)
#
# url = "https://www.instagram.com/ewokfn/"
# main(url, driver)
