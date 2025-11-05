import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="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",  # or rely on environment variable
    model="llama-3.3-70b-versatile"         # example model, you can change
)
st.title("AI Recipe Generator")
st.divider()
template="""
You are a world class chef. You have been asked to create a recipe based on the ingredients provided by the user.
You will provide a detailed recipe with the following sections:
1. Ingredients
2. Instructions
3. Cooking Time
4. Serving Suggestions
"""     
prompt=PromptTemplate(
    input_variables=["ingredients"],
    template=template + "The ingredients are: {ingredients}. Provide the recipe in the sections mentioned above."
)
chain = LLMChain(llm=llm, prompt=prompt)
ingredients = st.text_input("Enter the ingredients you have (comma separated)")
if st.button("Generate Recipe"):
    response = chain.run({"ingredients": ingredients})
    st.write(response)  
    