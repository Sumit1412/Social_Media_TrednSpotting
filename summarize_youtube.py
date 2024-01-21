from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import openai
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain_openai import ChatOpenAI
from extract_youtube import youTubeData as yt

openai.api_key = "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"
gpt_model="gpt-3.5-turbo-16k-0613"
chat = ChatOpenAI(temperature=0.0, openai_api_key = openai.api_key)

# Summarizing Transcript
response_schemas =[ResponseSchema(name="Summary",
                                 description="A detailed summary that analyses the youtubes \
                                 transcript like a data scientist to build persona of the product."),
                ]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()


PROMPT_TEMPLATE_transcripts = """
You are a unbaised Automobile expert task is to build product persona based on
{data} provided by youtuber.\
Incase No transcript available dont frame by persona.simply specify no\
transcript available.
Summarize the keys insights of the review. You have to consider certain below\
listed factors while building persona.\
1) Safety\
2) Build Quality\
3) Appearance\
4) Fuel economy\
5) Affordablity\

{format_instructions}
"""


prompt_template_trans = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_transcripts)


def summarization_func_trans(df,prompt_template,video_id,data_col):
      data_string = ".".join(df[df['Video_id']==video_id][data_col])
      details = prompt_template.format_messages(
                                    data=data_string,
                                    format_instructions=format_instructions
                                    )
      response = chat(details)
      output_dict = output_parser.parse(response.content)
      output_dict['video_id'] = video_id
      return output_dict
  
def data_summarizer(rslt_list:list,key):
    summary_all = ""
    for i in range(0,len(rslt_list)):
        if rslt_list[i][key] == "No transcript available.":
            continue
        else:
            summary_all = summary_all +'|'+ rslt_list[i][key]
    return summary_all


PROMPT_TEMPLATE_final_transcripts = """
You are a unbaised Automobile expert task is to build product persona based on
{data} provided by youtuber.\
Summarize the keys insights strictly in 100 words. You have to consider certain below\
listed factors while building persona. Provide the final output as bullet pointers with html\
<li> tags.\
1) Safety\
2) Build Quality\
3) Appearance\
4) Fuel economy\
5) Affordablity\

Also dont't repeat information and don't assume anything.

{format_instructions}
"""

prompt_template_final_trans = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_final_transcripts)

  
def clean_and_process_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

    # Join tokens back into a cleaned text
    cleaned_text = ' '.join(tokens)

    return cleaned_text

  

response_schemas =[ResponseSchema(name="Summary",
                                 description="A detailed summary that analyses the commnets like a data scientist"),
                ResponseSchema(name="Positivity_Rate",
                                 description="Overall positivity rate in terms of percentage"),
                ResponseSchema(name="Negativity_Rate",
                                 description="Overall negativity rate in terms of percentage"),
                ResponseSchema(name="Safety",
                                 description="Breif Summary over Saftey aspect"),
                ResponseSchema(name="Build_Quality",
                                 description="Breif Summary Build Quality aspect"),
                ResponseSchema(name="Appearance",
                                 description="Breif Summary Appearance aspect"),
                ResponseSchema(name="Fuel_Economy",
                                 description="Breif Summary Fuel economy aspect"),
                ResponseSchema(name="Affordability",
                                 description="Breif Summary Affordability aspect")
                ]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

PROMPT_TEMPLATE_Comments = """
As a seasoned Social Media Trend Analyst with over 10 years of expertise,\
you excel in tracking and comprehending evolving trends and deeply understanding\
user reviews. Your current assignment involves evaluating a {data} of social media\
comments, delineated by a pipe operator.

Your objective is to meticulously analyze each comment, deduce the overall \
sentiment, and present a concise summary that includes the positivity and \
negativity rates in percentage form. The outcome should be presented in JSON\
format.\

JSON Format:\
  "summary": "A Breif summary of overall comments",
  "Positivity_Rate": Score,
  "Negativity_Rate": Score,
  "Safety":Users Positive views and Negative views over Saftey aspect,
  "Build_Quality": Users Positive views and Negative views over Build Quality aspect,
  "Appearance": Users Positive views and Negative views over Appearance aspect,
  "Fuel_Economy": Users Positive views and Negative views over Fuel Economy aspect,
  "Affordability": Users Positive views and Negative views over Affordability aspect,

Please adhere to the provided format instructions while delivering the results.

{format_instructions}

"""

prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_Comments)

def summarization_func_comment(df,prompt_template,video_id,data_col):
      data_string = "|".join(df[df['Video_id']==video_id][data_col])
      details = prompt_template.format_messages(
                                    data=data_string,
                                    format_instructions=format_instructions
                                    )
      response = chat(details)
      output_dict = output_parser.parse(response.content)
      output_dict['video_id'] = video_id
      return output_dict
  
PROMPT_TEMPLATE_final_comments = """
You are a unbaised Automobile expert task is to summarize {data} delineated by\
a pipe operator.\
Take averag of positivity and negativity rate and display it as final score.
Summarize the keys insights strictly in 50 words. 
1) Safety\
2) Build Quality\
3) Appearance\
4) Fuel economy\
5) Affordablity\

Also dont't repeat information and don't assume anything.

{format_instructions}
"""

prompt_template_final_comments = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_final_comments)


PROMPT_TEMPLATE_sentiment = """
Take average of {data} delineated by a pipe operator and display it as final score.\
just provide output as single float value.

example:
Summary:'56.6'

{format_instructions}
"""

prompt_template_final_sentiment = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_sentiment)


def summarization_func_trans_final(prompt_template,data_string):
      details = prompt_template.format_messages(
                                    data=data_string,
                                    format_instructions=format_instructions
                                    )
      response = chat(details)
      output_dict = output_parser.parse(response.content)
      return output_dict