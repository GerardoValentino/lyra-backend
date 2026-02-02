from pydantic import BaseModel, Field

class SongRequest(BaseModel):
    artist: str = Field(min_length=3, max_length=20)
    song_name: str = Field(min_length=3)

class SongAnalyticsRequest(BaseModel):
    #message: str = Field(min_length=3, max_length=10000)
    song_lyrics: str = Field(min_length=3)