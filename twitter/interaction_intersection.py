from bs4 import BeautifulSoup
from pprint import pprint
import time

from selenium import webdriver
driver = webdriver.Firefox()

def get_domain(url):
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain


def intersection(first, *others):
    return set(first).intersection(*others)


all_users = []
tweets = []

for tweet in tweets:
    domain = get_domain(tweet)

    if not "mobile" in domain:
        tweet = tweet.replace("twitter.com","mobile.twitter.com")

    furl = tweet + "/retweets"
    print furl
    driver.get(furl)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source,"html5lib")
    users = [i.find("a",role="link")["href"] for i in soup.find_all("div",{"data-testid":"UserCell"})]
    all_users.append(set(users))

inter = set.intersection(*all_users)

pprint(inter)

driver.quit()
