from customtkinter import *
import customtkinter as ctk
from pytubefix import YouTube
import tkinter.filedialog as filedialog
import time
import os
import ffmpeg
import ctypes
import re
import sys

# Function to get the path of the ffmpeg binary
def get_ffmpeg_path():
    # Check if the script is running as a packaged .exe file
    if getattr(sys, 'frozen', False):  
        # If packaged, base_path is the temporary folder where PyInstaller places resources
        base_path = sys._MEIPASS  
    else:  
        # If running from source, base_path is the current script's directory
        base_path = os.path.dirname(__file__)  
    
    # Build the path to the FFmpeg binary within the bundled folder structure
    ffmpeg_path = os.path.join(base_path, 'ffmpeg', 'bin', 'ffmpeg.exe')
    
    return ffmpeg_path


# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# Function to merge video and audio using ffmpeg
def merge_video_audio(video_path, audio_path, output_path):
    if not os.path.exists(video_path) or not os.path.exists(audio_path):
        return
    
    ffmpeg_path = get_ffmpeg_path()
    if not os.path.exists(ffmpeg_path):
        print("FFmpeg binary not found!")
        return

    try:
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)
        ffmpeg_output = ffmpeg.output(video, audio, output_path, vcodec='copy', acodec='aac', strict='experimental')
        ffmpeg.run(ffmpeg_output, cmd=ffmpeg_path, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        print(f"Merge completed successfully! Output saved at: {output_path}")
    except ffmpeg.Error as e:
        print(f"Error occurred while merging: {e.stderr.decode()}")
        return

# Function to download audio
def download_audio(url, path):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            print(f'Downloading audio: {yt.title}')
            audio_stream.download(output_path=path)
            print('Audio download complete!')
        else:
            print('No audio stream available.')
    except Exception as e:
        print(f"Failed to download audio: {e}")

# Function to download video
def download_video(url, resolution, path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(res=resolution, file_extension='mp4', only_video=True).first()
        if not video_stream:
            available_streams = yt.streams.filter(file_extension='mp4', only_video=True)
            print(f"Available video streams: {[s.resolution for s in available_streams]}")

            for s in available_streams:
                if s.resolution and s.resolution.startswith(resolution[0]):
                    video_stream = s
                    break

        audio_stream = yt.streams.filter(only_audio=True).first()
        if video_stream and audio_stream:
            print(f'Downloading video at {resolution} and audio...')
            video_path = os.path.join(path, 'video.mp4')
            audio_path = os.path.join(path, 'audio.mp4')
            video_stream.download(output_path=path, filename='video.mp4')
            audio_stream.download(output_path=path, filename='audio.mp4')
            safe_title = sanitize_filename(yt.title)
            output_path = os.path.join(path, f"{safe_title}.mp4")
            merge_video_audio(video_path, audio_path, output_path)
            os.remove(video_path)
            os.remove(audio_path)
        else:
            print(f"Unable to find video or audio streams at {resolution} resolution.")
    except Exception as e:
        print(f"Failed to download video: {e}")

# Function for shaking the button if a field is not filled
def ShakeButton():
    for _ in range(5):
        btn.place(relx=0.5, rely=0.75, anchor='center', x=5)
        app.update()
        time.sleep(0.05)
        btn.place(relx=0.5, rely=0.75, anchor='center', x=-5)
        app.update()
        time.sleep(0.05)

# Function for browsing the path
def BrowsePath():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path.delete(0, END)
        path.insert(0, selected_path)

# Validate entries before starting download
def validateEntries():
    if not url.get() or not path.get():
        if not url.get():
            url.configure(fg_color='darkred', text_color='white')
        else:
            url.configure(fg_color='white', text_color='#b6bbff')

        if not path.get():
            path.configure(fg_color='darkred', text_color='white')
        else:
            path.configure(fg_color='white', text_color='#b6bbff')

        ShakeButton()
    else:
        inputUrl = url.get()
        inputPath = path.get()
        resolution = combobox.get()

        if not os.path.exists(inputPath):
            os.makedirs(inputPath)

        if checkbox.get() == 1:  # Audio-only checkbox
            try:
                download_audio(inputUrl, inputPath)
            except Exception as e:
                print(f"Error downloading audio: {e}")
        else:
            try:
                download_video(inputUrl, resolution, inputPath)
            except Exception as e:
                print(f"Error downloading video: {e}")

# Function to get the resource path for bundled files
def resource_path(relative_path):
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    except AttributeError:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

# Initialize the application window
app = ctk.CTk()
app.geometry('1080x720')
app.title("YouTube Downloader")

# Set dark mode appearance
set_appearance_mode('dark')

# Load the icon
icon_path = resource_path("YTD icon.ico")  
app.iconbitmap(icon_path)  # Set the app icon

# Set the application UserModel ID for Windows taskbar icon
myappid = 'YTDFinal'  # Unique ID for the app
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Create UI elements
label = CTkLabel(master=app, text='Youtube downloader', font=('Arial', 20), text_color='#b6bbff')
combobox = CTkComboBox(master=app, values=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'])
btn = CTkButton(master=app, text='Download', corner_radius=10, border_width=2, border_color='#b6bbff', command=validateEntries)
path = CTkEntry(master=app, placeholder_text='Path', width=500, text_color='#b6bbff')
browse = CTkButton(master=app, text='...', width=10, corner_radius=10, border_width=2, border_color='#b6bbff', command=BrowsePath)
url = CTkEntry(master=app, placeholder_text='Url', width=500, text_color='#b6bbff')
checkbox = CTkCheckBox(master=app, text='Audio only', checkbox_height=30, checkbox_width=30, corner_radius=35)

# Place UI elements
label.place(relx=0.5, rely=0.25, anchor='center')
url.place(relx=0.5, rely=0.35, anchor='center')
path.place(relx=0.5, rely=0.45, anchor='center')
browse.place(relx=0.75, rely=0.45, anchor='center')
combobox.place(relx=0.5, rely=0.55, anchor='center')
checkbox.place(relx=0.5, rely=0.65, anchor='center')
btn.place(relx=0.5, rely=0.75, anchor='center')

# Start the app
app.mainloop()
