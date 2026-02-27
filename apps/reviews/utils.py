import requests
from functools import lru_cache

# -----------------------------------------------------------------------------
# AniList API Integration Utilities
# -----------------------------------------------------------------------------

@lru_cache(maxsize=128)
def get_anime_title(media_id):
    """
    Fetch anime title from AniList API using the media_id.
    Cached to avoid repeated API calls for the same ID.
    Returns the title or None if not found.
    """
    url = 'https://graphql.anilist.co'
    
    # GraphQL query to retrieve specific media metadata
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
        # Request with a 3-second timeout to prevent stalling the internal API
        response = requests.post(url, json={'query': query, 'variables': variables}, timeout=3)
        
        if response.status_code == 200:
            data = response.json()
            title_data = data.get('data', {}).get('Media', {}).get('title', {})
            
            # Priority: English title -> Romaji title -> None
            return title_data.get('english') or title_data.get('romaji')
        return None
    except Exception:
        # Fail silently: prevents external API downtime from breaking the local app
        return None

def get_popular_anime(limit=20):
    """
    Fetch a list of popular anime from AniList API.
    Returns a list of anime with id, title, and coverImage.
    """
    url = 'https://graphql.anilist.co'
    
    # GraphQL query to fetch a paginated list of trending titles
    query = '''
    query ($page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            media(type: ANIME, sort: POPULARITY_DESC) {
                id
                title {
                    english
                    romaji
                }
                coverImage {
                    large
                }
                averageScore
                episodes
            }
        }
    }
    '''
    
    variables = {
        'page': 1,
        'perPage': limit
    }
    
    try:
        response = requests.post(url, json={'query': query, 'variables': variables}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            media_list = data.get('data', {}).get('Page', {}).get('media', [])
            
            # Normalize and format the external data for internal use
            anime_list = []
            for anime in media_list:
                title_data = anime.get('title', {})
                anime_list.append({
                    'id': anime.get('id'),
                    'title': title_data.get('english') or title_data.get('romaji'),
                    'cover_image': anime.get('coverImage', {}).get('large'),
                    'average_score': anime.get('averageScore'),
                    'episodes': anime.get('episodes')
                })
            
            return anime_list
        return []
    except Exception:
        return []