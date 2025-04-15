import streamlit as st
import requests

# Page configuration
st.set_page_config(page_title="Property Management Assistant", page_icon="🏠", layout="wide")

# Mistral API configuration
MISTRAL_API_KEY = "o8PPaDDrfEMa7n3dNuOojKsgjZu5PC56"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# System prompt
SYSTEM_PROMPT = """You are a knowledgeable Property Management Assistant, specialized in helping with rental property management tasks and queries. 
Your expertise includes:
- Property listing and marketing
- Tenant screening and management
- Lease agreements and documentation
- Maintenance and repairs
- Rent collection and financial management
- Property inspections
- Legal compliance and regulations

If a question is outside the scope of property management, politely inform the user and redirect them to property-related topics.

Always be professional, clear, and concise in your responses."""

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your Property Management Assistant. How can I help you today?"}
    ]

# Sidebar - Clear chat
with st.sidebar:
    st.title("⚙️ Options")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "👋 Hello! I'm your Property Management Assistant. How can I help you today?"}
        ]

# Chat window container
st.markdown("""
    <div class="chat-window">
""", unsafe_allow_html=True)

# Chat message rendering
for msg in st.session_state.messages:
    role = msg["role"]
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    st.markdown(f"""
        <div class="{bubble_class}">
            <div class="bubble-content">{msg["content"]}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input box at bottom
prompt = st.chat_input("Ask me anything about property management...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {
                    "model": "mistral-tiny",
                    "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {MISTRAL_API_KEY}"
                }
                response = requests.post(API_URL, headers=headers, json=payload)
                if response.status_code == 200:
                    reply = response.json()["choices"][0]["message"]["content"]
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.markdown(reply)
                else:
                    st.error("❌ Failed to get response from Mistral API.")
            except Exception as e:
                st.error(f"🚨 Error: {e}")

# Custom CSS for ChatGPT-like interface
st.markdown("""
    <style>
    .chat-window {
        max-width: 800px;
        margin: auto;
        padding: 20px;
        background-color: #ffffff;
    }

    .user-bubble, .assistant-bubble {
        display: flex;
        margin-bottom: 16px;
        max-width: 100%;
    }

    .user-bubble {
        justify-content: flex-end;
    }

    .assistant-bubble {
        justify-content: flex-start;
    }

    .bubble-content {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 80%;
        font-size: 1rem;
        line-height: 1.5;
        box-shadow: 0 1px 6px rgba(0, 0, 0, 0.05);
    }

    .user-bubble .bubble-content {
        background-color: #007bff;
        color: white;
        border-bottom-right-radius: 4px;
    }

    .assistant-bubble .bubble-content {
        background-color: #f1f1f1;
        color: #333;
        border-bottom-left-radius: 4px;
    }

    .stChatInput {
        position: sticky;
        bottom: 0;
        background: white;
        padding-top: 16px;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)