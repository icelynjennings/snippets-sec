import requests


def download_file(url, filepath):
    r = requests.get(url)
    with open(filepath, 'wb') as f:
        f.write(r.content)
