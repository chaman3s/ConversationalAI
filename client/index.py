import gradio as gr

# Temporary reply function will connect to backend later
def fake_ai_reply(message, history):
    response = "🤖 AI says: " + message[::-1]  # Just reverses input for now
    history.append((message, response))
    return history, history

# Launch the chat interface
gr.ChatInterface(
    fn=fake_ai_reply,
    title="Conversational AI Chat",
    description="Type anything and get a (fake) AI response!",
    theme="default"
).launch()
