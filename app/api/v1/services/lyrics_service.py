import httpx

async def fetch_song_lyrics(artist: str, song_name: str) -> dict:
    url = (
        "https://lrclib.net/api/get"
        f"?artist_name={artist}&track_name={song_name}"
    )

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
