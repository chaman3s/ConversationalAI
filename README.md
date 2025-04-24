# 🤖 Conversational AI Chatbot

A full-stack conversational chatbot app that integrates with multiple LLMs like GPT-4, Claude, Gemini, AI21, and more. It features a FastAPI backend and a Gradio-based frontend.

---

## 🚀 Features

- 🔌 Model switching: GPT-4, Claude, Mistral, Meta LLaMA, Gemini, AI21, DeepSeek
- 🧠 Maintains conversation history
- 🔄 Chain prompts in multi-turn flow
- 🎭 Ask one question to multiple models
- 💬 Clean Gradio UI with avatars and styles
- 🌍 Local setup, fully customizable

---

## 📁 Structure
backend/ ├── main.py # FastAPI app 
        ├── routes/ # API endpoints 
        ├── controllers/ # Chat handling logic 
        ├── validators/ # Request models 
        └── utils/llm_client.py # LLM integrations 
    client/ 
          └── index.py # Gradio frontend


docker build -t my-chat-app .
docker run -p 8000:8000 my-chat-app