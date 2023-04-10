import os
import pytube
import subprocess


def is_youtube_link(link):
    if 'playlist' in link:
        try:
            playlist = pytube.Playlist(link)
            return True
        except:
            return False
    try:
        yt = pytube.YouTube(link)
        return True
    except:
        return False


def download_video(link):
    video = pytube.YouTube(link)
    stream = video.streams.filter(progressive=True).order_by('resolution').desc().first()
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    stream.download('downloads')
    print(f"Downloaded: {video.title}")


def download_playlist(link):
    playlist = pytube.Playlist(link)
    for video in playlist.videos:
        try:
            video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
                output_path='downloads/')
            print(f"Downloaded: {video.title}")
        except Exception as e:
            print(f"Could not download {video.title} - {str(e)}")


with open('links.txt', 'r') as f:
    links = f.read().splitlines()

for link in links:
    if not is_youtube_link(link):
        print(f"{link} is not a valid YouTube link.")
        continue

    if 'playlist' in link:
        download_playlist(link)
    else:
        download_video(link)

os.chdir('downloads')
videos = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.mp4')]
for video in videos:
    mp3_filename = os.path.splitext(video)[0] + '.mp3'
    subprocess.call(
        ['ffmpeg', '-i', video, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', mp3_filename],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Converted: {mp3_filename}")
    os.remove(video)

print("Every requested link has been converted.")
input("\nPress enter to exit")
