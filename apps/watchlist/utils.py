import requests
from functools import lru_cache


@lru_cache(maxsize=128)
def get_anime_title(media_id):
    """
    Fetch anime title from AniList API using the media_id.
    Cached to avoid repeated API calls for the same ID.
    Returns the title or None if not found.
    """
    url = 'https://graphql.anilist.co'
    
    query = '''
    query ($id: Int) {
        Media(id: $id, type: ANIME) {
            title {
                english
                romaji
            }
        }
    }
    '''
    
    variables = {'id': media_id}
    
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            title_data = data.get('data', {}).get('Media', {}).get('title', {})
            # Prefer English title, fall back to Romaji
            return title_data.get('english') or title_data.get('romaji')
        return None
    except Exception:
        # If AniList is down or times out, don't break the entire API
        return None