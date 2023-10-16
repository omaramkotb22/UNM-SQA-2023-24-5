import googleapiclient.discovery


def search_youtube_videos(api_key, query, num_results=5):
    # Create a YouTube Data API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Perform the search request, specifying type=video
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=num_results,
        type="video"
    ).execute()

    # Process and display the search results
    for idx, search_result in enumerate(search_response.get("items", []), start=1):
        video_id = search_result["id"]["videoId"]
        video_title = search_result["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        print(f"Result #{idx}:")
        print(f"Title: {video_title}")
        print(f"Video URL: {video_url}")
        print("\n")


if __name__ == "__main__":
    # Replace 'YOUR_API_KEY' with your actual YouTube Data API key
    api_key = "AIzaSyD6Wp2WzfDrSnnpOq-Mxb2m3QDFfisBlqY"

    # Replace 'YOUR_SEARCH_QUERY' with the query you want to search for
    search_query = "Software Quality Assurance"

    # Specify the number of results you want (default is 5)
    num_results = 12

    search_youtube_videos(api_key, search_query, num_results)
