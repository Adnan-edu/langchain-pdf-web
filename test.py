from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(streaming=True) # Controls how OpenAI responds to LangChain
                                  # Whether or not the response is going to be streamed  

prompt = ChatPromptTemplate.from_messages([
    ("human", "{content}")
])

messages = prompt.format_messages(content="Tell me a joke.")

#output = chat(messages)
# output = chat.__call__(messages) Controls
# __call__() -> Controls how LangChain  responds to us and also
          #  -> Controls how OpenAI responds to LangChain 
          # Whether or not the response is going to be streamed over those two segments

#output = chat.stream(messages)

# chat.stream(messages) Override the language model streaming flag

for message in chat.stream(messages):
    print(message.content)