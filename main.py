import os
from dotenv import load_dotenv
from openai import OpenAI
from groq import Groq
from google import genai

load_dotenv()

openai = os.getenv("OPENAI_API_KEY")
groq = os.getenv("GROQ_API_KEY")
google = os.getenv("GEMINI_API_KEY")
# client = OpenAI()

# response = client.responses.create(
#     model="gpt-4o-mini", input="What is artificial Intelligence"
# )
# print(response.output_text)

# client = genai.Client()

# response = client.interactions.create(
#     model="gemini-3.5-flash", input="What is Artificial Intelligence"
# )

# print(response.output_text)

client = Groq()

command_history = []

while True:
    command = input("Enter your prompt here: ")
    if (command == "exit") or command == "quit" or command == "close":
        break
    command_history.append({"role": "user", "content": command})
    response = client.chat.completions.create(
        messages=command_history,
        model="llama-3.3-70b-versatile",
    )
    command_history.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    print(response.choices[0].message.content)
    print()
    print()
    print(command_history)
