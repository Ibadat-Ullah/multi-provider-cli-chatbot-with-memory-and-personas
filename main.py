import os
import json
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

personas = {
    "default": "you are a helpful, general purpose, concise AI assistant",
    "teacher": "you are a helpful AI assistant for teachers who teaches to his students",
    "student": "you are a helpful AI assistant for student to help them in understanding topics but not cheating should be provided",
    "pirate": "You are a swashbuckling pirate captain. Speak in pirate slang.",
    "kid": "You are an Informative AI assistant, avoid un-necessary details and use a friendly tone",
}

current_persona = "default"

if os.path.exists("memory.json"):
    try:
        with open("memory.json", "r") as f:
            command_history = json.load(f)
    except json.JSONDecodeError:
        command_history = []
else:
    command_history = []

if not command_history or command_history[0]["role"] != "system":
    command_history.insert(0, {"role": "system", "content": personas[current_persona]})

while True:
    command = input("Enter your prompt here: ")
    if (command == "exit") or command == "quit" or command == "close":
        break

    if command.startswith("/help"):
        print("Commands:")
        print("  /persona <name>   - switch persona")
        print("  /history [n]      - show last n turns (default 5)")
        print("  /reset            - clear conversation, keep current persona")
        print("  exit / quit / close - save and quit")
        continue

    if command.startswith("/history"):
        parts = command.split()
        n = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 5
        for turn in command_history[-n:]:
            print(f"{turn['role']}: {turn['content']}")
            continue

    if command.startswith("/reset"):
        command_history = [{"role": "system", "content": personas[current_persona]}]
        with open("memory.json", "w") as f:
            json.dump(command_history, f)
        print(f"Conversation Cleared, Persona kept : {current_persona}")

    if command.startswith("/persona"):
        parts = command.split()
        if len(parts) == 2 and parts[1] in personas:
            current_persona = parts[1]
            command_history[0] = {
                "role": "system",
                "content": personas[current_persona],
            }
            print(f"Switched to: {current_persona}")
        else:
            print("Usage: /persona <name>. Available:", " ".join(personas.keys()))
            continue
    command_history.append({"role": "user", "content": command})
    response = client.chat.completions.create(
        messages=command_history,
        model="llama-3.3-70b-versatile",
    )
    command_history.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )

    with open("memory.json", "w") as f:
        json.dump(command_history, f)

    print(response.choices[0].message.content)
    print()
    print()
    print(command_history)
