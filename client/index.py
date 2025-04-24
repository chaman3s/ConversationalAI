import gradio as gr
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Initial chat history
history = []

# List of available models
available_models = [
    "chatgpt", "chatgpt4", "Anthropic claude", "Anthropic claude pro",
    "MetaAi", "MetaAi Pro", "Mistral", "Mistral Pro",
    "DeepSeek Free", "DeepSeek Coder", "MythoMax", "gemini", "ai21"
]

# Function to call FastAPI for a single model
def talk_to_backend(message, history, model):
    if(len(message)<=0) : 
        history.append([" ", "!pls type somthing"]) 
        return "", history, history

    payload = {"message": message, "history": history, "Ai": model}
    try:
        res = requests.post(API_URL, json=payload).json()
        reply = res.get("reply") or res.get("response", [""])[0]
        history.append([message, reply])
    except Exception as e:
        history.append([message, f"Error: {e}"])
    return "", history, history

# Function to chain multiple prompts
def chain_prompts(message, history, model):
    if(len(message)<=0) : 
        history.append(["", "!pls type somthing"]) 
        return "", history, history
    
    inter = history.copy()
    step1 = f"Step 1: {message}"
    _, inter, _ = talk_to_backend(step1, inter, model)
    step2 = "Step 2: Can you elaborate more?"
    _, inter, _ = talk_to_backend(step2, inter, model)
    return "", inter, inter

# Function to query all models and append responses to chat history
def multi_model_chain(message, history):
    if(len(message)<=0) : 
        history.append([" ", "!pls type somthing"]) 
        return "", history, history
    
    inter = history.copy()
    for model in available_models:
        payload = {"message": message, "history": [], "Ai": model}
        try:
            res = requests.post(API_URL, json=payload).json()
            reply = res.get("reply") or res.get("response", [""])[0]
            inter.append([f"{model}", reply])
        except Exception as e:
            inter.append([f"{model}", f"Error: {e}"])
    return "", inter, inter

# CSS for styling: reduced message box height and increased input box height
custom_css = """
.chatbot .message.user .bubble,
.chatbot .message.bot .bubble {
    max-height: 120px;   /* Reduced message bubble height */
    overflow-y: auto;
}
#msg textarea {
    height: 100px !important;  /* Increased input box height */
}
.chatbot .message.user {
    display: flex; align-items: flex-start;
}
.chatbot .message.user::before {
    content: "";
    width: 32px; height: 32px;
    background-image: url('/file/assets/images/userLogo.svg');
    background-size: cover;
    margin-right: 8px;
}
.chatbot .message.bot {
    display: flex; align-items: flex-start;
}
.chatbot .message.bot::before {
    content: "";
    width: 32px; height: 32px;
    background-image: url('/file/assets/images/chatBot.svg');
    background-size: cover;
    margin-right: 8px;
}
.chatbot .message.user .bubble { background-color: #1e88e5 !important; color: white !important; }
.chatbot .message.bot .bubble { background-color: #43a047 !important; color: white !important; }
"""

# Gradio UI
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("## 🤖 Conversational AI Chat")
    with gr.Row():
        model_dropdown = gr.Dropdown(choices=available_models, label="Select Model", value="chatgpt")
    chatbot = gr.Chatbot(value=history, label="Chatbot", elem_classes="chatbot")
    msg = gr.Textbox(label="Type a message…", elem_id="msg")
    state = gr.State(value=history)
    with gr.Row():
        chain_button = gr.Button("🔄 Run Chain Prompt")
        multi_button = gr.Button("🤹‍♂️ Ask All Models")

    def submit_fn(user_msg, hist, model):
        return talk_to_backend(user_msg, hist, model)

    def chain_fn(user_msg, hist, model):
        return chain_prompts(user_msg, hist, model)

    def multi_fn(user_msg, hist):
        return multi_model_chain(user_msg, hist)

    msg.submit(submit_fn, [msg, state, model_dropdown], [msg, chatbot, state])
    chain_button.click(chain_fn, [msg, state, model_dropdown], [msg, chatbot, state])
    multi_button.click(multi_fn, [msg, state], [msg, chatbot, state])

demo.launch()
