import streamlit as st
from langchain import PromptTemplate, LLMChain
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",  # or rely on environment variable
    model="llama-3.3-70b-versatile"         # example model, you can change
)

st.title("AI Story Teller")
st.divider()

story_topic = st.text_input("Enter the story topic")
prompt=PromptTemplate(
    input_variables=["story_topic"],
    template="Write a creative story about {story_topic}"
)

chain = LLMChain(llm=llm, prompt=prompt)
if st.button("Generate Story"):
    story = chain.run(story_topic=story_topic)
    st.write(story)
