from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

KeyWord = "String Energy Drink"
top_video = 10
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyBS1QIztU4W_ZO1oZ1EN3T5LEzAHvP17-0"


youtube = build(api_service_name, api_version,
                developerKey=DEVELOPER_KEY)



videosSearch = VideosSearch(KeyWord+' Review', limit = top_video)
reponse_dict =  videosSearch.result()


for i in range(0,len(reponse_dict['result'])):
    print(reponse_dict['result'][i]['type'])
    print(reponse_dict['result'][i]['id'])
    print(reponse_dict['result'][i]['title'])
    print(reponse_dict['result'][i]['publishedTime'])
    print(reponse_dict['result'][i]['duration'])
    print(reponse_dict['result'][i]['viewCount']['text'])
    print(reponse_dict['result'][i]['viewCount']['short'])
    print(reponse_dict['result'][i]['descriptionSnippet'])
    print(reponse_dict['result'][i]['channel']['name'])
    print(reponse_dict['result'][i]['channel']['id']) 
    print(reponse_dict['result'][i]['accessibility'])
    print(reponse_dict['result'][i]['link'])
    print(reponse_dict['result'][i]['shelfTitle'])
    ch_request = youtube.channels().list(
        part='statistics',
        id=reponse_dict['result'][i]['channel']['id']
        )
    ch_response = ch_request.execute()
    print(ch_response)
    total_subscribers = ch_response['items'][0]['statistics']['subscriberCount']
    vid = ch_response['items'][0]['statistics']['videoCount']
    views = ch_response['items'][0]['statistics']['viewCount']
    try:
        YouTubeTranscriptApi.get_transcript(reponse_dict['result'][i]['id'])
        transcript = YouTubeTranscriptApi.get_transcript(reponse_dict['result'][i]['id'])
        trns_result = ""
        for i in transcript:
            trns_result += ' ' + i['text']
        print(len(trns_result))
    except:
        trns_result = "No transcript available"
    print(f"Total video count : {vid}")
    print(f"Total Views all over Video  : {views}")
    print(f"Total Suscriber Count:{total_subscribers}")
    print(trns_result)
    

