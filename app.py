import streamlit as st
import uuid
import requests


st.set_page_config(
    page_title = "PathFinder",
    page_icon = "🎓",
    layout = "centered",
)

st.markdown("""
    <style>
    .stApp {
        background-color: #e9e3ff;
    }
    </style>
    """, unsafe_allow_html=True)



# ------------------ LOAD CSS ------------------
def load_css():
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # App still works without CSS


load_css()


# ------------------ SESSION STATE ------------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())


# ------------------ LANDING PAGE ------------------
def landing_page():
    st.markdown(
        """
        <div class="landing-container">
            <div class="icon">🎓</div>
            <h1 class="title">Academic Advisor AI</h1>
            <p class="subtitle">
                Your personal guide to discovering the perfect major, career path,
                and university that aligns with your interests, strengths, and goals.
            </p>
            <br>
        </div>
        """
        ,unsafe_allow_html=True
    )

    if st.button("Start Your Journey", key="start_button"):
        st.session_state.page = "chat"
        st.rerun()

    st.markdown(
        "<p class='footer-text'>Free • Personalized • No sign-up required</p>",
        unsafe_allow_html=True
    )



# ------------------ CHAT PAGE ------------------
def chat_page():
    if st.button("← Back to Landing Page", key="back_button"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown(
        """
        <div class="chat-header">
            <span class="bot-icon">🎓</span>
            <div>
                <h3 class="chat-title">Academic Advisor AI</h3>
                <p class="chat-subtitle">Here to help with your academic journey</p>
            </div>
        </div>
        <hr>
        """,
        unsafe_allow_html=True
    )



    # Initial bot message
    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "Hi! I'm your academic advisor chatbot. I'm here to help you explore "
                "majors, career paths, and universities that match your interests and goals.\n\n"
                "To get started, what subjects or interests do you enjoy most?"
            )
        })

    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Quick action buttons
    col1, col2, col3, col4 = st.columns(4)
    if col1.button("🎓 Explore Majors"):
        st.session_state.messages.append(
            {"role": "assistant", "content": "Great! What subjects are you most curious about?"}
        )
        st.rerun()

    if col2.button("💼 Career Paths"):
        st.session_state.messages.append(
            {"role": "assistant", "content": "Awesome! Do you have any careers in mind already?"}
        )
        st.rerun()

    if col3.button("🏫 Find Universities"):
        st.session_state.messages.append(
            {"role": "assistant", "content": "Nice! Are you looking for universities in a specific country?"}
        )
        st.rerun()

    if col4.button("📊 Compare Options"):
        st.session_state.messages.append(
            {"role": "assistant", "content": "Sure! What options would you like to compare?"}
        )
        st.rerun()

    # User input
    user_input = st.chat_input("Type your message here...", key="user_input")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        # replaced with API call to backend
        try:
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"user_id": st.session_state.user_id, "message": user_input}
            )
            bot_reply = response.json()["response"]
        except Exception as e:
            bot_reply = f"Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()



# ------------------ ROUTER ------------------
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "chat":
    chat_page()
