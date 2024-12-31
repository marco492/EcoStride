import streamlit as st
import numpy as np
import pandas as pd
from datetime import date
from openai import AzureOpenAI

#with st.sidebar:
openai_api_key = "57579d7aaa8348ff9b94760a66a92a6c"
   # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    #"[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
   # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("🌍 Talk with our AI! 🌳")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "🌿 Welcome to EcoStride, your eco-friendly companion on the path to sustainability! 🌍 How can I assist you today? Whether you're seeking green tips, sustainability insights, or looking for eco-conscious spots to explore in Hong Kong, I'm here to help! Feel free to ask anything. Let's stride towards a greener future together! 🌱"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    #if not openai_api_key:
     #   st.info("Please add your OpenAI API key to continue.")
      #  st.stop()

    # START of Prompt engineering
    emoji_list= "🚲,🏖,🛤,🏞,🌄,🌅,🚵‍♀️,🏊‍♀️,🚣,🌳,🌍,🌎,🌏,🌞,🌻,🌺,🪨,🍃,🍂,🌵,🌿,🪵,🌱,🍄,☀️,🌤,⛅️,🌥,☁️,🌦,⛈,🌩,🌨,🌬,💧,🫧,☔️,🌊,🦋,🐼,🦊,🐰,🐬,🐟,🕷,🦐,🐢,🐸,🦝,🐝,🐡,🪼,🦀,🪸,🦓,🦧,🦍,🕊,🐇,🦚,🐓,🦜,🌴,🪺,🪹,🦥,😃,☺️,🙂,💚,♻️,🧗"
    command = "<INSTRUCTIONS>\
    You are an AI assistant in an app called EcoStride. Your mission is provide and answer green, eco-friendly, sustainability topics-related information to the user, or suggest places in Hong Kong for the user to visit \
    </INSTRUCTIONS> \
    \
    <CONSTRAINTS>\
    Dos and don'ts for the following aspects \
    1. Dos \
    Response in a friendly tone related with sustainability and enviornment ONLY, using emojis from {emoji_list}. Write it in Markdown format. \
    2. Don'ts \
    Do not respond with anything other than the given information, that is IRRELEVANT with sustainability, enviornment. False information may be dangerous and illegal. \
    </CONSTRAINTS> \
    \
    <CONTEXT> \
    {st.session_state.messages} \
    </CONTEXT> \
    \
    <OUTPUT_FORMAT> \
    The output format must be \
    Advice answering questions in input or related with input  \
    </OUTPUT_FORMAT> \
    \
    <RECAP>\
    False information may be dangerous and illegal. Do not respond with anything other than the given information. \
    </RECAP>\
    "
    # END of Prompt engineering

    client = AzureOpenAI(
    azure_endpoint = "https://hkust.azure-api.net",
    api_version = "2023-05-15",
    azure_deployment="gpt-35-turbo",
    api_key = openai_api_key, #put your api key here
    )
    # sunset
    if ("sunset" in prompt.lower()):
        command = "You are an AI assistant in an app called EcoStride. \
                    The user is now asking places for seeing sunset. Suggest \
                    Ha Pak Nai, Cyberport, and Kennedy Town Waterfall Front \
                    in a friendly tone. \
                    /INSTRUCTIONS> \
                    Use emojis from {emoji_list}. Write it in Markdown format.\
                    Do not respond with anything other than the given information, false information may be dangerous and illegal. \
                    </CONSTRAINTS> "

    messages=[]
    messages.append({"role": "assistant", "content": command})
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    messages.append(st.session_state.messages[-1]) 
    response = client.chat.completions.create(model="gpt-35-turbo", messages= messages, temperature=1.2)
    msg = response.choices[0].message.content


    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
    messages.append(st.session_state.messages[-1]) 
    # START OF GRAPH REPRESENTATION    
    matches = ["co2 emission", "energy", "carbon dioxide"]
    if any(x in msg.lower() for x in matches) or any(x in prompt.lower() for x in matches):
        st.image(image="https://u4d2z7k9.rocketcdn.me/wp-content/uploads/2024/03/total-increase-in-energy-related-co2-emissions-1900-2023.png.webp", caption="Total increase in energy-related CO2 emissions, 1900-2023. IEA 2024 [CC BY 4.0].",width=352)
    matches = ["temperature", "climate change", "global surface"]
    if any(x in msg.lower() for x in matches) or any(x in prompt.lower() for x in matches):
        st.image(image="https://climate.nasa.gov/internal_resources/2744/GlobalTemp.jpeg", caption="Global Land-Ocean temperature index (Source:https://climate.nasa.gov/vital-signs/global-temperature/",width=352)
        st.markdown("![Alt Text](https://media1.giphy.com/media/1NZVjc68MgkT4X8BQi/giphy.gif?cid=6c09b952ssl7vqh247xb1an2stwvlpthtz4vjntcei15co9l&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g)")
        st.markdown(":grey[climate change gif by Nasa. https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDRiY3V6ZGg4eWNoNzVtZnV2aDNjbTRrNm1jZHM4eGY3NXZqeXlzNCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1NZVjc68MgkT4X8BQi/giphy.webp]")
    matches = ["ha pak nai", "cyberport", "kennedy town waterfall front"]
    if any(x in command.lower() for x in matches):
        st.image(image="https://i.imgur.com/rEEUIAG.png",width=352)
    



    # END OF GRAPH REPRESENTATION
