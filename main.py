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


def get_reply(messages, provider):
    if provider == "groq":
        client = Groq(api_key=groq)

        response = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
        )
        return response.choices[0].message.content

    elif provider == "openai":
        client = OpenAI(api_key=openai)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content

    elif provider == "gemini":
        client = genai.Client(api_key=google)

        prompt = "\n".join(
            f"{message['role']}: {message['content']}" for message in messages
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    raise ValueError(f"Unknown provider: {provider}")


personas = {
    "default": "you are a helpful, general purpose, concise AI assistant",
    "teacher": "you are a helpful AI assistant for teachers who teaches to his students",
    "student": "you are a helpful AI assistant for student to help them in understanding topics but not cheating should be provided",
    "pirate": "You are a swashbuckling pirate captain. Speak in pirate slang.",
    "kid": "You are an Informative AI assistant, avoid un-necessary details and use a friendly tone",
}

current_persona = "default"
current_provider = "groq"

if os.path.exists("memory.json"):
    try:
        with open("memory.json", "r") as f:
            command_history = json.load(f)
    except json.JSONDecodeError:
        command_history = []
else:
    command_history = []

if not command_history or command_history[0]["role"] != "system":
    command_history.insert(
        0,
        {
            "role": "system",
            "content": personas[current_persona],
        },
    )

while True:
    command = input("Enter your prompt here: ").strip()

    if command.lower() in ("exit", "quit", "close"):
        break

    if command.startswith("/help"):
        print("Commands:")
        print("  /persona <name>      - switch persona")
        print("  /ai <provider>       - switch AI provider")
        print("  /history [n]         - show last n turns (default 5)")
        print("  /reset               - clear conversation, keep current persona")
        print("  exit / quit / close  - save and quit")
        continue

    if command.startswith("/history"):
        parts = command.split()
        n = int(parts[1]) if len(parts) == 2 and parts[1].isdigit() else 5

        for turn in command_history[-n:]:
            print(f"{turn['role']}: {turn['content']}")
        continue

    if command.startswith("/reset"):
        command_history = [
            {
                "role": "system",
                "content": personas[current_persona],
            }
        ]

        with open("memory.json", "w") as f:
            json.dump(command_history, f, indent=4)

        print(f"Conversation cleared. Persona kept: {current_persona}")
        continue

    if command.startswith("/persona"):
        parts = command.split()

        if len(parts) == 2 and parts[1] in personas:
            current_persona = parts[1]
            command_history[0] = {
                "role": "system",
                "content": personas[current_persona],
            }
            print(f"Switched persona to: {current_persona}")
        else:
            print("Usage: /persona <name>")
            print("Available:", ", ".join(personas.keys()))
        continue

    if command.startswith("/ai"):
        parts = command.split()

        providers = ["groq", "openai", "gemini"]

        if len(parts) == 2 and parts[1].lower() in providers:
            current_provider = parts[1].lower()
            print(f"Switched AI provider to: {current_provider}")
        else:
            print("Usage: /ai <provider>")
            print("Available:", ", ".join(providers))
        continue

    command_history.append(
        {
            "role": "user",
            "content": command,
        }
    )

    try:
        reply_text = get_reply(command_history, current_provider)
    except Exception as e:
        print(f"Error: {e}")
        command_history.pop()
        continue

    command_history.append(
        {
            "role": "assistant",
            "content": reply_text,
        }
    )

    with open("memory.json", "w") as f:
        json.dump(command_history, f, indent=4)

    print(f"\n[{current_provider.upper()} | {current_persona}]")
    print(reply_text)
    print()
