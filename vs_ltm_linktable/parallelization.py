from multiprocessing import Queue, cpu_count
from threading import Thread
from selenium import webdriver
import time
from numpy.random import randint
import logging
from vs_ltm_linktable import scraping

def parallel(function,selenium_data):
    start_time = time.time()

    logger = logging.getLogger(__name__)

    selenium_data.append("STOP")

    selenium_data_queue = Queue()
    worker_queue = Queue()

    worker_ids = list(range(6)) #changed number of worker_ids from cpu_count() to 4
    selenium_workers = {i: webdriver.Chrome() for i in worker_ids}
    for worker_id in worker_ids:
        worker_queue.put(worker_id)


    def selenium_task(worker, data):
        function(worker, data)


    def selenium_queue_listener(data_queue, worker_queue):
        logger.info("Selenium func worker started")
        while True:
            current_data = data_queue.get()
            if current_data == 'STOP':
                # If a stop is encountered then kill the current worker and put the stop back onto the queue
                # to poison other workers listening on the queue
                logger.warning("STOP encountered, killing worker thread")
                data_queue.put(current_data)
                break
            else:
                logger.info(f"Got the item {current_data} on the data queue")
            # Get the ID of any currently free workers from the worker queue
            worker_id = worker_queue.get()
            worker = selenium_workers[worker_id]
            # Assign current worker and current data to your selenium function
            selenium_task(worker, current_data)
            # Put the worker back into the worker queue as  it has completed it's task
            worker_queue.put(worker_id)
        return


    # Create one new queue listener thread per selenium worker and start them
    logger.info("Starting selenium background processes")
    selenium_processes = [Thread(target=selenium_queue_listener,
                                 args=(selenium_data_queue, worker_queue)) for _ in worker_ids]
    for p in selenium_processes:
        p.daemon = True
        p.start()

    # Add each item of data to the data queue, this could be done over time so long as the selenium queue listening
    # processes are still running
    logger.info("Adding data to data queue")
    for d in selenium_data:
        selenium_data_queue.put(d)

    # Wait for all selenium queue listening processes to complete, this happens when the queue listener returns
    logger.info("Waiting for Queue listener threads to complete")
    for p in selenium_processes:
        p.join()

    # Quit all the web workers elegantly in the background
    logger.info("Tearing down web workers")
    for b in selenium_workers.values():
        b.quit()

    print("This parallel operation took", time.time()-start_time, "to run")
    return