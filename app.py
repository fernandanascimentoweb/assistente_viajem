import os
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory


template = """ Você é um assistente de viagem que ajuda o usuário a planejar viagens, dando sugestões de destinos, roteiros e dicas práticas.
A primeira coisa que deve fazer é perguntar para onde o usuário vai, com quantas pessoas e por quanto tempo.

Histórico da conversa:
{history}

Entrada do usuário:
{input}"""


prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"), #placeholder para historico estruturado
    ("human", "{input}")
])

# modelo de linguagem que vai utilizar
llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini")

chain = prompt | llm


store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# -------- INTERFACE STREAMLIT --------
st.set_page_config(page_title="Assistente de Viagem", page_icon="✈️")
st.title("✈️ Assistente de Viagem")
st.write("Converse com seu assistente para planejar sua próxima viagem.")

# Inicializar histórico no Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir histórico no chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Caixa de entrada do usuário
if prompt_text := st.chat_input("Digite sua pergunta aqui..."):
    # Exibir mensagem do usuário
    st.chat_message("user").markdown(prompt_text)
    st.session_state.messages.append({"role": "user", "content": prompt_text})

    # Gerar resposta
    resposta = chain_with_history.invoke(
        {"input": prompt_text},
        config={"configurable": {"session_id": "user123"}}
    )

# Mostrar resposta do assistente
    resposta_texto = resposta.content
    with st.chat_message("assistant"):
        st.markdown(resposta_texto)

    st.session_state.messages.append({"role": "assistant", "content": resposta_texto})

#============================== fim streamlit =============================================

def iniciar_assistente_viagem():
    print("\nBem-vindo ao Assistente de Viagem! Digite 'sair' para encerrar. \n")
    while True:
        pergunta_usuario = input("Você: ")

        if pergunta_usuario.lower() in ["sair", "exit"]:
            print("Assistente de Viagem: Até mais! Aproveite sua viagem!")
            break

        resposta = chain_with_history.invoke(
            {'input': pergunta_usuario},
            config={'configurable': {'session_id': 'user123'}}
        )

        print('Assistente de Viagem : ', resposta.content)


if __name__ == "__main__":
    iniciar_assistente_viagem()
