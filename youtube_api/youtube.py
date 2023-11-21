import googleapiclient.discovery

class Video:
    def __init__(self, image_path, title, video_id):
        self.image_path = image_path
        self.title = title
        self.video_id = video_id

class Youtube:
<<<<<<< HEAD
    def __init__(self, api_key="AIzaSyC9QU4ZsJV92E6rE8obuZbs5Nwgpt_9zTM"):
=======
    def __init__(self, api_key="AIzaSyCOAC1zDhNmo5g69jmVCRlN8M7Cn00tqF8"):
>>>>>>> 92ff310ab7f979f0514204a7aec23a72cb533c9d
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    def search(self, query="Software Quality Assurance", num_results=12):
        search_response = self.youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=num_results,
            type="video"
        ).execute()

        results = []
        for search_result in search_response.get("items", []):
            video_id = search_result["id"]["videoId"]
            video_title = search_result["snippet"]["title"]
            video_image = search_result["snippet"]["thumbnails"]["high"]["url"]
            video = Video(video_image, video_title, video_id)
            results.append(video)
        return results