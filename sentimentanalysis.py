import streamlit as st
from textblob import TextBlob
st.title("Sentiment Analysis App")
user_input=st.text_area("Enter Text","Type Here")
if st.button("Analyze"):
    blob=TextBlob(user_input)
    result=blob.sentiment.polarity
    if result>0:
        st.write("Positive Sentiment")    
    elif result<0:
        st.write("Negative Sentiment")
    else:
        st.write("Neutral Sentiment")
     