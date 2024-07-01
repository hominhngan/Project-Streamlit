import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


def generate_response(prompt_input, hf_email, hf_password):
    try:
        # Login to Hugging Face
        sign = Login(hf_email, hf_password)
        cookies = sign.login()

        # Create Chatbot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        return chatbot.chat(prompt_input)
    except Exception as e:
        return str(e)


def main():
    # App title
    st.title("Simple Chatbot")

    # Login UI
    # Hugging Face credentials
    with st.sidebar:
        st.title("Login HugChat")
        hf_email = st.text_input("Enter Email:")
        hf_password = st.text_input("Enter Password:", type="password")
        if not (hf_email and hf_password):
            st.warning("Please enter your Email and Password")
        else:
            st.success("Proceed to entering Simple Chatbot")

    # Simple Chatbot UI
    # Store LLM response in session
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if user_prompt := st.chat_input(disabled=not (hf_email and hf_password)):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        # Generate new response if last response wasn't from "role": "assistant"
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(user_prompt, hf_email, hf_password)
                    st.write(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == '__main__':
    main()
