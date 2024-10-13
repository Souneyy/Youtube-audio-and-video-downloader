# Youtube video and audio downloader
A simple youtube downloader program that i made. You can choose between the different resolutions that are available and if you want to download audio only that is also possible!

# Be sure to install ffmpeg if the program doesnt work and add it to your system path in order for the program to work since i use it
(because youtube stores audio files and video files seperatly for video resolutions that are above 720p, ffmpeg is used to combine those two files after the download so that you get a single video file with the audio and the video).

# To do this for windows do the following:
download the ffmpeg zip from the following link: https://github.com/GyanD/codexffmpeg/releases/tag/2024-10-10-git-0f5592cfc7
unzip it and place it in your C: drive (the drive where windows is installed)
after that go into the unzipped file and into bin and copy the path 
once you've copied the path go to your file explorer and right click on this pc and click on properties then go to "advanced system settings"
when the new window is oppened go to environment variables and under "system variables" click on path and edit
then click on new and paste the path that you coppied of the bin folder and then exit out of everything and the program should work
