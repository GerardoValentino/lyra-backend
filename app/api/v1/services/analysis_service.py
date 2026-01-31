import httpx

async def analyze_song_lyrics(
    message: str,
    lyrics: str,
    api_key: str
) -> dict:
    url = "https://apifreellm.com/api/v1/chat"

    prompt = f"{message}\n\nLyrics:\n{lyrics}"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {"message": prompt}

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
