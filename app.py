"""Streamlit app for Industrial Geosynthetics."""

# To run: python -m streamlit run app.py
import logging
import streamlit as st
from functions_openai import OpenAi
import difflib
import os
from PIL import Image

def generate_text(prompt):
    if st.session_state.n_requests >= 5:
        st.session_state.text_error = "Too many requests. Please wait a few seconds before generating another answer."
        logging.info(f"Session request limit reached: {st.session_state.n_requests}")
        st.session_state.n_requests = 1
        return
    
    st.session_state.answer = ""

    if not prompt:
       st.session_state.text_error = "Please enter a topic"
    
   
    with st.spinner("This might take a couple minutes, fetching an answer..."):
        open_ai_function = OpenAi()
        st.session_state.text_error = ""
        st.session_state.n_requests += 1
        print(prompt)
        st.session_state.answer = (
            open_ai_function.retrieve_prompt(prompt)
            #open_ai_function.prompt_organized(prompt)
        )
        logging.info(
            f"Prompt: {prompt}\n"
            f"Answer: {st.session_state.answer}"
        )

def find_most_similar_name(text, names):
    """
    Loops through a list of names and returns the one with the highest similarity score to a given text.
    """
    highest_score = 0
    most_similar_name = ""
    for name in names:
        score = difflib.SequenceMatcher(None, text.lower(), name.lower()).ratio()
        print(name, score)
        if score > highest_score:
            highest_score = score
            most_similar_name = name
    if text == 'Woven geotextile':
        most_similar_name = 'Product coming soon.....png'
        
    if highest_score < 0.7:
        most_similar_name = 'Product coming soon.....png'
    return most_similar_name

def list_files_in_directory(directory_path):
    """
    Stores the names of all files in a directory in a list.
    """
    files = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            files.append(filename)
    return files

def bold_product(text, product_name, project_name):
    text = text.replace(str.lower(project_name) + ',', str.lower(f"**{project_name}**") + ',') 
    text = text.replace(project_name, f"**{project_name}**")
    text = text.replace('Specs:', "**Specs:**")
    text = text.replace(product_name, f"**{product_name}**")
    return text

st.set_page_config(page_title="Industrial Geosynthetics", page_icon="🤖")

if "answer" not in st.session_state:
    st.session_state.answer = ""
if "text_error" not in st.session_state:
    st.session_state.text_error = ""
if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

# Render Streamlit page
main_title = '<h1 style="text-align: center; color: #262730; font-size: 35px;"><strong>Your One stop Geosynthetic Shop<strong></h1>' 
st.markdown(main_title, unsafe_allow_html=True)
blue_header = '<p style="text-align: center; color:#14A0DF; font-size: 27px;"><strong>What project are you looking to undertake?<strong></p> <p style="text-align: center; color:#14A0DF; font-size: 20px;">Let our AI find the optimal geosynthetic product for you.</p>'
st.markdown(blue_header, unsafe_allow_html=True)
blue_mini_header = '<p style="text-align: center; color:#14A0DF; font-size: 27px;"><strong>Let our AI find the optimal geosynthetic product for you.<strong></p>'

buff1, col2_b, buff1 = st.columns([1,7,1])
project_input = col2_b.text_input(label= "", placeholder="Type here... ex: 'I want to build a home koi pond, which product fits best?' ")
primaryColor = st.get_option("theme.primaryColor")
textColor = st.get_option("theme.textColor")
col1_a, col2_a, col3_a = st.columns([1.1,1,1])
s = f"""
<style>
div.stButton > button:first-child {{background-color: white; color:#14a0df ; font-size:20px ; border: 1px solid {primaryColor}; border-radius:20px 20px 20px 20px; }}
div.stButton > button:hover {{background-color: #14a0df;color:white; font-size:20px ; border: 1px solid {primaryColor}; border-radius:20px 20px 20px 20px;}}
<style>
"""
st.markdown(s, unsafe_allow_html=True)
start = col2_a.button(label="Find my ideal product")

if start and project_input:
    generate_text(project_input)
    text_spinner_placeholder = st.empty()
    if st.session_state.text_error:
        st.error(st.session_state.text_error)

    if st.session_state.answer:
        print(st.session_state.answer)
        product_name = str(st.session_state.answer).split('Product: ')[-1]
        project_name = str(st.session_state.answer).split('Project: ')[-1].split('Product: ')[0]
        print(product_name, project_name)
        answer = bold_product(str(st.session_state.answer), product_name, project_name)
        st.markdown(answer.split('Project: ')[0])
        col1_c, col2_c, col3_c = st.columns([1,5,1])
        images = list_files_in_directory('product_images')
        product_image = find_most_similar_name(product_name, images)
        image = Image.open('product_images/' + str(product_image))
        col2_c.image(image, caption=product_name, use_column_width=True) 
        if product_name == 'HDPE Liner Lite/Pond Liner' or product_name == 'LLDPE Liners & Geomembranes':
            extension = str(product_name) + ' is really simple to set up and with our Liner Glue Tap Roll, things just got simpler. This is a double-sided waterproof tape that can be used along the seams in joining the seals of the geomembranes. \nCheck it out below and see our easy 4-step process on how you can use it to help with your' + str(project_name)
            st.markdown(extension)
            image2 = Image.open('product_images/Liner Glue Tape Roll.png')
            col3_c, col4_c, col5_c = st.columns([1,5,1])
            col4_c.image(image2, caption='Liner Glue Tape Roll', use_column_width=True)   
        
             
