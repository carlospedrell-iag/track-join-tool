# Track Join Tool

A Python utility for processing audio tracks from a DJ mix or collection, removing silence, and combining them into a single audio file, also applying normalization.

## Overview

Track Join Tool is designed to:
- Process multiple audio files (MP3, WAV, FLAC, OGG)
- Trim silence from the beginning and end of each track
- Apply smooth crossfades between tracks
- Normalize the final audio output
- Sort tracks by their track numbers (from metadata or filename)

## Requirements

- Python 3.x
- FFmpeg installed on your system (required for audio processing)
- Required libraries:
  - pydub
  - mutagen

## Installation

1. Clone or download this repository
2. Install FFmpeg:
   - macOS: `brew install ffmpeg`
   - Linux: `apt-get install ffmpeg`
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
3. Install the required dependencies (Recommend using python venv):

```bash
pip install -r requirements.txt
```

## Usage

1. Place your audio files in the `input` directory
2. Run the script:

```bash
python track_trimmer.py
```

3. The processed audio will be saved as `output.wav` in the project directory

## Configuration

You can modify the following variables in `track_trimmer.py` to customize behavior:

- `INPUT_DIR`: The directory containing input audio files (default: "input")
- `OUTPUT_FILE`: The filename for the processed output (default: "output.wav")
- `CROSSFADE_DURATION_MS`: Duration of crossfades between tracks in milliseconds (default: 20)

## How It Works

The script:
1. Reads all audio files from the input directory
2. Sorts them by track number (extracted from metadata or filename)
3. Processes each track to remove silence
4. Applies fade-in and fade-out effects to smooth transitions
5. Concatenates all tracks with crossfades
6. Normalizes the final audio
7. Exports the result to the specified output file

## License

MIT License
