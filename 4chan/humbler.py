import logging
import re
import argparse
import basc_py4chan
import threading
import time
import humble_redeem

class observe_thread(threading.Thread):
    def __init__(self, Thread):
        threading.Thread.__init__(self)
        self.Thread = Thread
        self.last_checked_post = 0
    def run(self):
        """ Observes a 4chan thread, redeeming humble bundle gifts and checking for new replies """   

        while (not self.Thread.closed):
            for i in range (self.last_checked_post,len(self.Thread.all_posts)):

                gift_ids = re.findall(pattern_gift_id,self.Thread.all_posts[i].text_comment)
                for gift_id in gift_ids:
                        humble_redeem.redeem(args.email,gift_id)
                        time.sleep(0.1)

            self.last_checked_post = len(self.Thread.all_posts)
    
            with lock:
                num_new_replies = self.Thread.update()
                time.sleep(1)

        # 404 remove the following 2 lines if stuff fucks up
        print "Observed thread No. " + str(self.Thread.op.post_id) + " has closed. No longer observing."
        observed_thread_ids.remove(self.Thread.op.post_id)
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Searches /v/ for humble bundle gift threads and redeems links posted.')
    parser.add_argument('email', help='email address to redeem gifts to.', nargs=1)
    args = parser.parse_args()

    pattern_gift_id = re.compile('(?:)((?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{16})')

    thread_keywords = ['humble', 'bundle','gift', 'giveaway', 'beg', 'free stuff', 'free games', 'free shit', 'free crap', 'free vidya']
    #thread_keywords = ['hohoho', 'bundle']
    observed_thread_ids = []
    py_threads = []

    lock = threading.Lock()

    board = basc_py4chan.Board('v')

    while 1:
        # Check for new threads every minute
        # Start new threaded parser for threads with keywords

        with lock:
            try:
                #time.sleep(1)
                threads = board.get_all_threads()
                print "Checking for new threads. Threads currently under observation: "
                print str(observed_thread_ids)
            except:
                pass

        for i in range(0, len(threads)):

             try:
                 sub = threads[i].op.subject.lower()
             except:
                 sub = ""
             #if any(x in (threads[i].op.text_comment.lower()) for x in thread_keywords) and threads[i].op.post_id not in observed_thread_ids: # check for keywords in OP
             if any(x in (threads[i].op.text_comment.lower() + ' ' + sub) for x in thread_keywords) and threads[i].op.post_id not in observed_thread_ids: # check for keywords in OP
                 observed_thread_ids.append(threads[i].op.post_id)
                 #thread = observe_thread (observe_thread, (threads[i], ))
                 thread = observe_thread(threads[i])
                 py_threads.append(thread)
                 thread.start()
                 print "========================================"
                 print "FOUND POSSIBLE GIFT THREAD No. " + str(threads[i].op.post_id) + " - Observing..."
                 print ""
                 print "URL:"
                 print threads[i].op.semantic_url
                 print "========================================"

        time.sleep(60)  
