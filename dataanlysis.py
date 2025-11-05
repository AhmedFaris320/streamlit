import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_groq import ChatGroq

st.set_page_config(page_title="Data Analysis with Groq", page_icon=":bar_chart:", layout="wide")
st.title("Data Analysis with Groq")     
st.subheader("Upload your CSV file and ask questions about your data")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"], key="file_uploader")

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        
        st.write("First 5 rows of the dataset:")
        st.dataframe(df.head())
        
        st.write("Ask questions about your data:")
        question = st.text_input("Enter your question here")
        
        if question:
            def create_agent(df):
                groq_api_key = "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"
                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model="llama-3.3-70b-versatile"
                )
                agent = create_pandas_dataframe_agent(llm, df, verbose=True, allow_dangerous_code=True)
                return agent
            
            agent = create_agent(df)
            with st.spinner("Analyzing..."):
                try:
                    response = agent.run(question)
                    st.write("Answer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Error analyzing data: {str(e)}")
                    
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
else:
    st.info("Please upload a CSV file to begin data analysis.")