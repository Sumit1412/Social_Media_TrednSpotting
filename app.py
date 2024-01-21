import streamlit as st
from extract_youtube import youTubeData as yt
import summarize_youtube as sy
import matplotlib.pyplot as plt
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
import base64
import os
import re


def generate_donut_chart(positivity_percentage, negativity_percentage):
    # Data for the donut chart
    data = [positivity_percentage, negativity_percentage]
    colors = ['#66ff66', '#ff6666']  # Green for positivity, red for negativity

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(data, autopct='%1.1f%%', startangle=90, colors=colors)

    # Draw a white circle in the center to create a donut chart
    centre_circle = plt.Circle((0,0),0.50,fc='white')
    ax.add_artist(centre_circle)

    # Equal aspect ratio ensures the pie chart is circular
    ax.axis('equal')

    return fig

LOGO_IMAGE = "yt.png"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.environ["YouTube_API_KEY"]


st.markdown(
    """
    <style>
    .container {
        display: flex;
        height: 1px;
        width : 800px;
        align-items: center;
    }
    .header {
    margin: 1px 0;
    }
    .logo-text {
        font-weight:700 !important;
        font-size:50px !important;
        color: #008080 !important;

    }
    .logo-img {
        width: 150px;
        height: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{base64.b64encode(open(LOGO_IMAGE, "rb").read()).decode()}">
        <p class="logo-text">Automobile Persona App</p>
    </div>
    """,
    unsafe_allow_html=True
)

def search_videos(query,api_service_name = "youtube",api_version = "v3",DEVELOPER_KEY = DEVELOPER_KEY):
    trans_df = yt.extract_youtube_info(query,api_service_name,api_version,DEVELOPER_KEY)
    return trans_df
    # st.write(f"Searching videos for: {title_df}")

def search_comments(query,api_service_name = "youtube",api_version = "v3",DEVELOPER_KEY = DEVELOPER_KEY):
    comments_df = yt.extract_comments(query,api_service_name,api_version,DEVELOPER_KEY)
    return comments_df
    # st.write(f"Searching videos for: {title_df}")
    

# Create a layout with two columns
search_column, button_column = st.columns([5,1])

# Add a text input for the search query in the first column
search_query = search_column.text_input( "")

