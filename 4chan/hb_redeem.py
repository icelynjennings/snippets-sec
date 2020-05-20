import urllib
import re
import argparse
import time
import threading

success_gift_url_strings = ['gift-thanks']
used_gift_url_strings = ['used-gift']
bad_gift_url_strings = ['badgift','badkey']

lock = threading.Lock()

class humble_thread (threading.Thread):
    def __init__(self, email, giftId):
        threading.Thread.__init__(self)
        self.email = email
        self.giftId = giftId
    def run(self):
        with lock:
            redeem(self.email, self.giftId)
            time.sleep(1)

def redeem(email, giftId):
    
    humblebundle_url = 'https://www.humblebundle.com/gift/' + giftId

    # POST to redeem gift
    params = urllib.urlencode( {'email': email[0], 'subscribe': 'false' } )
    
    htmlfile = urllib.urlopen(humblebundle_url, params)        
    finalurl = htmlfile.geturl()

    # TODO more possible cases
    if any(x in finalurl for x in success_gift_url_strings):
        result = "Success."
    elif any(x in finalurl for x in used_gift_url_strings):
        result = "FAIL - used gift."
    elif any(x in finalurl for x in bad_gift_url_strings):
        result = "FAIL - invalid key."
    else:
        result = "FAIL - unknown failure."

    print('[{}] {}').format(giftId,result)
    return 0
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Redeems humble bundle gifts.')
    parser.add_argument('email', help='email address to redeem gifts to.', nargs=1)
    parser.add_argument('urls', help='humblebundle gift url(s) or id(s).',nargs='+')
    args = parser.parse_args()



    pattern_gift_id = re.compile('(?:)((?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{16})')

    
    threads = []
    
    for url in args.urls:

        giftId = re.search(pattern_gift_id,url)
        if (giftId):

            thread = humble_thread(args.email,giftId.group(0))
            thread.start()
            threads.append(thread)
        else:
            print url + " - Invalid gift."

    for t in threads:
        t.join()
