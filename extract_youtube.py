from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

KeyWord = "String Energy Drink"
top_video = 1

videosSearch = VideosSearch(KeyWord+' Review', limit = top_video)
reponse_dict =  videosSearch.result()

results= []

for item in reponse_dict['result']:
    result = item
    results.append([
        result['type'],
        result['id']]
    )
df = pd.DataFrame(results, columns=['type', 'id'])

df
# for i in range(0,len(reponse_dict['result'])):
#     print(reponse_dict['result'][i]['type'])
#     print(reponse_dict['result'][i]['id'])
#     print(reponse_dict['result'][i]['title'])
#     print(reponse_dict['result'][i]['publishedTime'])
#     print(reponse_dict['result'][i]['duration'])
#     print(reponse_dict['result'][i]['viewCount']['text'])
#     print(reponse_dict['result'][i]['viewCount']['short'])
#     print(reponse_dict['result'][i]['descriptionSnippet'])
#     print(reponse_dict['result'][i]['channel']['name'])
#     print(reponse_dict['result'][i]['channel']['id']) 
#     print(reponse_dict['result'][i]['accessibility']['title'])
#     print(reponse_dict['result'][i]['link'])
#     print(reponse_dict['result'][i]['shelfTitle'])
#     try:
#         YouTubeTranscriptApi.get_transcript(reponse_dict['result'][i]['id'])
#         transcript = YouTubeTranscriptApi.get_transcript(reponse_dict['result'][i]['id'])
#         trns_result = ""
#         for i in transcript:
#             trns_result += ' ' + i['text']
#         print(len(trns_result))
#     except:
#         trns_result = "No transcript available"
#     print(trns_result)
    

