import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import os
import subprocess

def download_video_audio():
    url = url_entry.get()
    choice = choice_var.get()
    save_path = path_var.get()

    if not url:
        messagebox.showwarning("Input Error", "Please enter a YouTube URL")
        return
    if not save_path:
        messagebox.showwarning("Input Error", "Please select a folder to save the file")
        return

    try:
        yt = YouTube(url)
        
        if choice == "Audio Only":
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            out_file = audio_stream.download(output_path=save_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            messagebox.showinfo("Success", f"Audio downloaded successfully:\n{new_file}")

        elif choice == "Video with Audio":
            # Try to get progressive stream with audio first (best quality)
            progressive_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if progressive_stream:
                out_file = progressive_stream.download(output_path=save_path)
                messagebox.showinfo("Success", f"Video downloaded successfully:\n{out_file}")
            else:
                # No progressive stream available (likely 1080p or higher)
                # Download highest video-only and audio-only streams
                video_stream = yt.streams.filter(adaptive=True, only_video=True, file_extension='mp4').order_by('resolution').desc().first()
                audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                if not video_stream or not audio_stream:
                    messagebox.showerror("Error", "Could not find suitable video/audio streams to download")
                    return

                video_file = video_stream.download(output_path=save_path, filename="video_temp.mp4")
                audio_file = audio_stream.download(output_path=save_path, filename="audio_temp.mp4")
                
                # Merge with ffmpeg
                merged_file = os.path.join(save_path, yt.title.replace(" ", "_") + ".mp4")
                cmd = [
                    'ffmpeg',
                    '-y',  # overwrite output file if exists
                    '-i', video_file,
                    '-i', audio_file,
                    '-c', 'copy',
                    merged_file
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Clean up temp files
                os.remove(video_file)
                os.remove(audio_file)
                
                messagebox.showinfo("Success", f"Video downloaded and merged successfully:\n{merged_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download:\n{e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_var.set(folder_selected)

root = tk.Tk()
root.title("YouTube Video & Audio Downloader")

tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

tk.Label(root, text="Download Option:").pack(pady=5)
choice_var = tk.StringVar(value="Video with Audio")
choices = ["Video with Audio", "Audio Only"]
choice_menu = tk.OptionMenu(root, choice_var, *choices)
choice_menu.pack(pady=5)

tk.Label(root, text="Save To Folder:").pack(pady=5)
path_var = tk.StringVar()
path_entry = tk.Entry(root, textvariable=path_var, width=50)
path_entry.pack(side=tk.LEFT, padx=10, pady=5)
browse_btn = tk.Button(root, text="Browse", command=browse_folder)
browse_btn.pack(side=tk.LEFT, pady=5)

download_btn = tk.Button(root, text="Download", command=download_video_audio)
download_btn.pack(pady=20)

root.mainloop()
