from customtkinter import *
from pytubefix import YouTube
import tkinter.filedialog as filedialog
import time
import os
import ffmpeg
# Make sure to install ffmpeg and create a path for the bin folder. Install customtkinter and pytubefix with: ex. pip install pytubefix


def merge_video_audio(video_path, audio_path, output_path):
    # Check if both video and audio files exist
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return
    
    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return
    
    # Print paths to debug
    print(f"Merging video: {video_path}")
    print(f"Merging audio: {audio_path}")
    print(f"Output file: {output_path}")

    # Merge video and audio using ffmpeg
    try:
        video = ffmpeg.input(video_path)
        audio = ffmpeg.input(audio_path)
        
        ffmpeg_output = ffmpeg.output(video, audio, output_path, vcodec='copy', acodec='aac', strict='experimental')
        
        # Capture stdout and stderr for debugging
        ffmpeg.run(ffmpeg_output, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        print(f"Merge completed successfully! Output saved at: {output_path}")
    
    except ffmpeg.Error as e:
        print(f"Error occurred while merging: {e.stderr.decode()}")
        return


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


def download_video(url, resolution, path):
    try:
        yt = YouTube(url)

        # Try to get the video stream (without audio)
        video_stream = yt.streams.filter(res=resolution, file_extension='mp4', only_video=True).first()

        if not video_stream:
            # If video stream isn't found, print available resolutions
            available_streams = yt.streams.filter(file_extension='mp4', only_video=True)
            print(f"Available video streams: {[s.resolution for s in available_streams]}")

            # Attempt to find the closest resolution
            for s in available_streams:
                if s.resolution and s.resolution.startswith(resolution[0]):
                    video_stream = s
                    break

        # Try to get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        if video_stream and audio_stream:
            # If both streams exist, download them separately and merge them
            print(f'Downloading video at {resolution} and audio...')
            video_path = os.path.join(path, 'video.mp4')
            audio_path = os.path.join(path, 'audio.mp4')

            video_stream.download(output_path=path, filename='video.mp4')
            audio_stream.download(output_path=path, filename='audio.mp4')

            # Merge the video and audio streams and delete the standalone files afterwards
            output_path = os.path.join(path, f"{yt.title}.mp4")
            merge_video_audio(video_path, audio_path, output_path)
            print('Download complete with video and audio seperated!')
            
            os.remove(video_path)
            os.remove(audio_path)
        else:
            print(f"Unable to find video or audio streams at {resolution} resolution.")

    except Exception as e:
        print(f"Failed to download video: {e}")


# Shake animation if a field is not filled before pressing the download button
def ShakeButton():
    for _ in range(5):
        btn.place(relx=0.5, rely=0.75, anchor='center', x=5)
        app.update()
        time.sleep(0.05)
        btn.place(relx=0.5, rely=0.75, anchor='center', x=-5)
        app.update()
        time.sleep(0.05)


# Browse button functionality
def BrowsePath():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path.delete(0, END)
        path.insert(0, selected_path)


# Validate entries and initiate download if both fields are filled
def validateEntries():
    # Check if both entry fields are filled
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


# Making UI elements with customtkinter 
# Initialize the app
app = CTk()
app.geometry('1080x720')
app.title("YouTube Downloader")
set_appearance_mode('dark')

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

app.mainloop()