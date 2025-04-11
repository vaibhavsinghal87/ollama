"""langchain basic example using ChatOllama"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# create a chat template with a system message and a user message
chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that gives one line definition of the user's query."),
        ("user", "{input}"),
    ]
)
messages = chat_template.format_messages(input="What is LangChain?")
print(messages)

# create a ChatOllama instance with the model and parameters
llm = ChatOllama(model="gemma3:1b", temperature=0.5, max_tokens=1000)
response = llm.invoke(messages)
print(response)

chain = chat_template | llm | StrOutputParser()
response = chain.invoke(input="What is LangChain?")
print(response)
