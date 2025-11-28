from fastapi import FastAPI
from processing import process_track
import os, glob, json

app = FastAPI(title="Harmonia Music Analyzer")

DATA_FILE = "data/track_summaries.json"
os.makedirs("data", exist_ok=True)

# Load existing summaries if any
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        track_summaries = json.load(f)
else:
    track_summaries = []

@app.post("/process_album/")
async def process_album(album_name: str, folder_path: str):
    album_results = []
    track_files = glob.glob(os.path.join(folder_path, "*.wav")) + glob.glob(os.path.join(folder_path, "*.mp3"))
    for file_path in track_files:
        track_name = os.path.splitext(os.path.basename(file_path))[0]
        result = process_track(file_path, track_name, album_name)
        album_results.append(result)
        track_summaries.append(result)

    with open(DATA_FILE, "w") as f:
        json.dump(track_summaries, f, indent=2)

    return {"album": album_name, "tracks_processed": len(album_results), "summaries": album_results}

@app.get("/albums/")
async def list_albums():
    albums = list({track["album"] for track in track_summaries})
    return {"albums": albums}

@app.get("/album/{album_name}")
async def get_album_summary(album_name: str):
    album_tracks = [t for t in track_summaries if t["album"].lower() == album_name.lower()]
    return {"album": album_name, "tracks": album_tracks}

@app.get("/track/{track_name}")
async def get_track_summary(track_name: str):
    track = next((t for t in track_summaries if t["track_name"].lower() == track_name.lower()), None)
    if track:
        return track
    return {"error": "Track not found"}
