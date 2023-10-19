import googleapiclient.discovery

class Youtube:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    def search(self, query, num_results=5):
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
            results.append({
                "title": video_title,
                "id": video_id,
            })

        return results
    
