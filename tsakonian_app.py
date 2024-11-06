import streamlit as st
from llama_cpp import Llama

# Streaming helper
def stream_text(text):
    for char in text:
        yield char

st.title("Tsakonian translator")

if st.session_state.get("model_loaded", False) == False:
    with st.spinner('Loading model... This might take 5 minutes to run.'):
        llm = Llama.from_pretrained(
            repo_id="jgchaparro/Tyros-v5-8B-GGUF",
            filename="tyros-v5-8b.Q2_K.gguf",
        )
        st.session_state.model_loaded = True
        st.session_state.llm = llm

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if greek_sentence := st.chat_input("Input a sentence in Greek to translate to Tsakonian..."):
    st.session_state.messages.append({"role": "user", "content": greek_sentence})
    with st.chat_message("user"):
        st.markdown(greek_sentence)

    with st.chat_message("assistant"):
        response = st.session_state.llm.create_chat_completion(
        messages = [
            {
                "role": "user",
                "content": f"Translate from Greek to Tsakonian: {greek_sentence}"
            }
        ],
        temperature = 0,
    )

        translation = response['choices'][0]['message']['content'].replace('Translation to Tsakonian: ', "")
        st.write_stream(stream_text(translation))
        st.session_state.messages.append({"role": "assistant", "content": translation})