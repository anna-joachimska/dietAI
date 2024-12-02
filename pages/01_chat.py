import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from ai import chat

#Initialize chat history in sesssion state
if "messages" not in st.session_state:
    st.session_state.messages = []


col1, col2 = st.columns([2, 1])

with col1:
    st.title("Food Advisor")
with col2:
    with stylable_container(
        key="clear_chat_button",
        css_styles="""
        button {
        float: right;
        }
        """
    ):
        if st.button("🗑️", type="primary"):
            st.session_state.messages = []


#display chat history from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#react to user input

## inaczej
# prompt = st.chat_input("whats up")
#if prompt:
#rest

if prompt := st.chat_input("What's up?"):
    # display user message in chat container
    st.chat_message("user").markdown(prompt)
    #add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = chat.generate_response(prompt, st.session_state.messages)

    #display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    ## add ai response to chat history
    st.session_state.messages.append(({"role": "assistant", "content": response}))
