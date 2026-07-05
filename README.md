# Multi-Provider AI CLI Chat Assistant

A Python command-line chatbot that lets you interact with multiple AI providers from one interface.

Currently supported providers:
- OpenAI (GPT-4o Mini)
- Groq (Llama 3.3 70B Versatile)
- Google Gemini (Gemini 2.5 Flash)

The application also supports conversation memory, AI personas, provider switching, chat history, and conversation reset.

---

## Features

- 🤖 Multiple AI providers
  - OpenAI
  - Groq
  - Google Gemini

- 🎭 Multiple AI personas
  - Default Assistant
  - Teacher
  - Student
  - Pirate
  - Kid-Friendly Assistant

- 💾 Persistent conversation memory
  - Saves conversations to `memory.json`
  - Automatically loads previous conversations

- 🔄 Switch providers at runtime

- 📝 View recent chat history

- ♻ Reset conversations while keeping the selected persona

- ⚡ Simple command-line interface

---

## Project Structure

```
.
├── main.py
├── memory.json
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10+
- API key for at least one provider

Install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install openai groq google-genai python-dotenv
```

---

## Environment Variables

Create a `.env` file in the project directory.

```env
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Only the providers you intend to use require valid API keys.

---

## Running the Application

```bash
python main.py
```

You will be prompted to enter messages in the terminal.

Example:

```
Enter your prompt here:
```

---

## Available Commands

### Show help

```
/help
```

Displays all available commands.

---

### Change AI Provider

```
/ai openai
```

```
/ai groq
```

```
/ai gemini
```

---

### Change Persona

```
/persona teacher
```

Available personas:

- default
- teacher
- student
- pirate
- kid

---

### Show Conversation History

```
/history
```

Show the last 5 messages.

Or specify a number:

```
/history 10
```

---

### Reset Conversation

```
/reset
```

Clears the conversation while keeping the current persona.

---

### Exit

```
exit
```

or

```
quit
```

or

```
close
```

Conversation history is automatically saved before exiting.

---

## Personas

### Default
General-purpose AI assistant.

### Teacher
Explains concepts clearly for teaching and learning.

### Student
Helps students understand topics without providing cheating assistance.

### Pirate
Responds entirely in pirate language.

### Kid
Uses simple, friendly, age-appropriate explanations.

---

## Conversation Memory

The application stores all conversations in:

```
memory.json
```

This allows conversations to continue between sessions.

If the file does not exist, it will be created automatically.

---

## Supported Models

| Provider | Model |
|----------|-------|
| OpenAI | GPT-4o Mini |
| Groq | Llama 3.3 70B Versatile |
| Google Gemini | Gemini 2.5 Flash |

---

## How It Works

1. Loads API keys from `.env`
2. Loads previous conversation from `memory.json`
3. Applies the selected system persona
4. Sends the conversation history to the selected AI provider
5. Saves new messages back to `memory.json`

---

## Future Improvements

- Streaming responses
- Markdown rendering
- Token usage tracking
- Additional AI providers
- Voice input/output
- Conversation export
- Multiple chat sessions
- GUI/Web interface

---
