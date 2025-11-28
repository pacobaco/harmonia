import torch, librosa, numpy as np
from transformers import CLAPProcessor, CLAPModel
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

processor = CLAPProcessor.from_pretrained("laion/CLAP")
clap_model = CLAPModel.from_pretrained("laion/CLAP")

def extract_mir_features(audio, sr):
    rms = np.mean(librosa.feature.rms(y=audio))
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
    tempo, _ = librosa.beat.beat_track(y=audio, sr=sr)
    return {"rms": float(rms), "spectral_centroid": float(spectral_centroid), "tempo": float(tempo)}

def extract_clap_embedding(audio, sr):
    inputs = processor(audio, sampling_rate=sr, return_tensors="pt")
    with torch.no_grad():
        embedding = clap_model.get_audio_features(**inputs)
    return embedding.squeeze().numpy()

def generate_summary(track_name, album_name, mir_features, clap_embedding):
    prompt = f"""Track: {track_name}
Album: {album_name}
MIR features: {mir_features}
CLAP embedding length: {len(clap_embedding)}

Produce a concise track description mentioning energy, mood, and musical character."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def process_track(file_path, track_name, album_name):
    audio, sr = librosa.load(file_path, sr=16000, mono=True)
    mir_features = extract_mir_features(audio, sr)
    clap_embedding = extract_clap_embedding(audio, sr)
    summary = generate_summary(track_name, album_name, mir_features, clap_embedding)
    return {"track_name": track_name, "album": album_name, "mir_features": mir_features, "clap_embedding_length": len(clap_embedding), "summary": summary}
