from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from dotenv import load_dotenv
from queue import Queue
from threading import Thread

load_dotenv()


queue = Queue()

"""
 Every single token that is received by our language model
"""
class StreamingHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token, **kwargs):
        queue.put(token)
    def on_llm_end(self, response, **kwargs):
        queue.put(None)
    def on_llm_error(self, error, **kwargs):
        queue.put(None)        

chat = ChatOpenAI(streaming=True, callbacks=[StreamingHandler()]) # Controls how OpenAI responds to LangChain
                                  # Whether or not the response is going to be streamed  

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

# messages = prompt.format_messages(content="Tell me a joke.")
# chain = LLMChain(llm=chat, prompt=prompt)

#output = chat(messages)
# output = chat.__call__(messages) Controls
# __call__() -> Controls how LangChain  responds to us and also
          #  -> Controls how OpenAI responds to LangChain 
          # Whether or not the response is going to be streamed over those two segments

#output = chat.stream(messages)

# chat.stream(messages) Override the language model streaming flag

# for output in chain.stream(input={"content": "tell me a joke"}):
#     print(output)

class StreamingChain(LLMChain):
    def stream(self, input):
        def task():
            self(input) #Execute the Chain
        Thread(target=task).start()
        while True:
            token = queue.get()
            if token is None:
                break
            yield token

chain = StreamingChain(
    llm=chat,
    prompt=prompt
)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)