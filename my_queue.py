import queue
import threading
import time

# Initializing queues for document uploads and URL 
document_queue = queue.Queue()
url_queue = queue.Queue()

# Function to enqueue tasks
def producer(task_type, task_data):
    # Add urls or upload documents
    if task_type == "document":
        queue_to_use = document_queue
    elif task_type == "url":
        queue_to_use = url_queue
    else:
        raise ValueError("Invalid task type")

    # Enqueue the task into the appropriate queue
    queue_to_use.put(task_data)

# Consumer function to dequeue and process tasks
def consumer(queue):
    while True:
        # Retrieve a task from the queue
        task = queue.get()
        # Mark the task as complete
        queue.task_done()

# Create and start producer and consumer threads for document uploads
document_producer_thread = threading.Thread(target=producer, args=("document", "document_path"))
document_consumer_thread = threading.Thread(target=consumer, args=(document_queue,))

document_producer_thread.start()
document_consumer_thread.start()

# Create and start producer and consumer threads for URL entries
url_producer_thread = threading.Thread(target=producer, args=("url", "https://example.com"))
url_consumer_thread = threading.Thread(target=consumer, args=(url_queue,))

url_producer_thread.start()
url_consumer_thread.start()