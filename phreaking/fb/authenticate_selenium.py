import requests
import re
from bs4 import BeautifulSoup


def session():   
    s = requests.Session()
    r = s.get('https://www.facebook.com/', allow_redirects=False)
    soup = BeautifulSoup(r.text)
    
    # Handle login form
    action_url = soup.find('form', id='login_form')['action']
    inputs = soup.find('form', id='login_form').findAll('input', {'type': ['hidden', 'submit']})
    post_data = {input.get('name'): input.get('value')  for input in inputs}
    post_data['email'] = email
    post_data['pass'] = password.upper()

    # Find and save the 'datr' cookie
    scripts = soup.findAll('script')
    scripts_string = '/n/'.join([script.text for script in scripts])
    datr_search = re.search('\["_js_datr","([^"]*)"', scripts_string, re.DOTALL)
    if datr_search:
        datr = datr_search.group(1)
        cookies = {'_js_datr' : datr}
    else:
        return False
    s.post(action_url, data=post_data, cookies=cookies, allow_redirects=False)
    return s