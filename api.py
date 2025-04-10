from ollama import Client

client = Client("http://localhost:11434")

response = client.chat(
    model="gemma3:1b",
    messages=[
        {"role": "user", "content": "What is Generative AI?"},
    ],
)
print(response["message"]["content"])
