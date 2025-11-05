import streamlit as st
from langchain import LLMChain, PromptTemplate
from langchain.llms import OpenAI
st.title("LLM Web App")
st.write("Welcome to the LLM Web App!")
st.divider()
st.write("Enter your prompt below:")
user_input = st.text_area("Prompt")
st.divider()
if user_input:
    st.balloons()
    llm=OpenAI(temperature=0.7,
                openai_api_key="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")
    template=("You are a helpful assistant.Answer this prompt: {user_input}"
    )
    prompt=PromptTemplate(
        input_variables=["user_input"],
        template=template,
    )
    llm_chain=LLMChain(prompt=prompt,llm=llm)
    response=llm_chain.run(user_input)
    st.write("Assistant's response:")
    st.write(response)
