from pytubefix import YouTube
import os
import urllib.error
import time
import threading
from pytubefix.cli import on_progress

class TimeoutException(Exception):
    pass

def download_with_timeout(video_stream, output_path, filename, timeout_duration):
    def download():
        video_stream.download(output_path=output_path, filename=filename)

    download_thread = threading.Thread(target=download)
    download_thread.start()
    download_thread.join(timeout=timeout_duration)

    if download_thread.is_alive():
        raise TimeoutException("Download took too long and was aborted.")

def download_youtube_video(video_url, output_path='downloads', filename=None):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # Initialize YouTube object with progress callback
        yt = YouTube(video_url, on_progress_callback=on_progress)
        
        # Select the highest resolution stream available
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not video_stream:
            print("No suitable stream found for the video.")
            return False
        
        # Download the video with progress tracking and timeout
        print(f"Downloading: {yt.title}")
        start_time = time.time()
        download_with_timeout(video_stream, output_path, filename, timeout_duration=10)
        end_time = time.time()
        
        print(f"Download completed. Saved to: {output_path}")
        print(f"Total time taken: {end_time - start_time:.2f} seconds")
        return True
    except TimeoutException as e:
        print(f"An error occurred: {e}")
        return False
    except urllib.error.HTTPError as e:
        print(f"HTTP Error occurred: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Example usage
if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=FwSh1PzhdPs'  # Replace with your video URL
    download_youtube_video(video_url, output_path='downloads', filename='my_video.mp4')
