# create simple chat app using ollama 

import ollama

print(ollama.list())  # list all models

result = ollama.generate(
    model="gemma3:1b",
    prompt="Can you tell me a joke on Generative AI?"
)

print(result["response"])

response = ollama.chat(
    model="gemma3:1b",
    messages=[
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm good, thank you! How can I help you today?"}
    ],
)

print(response["message"]["content"])

# create model using a model file
modelfile = """
FROM gemma3:1b
SYSTEM You are Jarvis from Iron man and the user is Tony Stark. 
"""

ollama.create(model="jarvis", model_file=modelfile)
response = ollama.chat(
    model="jarvis",
    messages=[
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm good, thank you! How can I help you today?"}
    ],
)
