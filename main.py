import streamlit as st
from openai import OpenAI

from ai_agents import AI_Player

player1 = AI_Player(name="John", prompt="You are a twitter/X user. Argue FOR whatever the topic is. Defend it with all your might. Only use 240 characters.")
player2 = AI_Player(name="Mike", prompt="You are a twitter/X user. Argue Against whatever the topic is. Dismantle it with all your might. Only use 240 characters.")

st.title("Endless Argument Simulator")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"
if "messages" not in st.session_state:
    st.session_state.messages = []
# if "first_message" not in st.session_state:
#     st.session_state.first_message = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Choose a topic that the AI will argue about."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role":"user", "content": f"Topic: {prompt}"})
    response1, response2 = None, None
    while response1 != 'pass' or response2 != 'pass':
        response1 = player1.respond(st.session_state.messages)
        with st.chat_message("assistant"):
            st.markdown(f"{player1.name}: {response1}")
        st.session_state.messages.append({"role": "assistant", "content": f"{player1.name}: {response1}"})

        response2 = player2.respond(st.session_state.messages)
        with st.chat_message("assistant"):
            st.markdown(f"{player2.name}: {response2}")
        st.session_state.messages.append({"role": "assistant", "content": f"{player2.name}: {response2}"})

