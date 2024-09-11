from flask import current_app
from queue import Queue
from threading import Thread

from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)
        def task(app_context):
            app_context.push() #Gives access to context inside this new thread
            self(input, callbacks=[handler]) #Execute the Chain
        Thread(target=task, args=[current_app.app_context()]).start() # Extra argument to this task function
        while True:
            token = queue.get()
            if token is None:
                break
            yield token