import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

s = requests.Session()

r = s.post("https://mobile.twitter.com/sessions",data={"":""},headers=headers)
r = s.get("https://mobile.twitter.com/sessions")

soup = BeautifulSoup(r.content,"html5lib")
token = soup.find("input",{"name":"authenticity_token"}).get("value")

data = {
    "session[username_or_email]": "",
    "session[password]": "",
    "remember_me": "1",
    "wfa": "1",
    "authenticity_token": token
}


r = s.post("https://mobile.twitter.com/sessions",data=data,headers=headers)
r = s.get("https://mobile.twitter.com/messages")

soup = BeautifulSoup(r.content,"html5lib")

return s
