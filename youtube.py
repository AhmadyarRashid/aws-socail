from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
from datetime import date, datetime
from selenium.webdriver.common.keys import Keys
from html5lib import html5parser

list_of_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def monthDiff(d1, d2):
    d1Y = d1.year
    d2Y = d2.year
    d1M = d1.month
    d2M = d2.month

    return (d2M + 12 * d2Y) - (d1M + 12 * d1Y)

def videoDetail(url, driver):
    url = 'https://www.youtube.com' + url
    driver.get(url)
    # driver.execute_script("window.scrollTo(0, 1000);")
    # delay = 3  # seconds
    # try:
    #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    #     print("Page is ready!")
    # except TimeoutException:
    #     print("Loading took too much time!")

    page_source_inner = driver.page_source
    vpage = BeautifulSoup(page_source_inner, 'html.parser')

    viewer = vpage.find('span', attrs={"class": "view-count style-scope yt-view-count-renderer"}).text
    print('----- viewer ----------' , viewer)

    likes = vpage.find('yt-formatted-string', attrs={"class": "style-scope ytd-toggle-button-renderer style-text"})['aria-label']
    print('---- like ------------' , likes)

    dislikes = vpage.find_all('yt-formatted-string', attrs={"class": "style-scope ytd-toggle-button-renderer style-text"})[1].text
    print('------ dislikes ---------' , dislikes)

    posted_date = vpage.find_all('yt-formatted-string', attrs={'class': 'style-scope ytd-video-primary-info-renderer'})[1].text
    print('------ posted date -----', posted_date)

    comment = vpage.find_all('yt-formatted-string', attrs={'class': 'count-text style-scope ytd-comments-header-renderer'})
    if len(comment) > 0:
        comment = comment[0].text
    else:
        comment = '0 Comments'
    print('------ comments ------' , comment)

    if posted_date.split()[0] in list_of_months:
        post_year = posted_date.split()[2]
        post_month = list_of_months.index(posted_date.split()[0]) + 1
        post_date = posted_date.split()[1][: len(posted_date.split()[1]) - 1]
        posted_d = datetime(int(post_year), int(post_month), int(post_date))
        d = datetime.today()
        diff = monthDiff(posted_d, d)
        print('--------- month diff -----', diff)
        if diff > 1:
            return None
        else:
            return {
                'likes': likes,
                'dislikes': dislikes,
                'comments': comment,
                'viewers': viewer,
                'posted_date': posted_date
            }
    else:
        return {
            'likes': likes,
            'dislikes': dislikes,
            'comments': comment,
            'viewers': viewer,
            'posted_date': posted_date
        }



def uploadPage(url, driver):
    url1 = url + '?view=0&sort=dd&flow=grid'
    # url2 = 'https://www.youtube.com' + url1
    print('---- url is ----' , url1)
    driver.get(url1)
    # driver.execute_script("window.scrollTo(0, 2000);")
    # delay = 3  # seconds
    # try:
    #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    #     print("Page is ready!")
    # except TimeoutException:
    #     print("Loading took too much time!")
    page_source_inner = driver.page_source
    upage = BeautifulSoup(page_source_inner, 'html.parser')

    videos = upage.find_all('ytd-grid-video-renderer', attrs={"class": "style-scope ytd-grid-renderer"})
    # print('----- videos ---' , videos)
    list = []
    for url in videos:
        data = videoDetail(url.a['href'], driver)
        if data == None:
            break
        else:
            list.append(data)
    return list


def main(url, driver):
    driver.get(url)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    data = dict()

    username = soup.find('div', attrs={"class": "style-scope ytd-channel-name"}).text
    print('--- username ---' , username.strip())
    data['userName'] = username.strip()

    subscriber = soup.find('yt-formatted-string', attrs={"id": "subscriber-count"}).text
    # print('--------- subscriber ------', subscriber.strip())
    data['subscriber'] = subscriber.strip()

    avatar = soup.find('img', attrs={'class': 'style-scope yt-img-shadow'})['src']
    data['avatar'] = avatar
    # upload_url = soup.find('a', attrs={"class": "yt-simple-endpoint style-scope ytd-shelf-renderer"})['href']
    # print('--------- url ------', upload_url)
    details = uploadPage(url + '/videos' , driver)

    data['post_list'] = details
    print('---- data ----', data)
    # driver.quit()
    return data


#
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')
# options.add_argument('--lang=en-us')
# options.add_argument('--log-level=3')
#
# driver = webdriver.Chrome("./chromedriver", chrome_options=options)
#
# url = "https://www.youtube.com/channel/UC3DkFux8Iv-aYnTRWzwaiBA"
# main(url, driver)
