import requests
import streamlit as st

def get_country_info(country_name):
    response = requests.get(f'https://restcountries.com/v3.1/name/{country_name}')
    if response.status_code == 200:
        return response.json()
        country_name = response.json()[0]['name']['common']
        capital = response.json()[0]['capital'][0]
        population = response.json()[0]['population']
        area = response.json()[0]['area']
        currency = response.json()[0]['currencies']
        return {
            "name": country_name,
            "capital": capital,
            "population": population,
            "area": area
        }
    else:
        return None
def main():
    st.title("Country Information")
    country_name = st.text_input("Enter a country name:")
    if country_name:
        info = get_country_info(country_name)
        if info:
            st.write("Country Name:", info['name'])
            st.write("Capital:", info['capital'])
            st.write("Population:", info['population'])
            st.write("Area:", info['area'])
            st.write("Currency:", info['currencies'])
        else:
            st.write("Country not found.")
