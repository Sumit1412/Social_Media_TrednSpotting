from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd



class youTubeData:
    @staticmethod
    def extract_youtube_info(SerachString,api_service_name,api_version,DEVELOPER_KEY):
        KeyWord = SerachString
        top_video = 5
        videosSearch = VideosSearch(KeyWord+' Review', limit = top_video)
        reponse_dict =  videosSearch.result()

        # Create YouTube Object
        youtube = build(api_service_name, api_version,
                        developerKey=DEVELOPER_KEY)


        results= []

        for item in reponse_dict['result']:
            result = item
            try:
                transcript = YouTubeTranscriptApi.get_transcript(result['id'])
                trns_result = ""
                for i in transcript:
                    trns_result += ' ' + i['text']
            except:
                trns_result = "No transcript available"

            ch_request = youtube.channels().list(
            part='statistics',
            id=result['channel']['id'])


            ch_response = ch_request.execute()

            sub = ch_response['items'][0]['statistics']['subscriberCount']
            vid = ch_response['items'][0]['statistics']['videoCount']
            views = ch_response['items'][0]['statistics']['viewCount']

            results.append([
                result['type'],
                result['id'],
                result['title'],
                result['publishedTime'],
                result['duration'],
                result['viewCount']['text'],
                result['viewCount']['short'],
                result['descriptionSnippet'],
                result['channel']['name'],
                result['channel']['id'],
                result['link'],
                trns_result,
                sub,
                vid,
                views
                ]
            )
        detailed_df = pd.DataFrame(results, columns=['type', 'Video_id', 'title', 'publishedTime', 'duration', 'text', 'short', \
                                            'descriptionSnippet', 'name', 'Channel_id', 'link','trns_result',\
                                            'Subscriber','Videos_Count','Channel_Views'])
        return detailed_df
    
    
    @staticmethod
    def extract_comments(SerachString,api_service_name,api_version,DEVELOPER_KEY):
        KeyWord = SerachString
        top_video = 5
        videosSearch = VideosSearch(KeyWord+' Review', limit = top_video)
        reponse_dict =  videosSearch.result()
        api_service_name = api_service_name
        api_version = api_version
        DEVELOPER_KEY = DEVELOPER_KEY
        all_comments = []
        df = pd.DataFrame(all_comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text','Video_id'])
        for item in reponse_dict['result']:
            result = item
            youtube = build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)
            try:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=result['id'],
                    maxResults=10000
                )
                response = request.execute()

                comments = []

                for item in response['items']:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments.append([
                        comment['authorDisplayName'],
                        comment['publishedAt'],
                        comment['updatedAt'],
                        comment['likeCount'],
                        comment['textDisplay'],
                        result['id']
                    ])
                    data = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text','Video_id'])
            except:
                pass
            df = pd.concat([df,data],ignore_index=True)

        return df


