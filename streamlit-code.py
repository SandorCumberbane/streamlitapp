# Documentation
# For the program to work a terminal must be opened with following is typed in:
# cd /Users/Alexander/Documents/FH\ Technikum\ Wien/WS23/Solution\ Deployment/Modul\ 4/Aufgabe4
# streamlit run streamlit-code.py

# Libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

# Import and tidy data
covid = pd.read_csv("data.csv", usecols = [0, 4, 5, 6, 7, 9])
covid.rename(columns={"dateRep": "Date",
                      "cases": "Cases",
                      "deaths": "Deaths",
                      "countriesAndTerritories": "Country",
                      "geoId": "Geocode",
                      "popData2020": "Population"}, inplace=True)
covid["Date"] = pd.to_datetime(covid["Date"],
                               format="%d/%m/%Y").dt.date


# Streamlit
st.title('Covid 19 Dashboard')

st.header("*by Alexander Kopp*")

countries = st.multiselect(label="Select your countries:",
               options=covid["Country"].unique().tolist(),
               default="Austria")

st.write('You selected: {}'.format(", ".join(countries)))

plottype = st.multiselect(label="Select your type:",
                      options=["Cases", "Deaths"],
                      default="Cases")

covid_selection = covid[covid["Country"].isin(countries)]
halfyear_ranges = pd.date_range("2020", "2022", freq="AS").date

if "Cases" in plottype:
    st.header("Number of cases")
    cases = covid_selection[["Date", "Country", "Cases"]].set_index("Date").pivot(columns="Country", values="Cases")
    fig, ax = plt.subplots()
    ax.plot(cases)
    ax.legend(countries)
    ax.set_xticks(halfyear_ranges)
    st.pyplot(fig)
    
    st.header("Number of cases divided by population")
    covid_selection["Cases/Pop"] = covid_selection.apply(lambda row: row.Cases / row.Population, axis=1)
    cases_pop = covid_selection[["Date", "Country", "Cases/Pop"]].set_index("Date").pivot(columns="Country", values="Cases/Pop")
    fig, ax = plt.subplots()
    ax.plot(cases_pop)
    ax.legend(countries)
    ax.set_xticks(halfyear_ranges)
    st.pyplot(fig)

if "Deaths" in plottype:
    st.header("Number of deaths")
    deaths = covid_selection[["Date", "Country","Deaths"]].set_index("Date").pivot(columns="Country", values="Deaths")
    fig, ax = plt.subplots()
    ax.plot(deaths)
    ax.legend(countries)
    ax.set_xticks(halfyear_ranges)
    st.pyplot(fig)
    
    st.header("Number of deaths divided by population")
    covid_selection["Deaths/Pop"] = covid_selection.apply(lambda row: row.Deaths / row.Population, axis=1)
    deaths_pop = covid_selection[["Date", "Country", "Deaths/Pop"]].set_index("Date").pivot(columns="Country", values="Deaths/Pop")
    fig, ax = plt.subplots()
    ax.plot(deaths_pop)
    ax.legend(countries)
    ax.set_xticks(halfyear_ranges)
    st.pyplot(fig)

st.header("Address Locator")

strasse = st.text_input("Enter your street:", "Höchstädtplatz")
stadt = st.text_input("Enter your city:", "Wien")
address = strasse + ", " + stadt
geolocator = Nominatim(user_agent="app")
location = geolocator.geocode(address)
st.write("Did you mean", address, "?")
st.write("It is located here:")
df = pd.DataFrame(
    {"lat": [location.latitude], "lon": [location.longitude]})
st.map(df)

