import streamlit as st
import time

st.title(" Streamlit Pomodor Timer App")

worktime=st.slider("Work Time (minutes)",5,90,25)
Breaktime=st.slider("Break Time (minutes)",1,30,5)

def pomodorotimer(worktime,Breaktime):
	workseconds=worktime*60
	breakseconds=Breaktime*60
	
    workplaceholder=st.empty()
    breakplaceholder=st.empty()

    workplaceholder.text(f"Work Time: {workseconds} seconds")

    breakplaceholder.text(f"Break Time: {breakseconds} seconds")




	
			
		


