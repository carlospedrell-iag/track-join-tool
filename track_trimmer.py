import os, re
from pydub import AudioSegment
from mutagen import File

INPUT_DIR = "input"
OUTPUT_FILE = "output.wav"
CROSSFADE_DURATION_MS = 20


def get_track_number(filepath):
    # Try metadata first
    try:
        audio = File(filepath)
        track = audio.get("tracknumber")
        if track:
            return int(str(track[0]).split('/')[0])
    except Exception:
        pass

    # Fallback: Try to extract a leading number from the filename
    filename = os.path.basename(filepath)
    match = re.match(r'^(\d+)', filename)
    if match:
        return int(match.group(1))

    # Otherwise, try to find any number in the filename
    match = re.search(r'(\d+)', filename)
    if match:
        return int(match.group(1))

    return float('inf')  # Unsortable stuff goes at the end


def detect_leading_silence(sound, silence_thresh=-50.0, chunk_size=10):
    trim_ms = 0
    assert chunk_size > 0
    while trim_ms < len(sound) and sound[trim_ms:trim_ms+chunk_size].dBFS < silence_thresh:
        trim_ms += chunk_size
    return trim_ms


def trim_silence(audio, silence_thresh=-50.0, chunk_size=10):
    start_trim = detect_leading_silence(audio, silence_thresh, chunk_size)
    end_trim = detect_leading_silence(audio.reverse(), silence_thresh, chunk_size)
    duration = len(audio)
    return audio[start_trim:duration - end_trim]


def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.mp3', '.wav', '.flac', '.ogg'))]
    files.sort(key=lambda f: get_track_number(os.path.join(INPUT_DIR, f)))

    final_audio = AudioSegment.silent(duration=0)

    for file in files:
        filepath = os.path.join(INPUT_DIR, file)
        print(f"Processing {file}...")
        audio = AudioSegment.from_file(filepath)

        print(f"Type of audio: {type(audio)}")
        
        trimmed_audio = trim_silence(audio)

        # Fade edges to smooth transitions
        faded_audio = trimmed_audio.fade_in(5).fade_out(5)

        faded_audio = trimmed_audio

        if len(final_audio) == 0:
            final_audio = faded_audio
        else:
            final_audio = final_audio.append(faded_audio, crossfade=CROSSFADE_DURATION_MS)

    print("Normalizing final mix...")
    normalized_audio = final_audio.normalize()

    print(f"Exporting to {OUTPUT_FILE}...")
    normalized_audio.export(OUTPUT_FILE, format="wav")
    print("Done.")


if __name__ == "__main__":
    main()
