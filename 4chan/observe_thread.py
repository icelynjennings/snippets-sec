import threading
import logging
from itertools import islice
import time

format = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('example')
logging.basicConfig(filename='logs.txt',format=format,level=logging.INFO)

class observe_thread(threading.Thread):
    def __init__(self, Thread, search_terms, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.search_terms = search_terms
        self.Thread = Thread
        self.last_checked_post = 0
    def run(self):
        """ Periodically updates a 4chan thread, notifying of any new replies containing search terms. """   

        while (not self.Thread.closed):
            for p in islice(self.Thread.all_posts, self.last_checked_post, None):            
                try:
                    subject = p.subject.lower()
                except:
                    subject = ""
                full_post = subject + ' ' + p.text_comment
                match = any(x in (full_post) for x in self.search_terms)
                
                if match:
                    newpost_notification = "Post found: {}".format(str(p.semantic_url))   
                    logger.info(newpost_notification)
                    print newpost_notification         

            self.last_checked_post = len(self.Thread.all_posts)
    
            with self.lock:
                num_new_replies = self.Thread.update()
                time.sleep(1)

        closedthread_notification = "Thread closed: {}".format(str(t.op.semantic_url)) 
        logger.info(closedthread_notification)
