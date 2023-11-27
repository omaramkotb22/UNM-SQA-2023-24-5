import googleapiclient.discovery

class Video:
    def __init__(self, image_path, title, video_id):
        self.image_path = image_path
        self.title = title
        self.video_id = video_id

class Youtube:
    def __init__(self, api_key="AIzaSyDXkqW96fpSrufruRz3WfZKbmbzk_0nCGw"):
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