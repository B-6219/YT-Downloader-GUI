
# YT Downloader GUI

A simple Python application with a graphical user interface (GUI) built using Tkinter, that allows users to download YouTube videos with audio or audio-only files easily.

## Features

- Download YouTube videos with audio combined (supports 720p progressive streams or merges video+audio for 1080p+ using `ffmpeg`)  
- Download audio-only files from YouTube videos  
- Choose where to save downloaded files  
- Simple and user-friendly Tkinter interface

## Requirements

- Python 3.x  
- `pytube` library  
- `ffmpeg` installed and added to system PATH for merging video and audio streams  
  - Download from: https://ffmpeg.org/download.html

## Installation

1. Clone or download this repository.  
2. Install required Python package:

```bash
pip install pytube
````

3. Make sure `ffmpeg` is installed and accessible in your system PATH.
   You can test this by running `ffmpeg -version` in your terminal or command prompt.

## Usage

1. Run the Python script:

```bash
python yt_downloader_gui.py
```

2. Enter the YouTube video URL in the input field.
3. Select your download option:

   * **Video with Audio** — Downloads full video with audio combined.
   * **Audio Only** — Downloads audio track only.
4. Choose the folder where you want to save the downloaded file.
5. Click the **Download** button.
6. Wait for the download to complete. A success or error message will be shown.

## Notes

* For videos above 720p, the app downloads video and audio separately and merges them with `ffmpeg`.
* Audio-only downloads are saved as `.mp3` files by renaming the downloaded audio stream (no actual audio format conversion).
* Ensure you have a stable internet connection for downloads.

## License

This project is open-source and free to use.

---

Enjoy downloading your favorite YouTube videos and audio!

