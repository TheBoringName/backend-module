"""
Created on Thu Jul 14 14:06:01 2022

@author: freelon
"""


from bs4 import BeautifulSoup
import json
import re
import requests
import dill

headers = {'Accept-Encoding': 'gzip, deflate, sdch',
           'Accept-Language': 'en-US,en;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive'}
url_regex = '(?<=\.com/)(.+?)(?=\?|$)'
runsb_err = 'No browser defined for cookie extraction. We strongly recommend you run \'specify_browser\', which takes as its sole argument a string representing a browser installed on your system, e.g. "chrome," "firefox," "edge," etc.'


def get_tiktok_json(video_url):
    global cookies
    with open('functions/tiktok_lib/cookies.pkl', 'rb') as file:
        cookies = dill.load(file)

    tt = requests.get(video_url,
                      headers=headers,
                      cookies=cookies,
                      timeout=20)
    cookies = tt.cookies
    soup = BeautifulSoup(tt.text, "html.parser")
    tt_script = soup.find('script', attrs={'id':"__UNIVERSAL_DATA_FOR_REHYDRATION__"})
    try:
        tt_json = json.loads(tt_script.string)
    except AttributeError:
        return
    return tt_json

def save_tiktok(video_url):
    global cookies
    with open('functions/tiktok_lib/cookies.pkl', 'rb') as file:
        cookies = dill.load(file)

    tt_json = get_tiktok_json(video_url)
    regex_url = re.findall(url_regex, video_url)[0]
    video_fn = regex_url.replace('/', '_') + '.mp4'
    tt_video_url = tt_json["__DEFAULT_SCOPE__"]['webapp.video-detail']['itemInfo']['itemStruct']['video']['downloadAddr']
    headers['referer'] = 'https://www.tiktok.com/'
    # include cookies with the video request
    tt_video = requests.get(tt_video_url, allow_redirects=True, headers=headers, cookies=cookies)
    with open(video_fn, 'wb') as fn:
            fn.write(tt_video.content)