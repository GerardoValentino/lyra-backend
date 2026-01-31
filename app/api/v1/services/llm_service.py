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

    timeout = httpx.Timeout(
        connect=5.0,
        read=30.0,
        write=10.0,
        pool=5.0
    )

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()