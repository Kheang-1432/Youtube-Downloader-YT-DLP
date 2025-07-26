import os
import yt_dlp

save_location = r"../download"

def is_playlist(url):
    return ("list=" in url and "watch" in url) or "playlist?" in url

def download_youtube_video(url, resolution="1080", filename=None):
    os.makedirs(save_location, exist_ok=True)

    format_selector = f"bv*[height<={resolution}][ext=mp4]+ba[ext=m4a]/b[height<={resolution}][ext=mp4]/best"

    ydl_opts = {
        'format': format_selector,
        'merge_output_format': 'mp4',
        'outtmpl': '',
        'noplaylist': True,
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    if is_playlist(url):
        ydl_opts['noplaylist'] = False
        ydl_opts['outtmpl'] = os.path.join(
            save_location, '%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s'
        )
    else:
        if not filename:
            filename = "%(title)s.%(ext)s"
        elif not filename.lower().endswith('.mp4'):
            filename += '.mp4'
        ydl_opts['outtmpl'] = os.path.join(save_location, filename)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    url = input("Enter YouTube video or playlist URL: ").strip()
    resolution = input("Enter max resolution (360, 480, 720, 1080, 1440) [default: 1080]: ").strip()
    resolution = resolution if resolution else "1080"

    filename = None
    if not is_playlist(url):
        filename = input(f"Enter filename (used if single video, saved to {save_location}): ").strip()

    download_youtube_video(url, resolution, filename)