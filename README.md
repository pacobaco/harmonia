# Harmonia

**Harmonia** is a powerful and flexible music analysis utility that helps artists, producers, and enthusiasts explore and understand albums and tracks in depth.

## Features

- Audio preprocessing (resample, normalize)  
- MIR feature extraction (RMS, spectral centroid, tempo)  
- CLAP embedding extraction  
- Optional MERT embeddings for musical structure  
- Track-level summaries using OpenAI LLM  
- Storage of summaries in JSON  
- FastAPI endpoints for easy programmatic access  

## Usage

### 1. Organize your audio
Place your WAV/MP3 tracks in album folders:

```
audio/
├── Album1/
│   ├── Track1.wav
│   └── Track2.wav
├── Album2/
│   ├── Track1.wav
│   └── Track2.wav
```

### 2. Run the FastAPI server
```bash
uvicorn main:app --reload
```

### 3. API Endpoints
- POST /process_album/ : Process a folder containing an album  
- GET /albums/ : List all albums processed  
- GET /album/{album_name} : Get summaries for a specific album  
- GET /track/{track_name} : Get a summary for a specific track  

### 4. Docker Usage
```bash
docker build -t harmonia .
docker run -p 8000:8000 harmonia
```

## Repository Structure
```
harmonia/
├── main.py             # FastAPI backend
├── processing.py       # Audio preprocessing & embedding pipeline
├── audio/              # Folder with album tracks
├── data/
│   └── track_summaries.json
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .github/workflows/deploy.yml
```

## Requirements
See requirements.txt. Install dependencies using:

```bash
pip install -r requirements.txt
```

## Future Enhancements
- Interactive dashboard to visualize tracks, albums, and embeddings  
- Similarity search across albums using embeddings  
- Batch processing for large catalogs  
- Optional MERT integration for track structure analysis

**Harmonia** transforms your album collections into a rich source of musical insights.
