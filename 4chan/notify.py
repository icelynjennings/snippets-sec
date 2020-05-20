import logging
import argparse
import basc_py4chan
import threading
import time
from itertools import islice

format = "%(asctime)s [%(levelname)s] %(message)s"
logger = logging.getLogger('example')
logging.basicConfig(filename='logs.txt',format=format,level=logging.INFO)



from observe_thread import observe_thread
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Notifications for 4chan threads. Finds threads matching given search terms.')
    parser.add_argument('-t', '--terms', nargs='+')
    args = parser.parse_args()

    search_terms = args.terms
    observed_thread_ids = []

    py_threads = []
    lock = threading.Lock()
    board = basc_py4chan.Board('v')

    # Keep checking for new threads
    while 1:
        with lock:
            try:
                # Get currently open threads
                open_threads = board.get_all_threads()
                open_thread_ids = board.get_all_thread_ids()
            except:
                pass

        new_threads = [i for i in open_threads if i.op.post_id not in observed_thread_ids]        
        for t in new_threads:
            try:
                subject = t.op.subject.lower()
            except:
                subject = ""
                
            full_OP = subject + ' ' + t.op.text_comment.lower()
            match = t.op.post_id not in observed_thread_ids and any(x in (full_OP) for x in search_terms)
            
            if match:
            
                thread = observe_thread(t,search_terms,lock)
                py_threads.append(thread)
                thread.start()
            
                observed_thread_ids.append(t.op.post_id)
                newthread_notification = "Thread found: {}".format(str(t.op.semantic_url))                
                logger.info(newthread_notification)
                print newthread_notification
                
        time.sleep(2)  