# Add a button to trigger the search in the second column
if button_column.button("Search"):
    # Trigger the search function
    data = search_videos(search_query)  
    data['trns_result'] = data['trns_result'].apply(sy.clean_and_process_text)
    comments_data = search_comments(search_query)
    comments_data['Cleaned_Text'] = comments_data['text'].apply(sy.clean_and_process_text)
    video_list = data['Video_id'].unique().tolist()
    result_list_trans = [sy.summarization_func_trans(data,sy.prompt_template_trans,x,'trns_result') for x in video_list]
    summary_all = sy.data_summarizer(result_list_trans,"Summary")
    final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_trans,summary_all)
    result_list = [sy.summarization_func_comment(comments_data,sy.prompt_template,x,'Cleaned_Text') for x in video_list]
    safety_summary = sy.data_summarizer(result_list,"Safety")
    safety_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_comments,safety_summary)
    build_quality_summary = sy.data_summarizer(result_list,"Build_Quality")
    build_quality_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_comments,build_quality_summary)
    appearance_summary = sy.data_summarizer(result_list,"Appearance")
    appearance_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_comments,appearance_summary)
    affordability_summary = sy.data_summarizer(result_list,"Affordability")
    affordability_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_comments,affordability_summary)
    positivity_summary = sy.data_summarizer(result_list,"Positivity_Rate")
    positivity_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_sentiment,positivity_summary)
    negativity_summary = sy.data_summarizer(result_list,"Negativity_Rate")
    negativity_final_summary = sy.summarization_func_trans_final(sy.prompt_template_final_sentiment,negativity_summary)
    # Create a row of 5 fancy tiles using Markdown and HTML
    tiles = st.columns(5)
    for i in range(5):
        with tiles[i]:
            st.markdown(f"""
                <div class="fancy-tile">
                    <p><b><font size="2">{data.iloc[i,8]}<br>{data.iloc[i,5]}</font>.</b></p>
                </div>
            """, unsafe_allow_html=True)
     
    area = st.columns(2)        
    with area[0]:
        st.markdown(f"""
                    <div class="beautiful-background">
                    <head><b><center>Reviewers Views</center></b></head>
                    <p><b><font size="2">{final_summary['Summary']}</font>.</b></p>
                    </div>"""
                    , unsafe_allow_html=True)
        # st.write("dummay data")
        # st.markdown('</div>', unsafe_allow_html=True)
        # Generate pie chart
    with area[1]:
        fig = generate_donut_chart(float(re.findall(r"[-+]?\d*\.?\d+|\d+", positivity_final_summary['Summary'])[0]),
                                   float(re.findall(r"[-+]?\d*\.?\d+|\d+", negativity_final_summary['Summary'])[0])
                                   )
        

        # Display the donut chart in a styled container
        st.markdown('<div class="donut-chart-container"><head><b><center>Comments Sentiment</center></b></head>', unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)
        
    comments = st.columns(4)
    with comments[0]:
        st.markdown(f"""
                    <div class="beautiful-background">
                    <head><b><center>Safety</center></b></head>
                    <p><b><font size="2">{safety_final_summary['Summary']}</font>.</b></p>
                    </div>"""
                    , unsafe_allow_html=True)
    with comments[1]:
        st.markdown(f"""
                    <div class="beautiful-background">
                    <head><b><center>Build Quality</center></b></head>
                    <p><b><font size="2">{build_quality_final_summary['Summary']}</font>.</b></p>
                    </div>"""
                    , unsafe_allow_html=True)
    with comments[2]:
        st.markdown(f"""
                    <div class="beautiful-background">
                    <head><b><center>Appearance</center></b></head>
                    <p><b><font size="2">{appearance_final_summary['Summary']}</font>.</b></p>
                    </div>"""
                    , unsafe_allow_html=True)
    with comments[3]:
        st.markdown(f"""
                    <div class="beautiful-background">
                    <head><b><center>Affordability</center></b></head>
                    <p><b><font size="2">{affordability_final_summary['Summary']}</font>.</b></p>
                    </div>"""
                    , unsafe_allow_html=True)
    
# Custom HTML and CSS to set container height and size
custom_css = """
<style>
    .st-cf {
        height: 40px; /* Set the height of the container */
        width: 100%;   /* Set the width of the container */
        display: flex;
        align-items: center;
        justify-content: center;
        
    }
    
    .stButton {
        margin-top: 25px; /* Adjust the margin-top value to shift the button downwards */
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# Custom HTML and CSS for a fancy tile
custom_tile_style = """
<style>
    .fancy-tile {
        background-color: #F5F5DC;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
        margin-right: 15px;
        max-height: 150px; /* Set the maximum height of the tile */
        overflow: hidden; /* Enable overflow to hide excess text */
        font-size: 5px;
    }

    .fancy-tile:last-child {
        margin-right: 0;
    }

    .fancy-tile:hover {
        transform: scale(1.05);
    }
    
</style>
"""

# Apply the custom style
st.markdown(custom_tile_style, unsafe_allow_html=True)

# CSS styles to make the tile clickable
st.markdown("""
    <style>
        .clickable-tile {
            cursor: pointer;
            border: 1px solid #ccc;
            padding: 10px;
            margin: 5px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)



area_css = """
<style>
    /* Beautiful background section */
    .beautiful-background {
        background-color: #f0f0f0; /* Set your desired background color */
        padding: 20px;
        margin-top: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Stylish text area */
    .custom-text-area {
        width: 100%;
        height: 200px;
        background-color: #ffffff;
        border: 2px solid #ddd;
        border-radius: 8px;
        margin-top: 40px;
        padding: 10px;
        font-size: 16px;
        box-sizing: border-box;
    }
</style>
"""

# Render custom CSS
st.markdown(area_css, unsafe_allow_html=True)


# Custom CSS styles
custom_css = """
<style>
    /* Styling for the donut chart container */
    .donut-chart-container {
        text-align: center;
        padding: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px; /* Set the desired margin-top value */
    }
</style>
"""

# Render custom CSS
st.markdown(custom_css, unsafe_allow_html=True)



