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
        raise TimeoutException("다운로드가 너무 오래 걸려 중단되었습니다.")

def download_youtube_video(video_url, output_path='downloads', filename=None):
    try:
        # 출력 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        # 진행 상황 콜백과 함께 YouTube 객체 초기화
        yt = YouTube(video_url, on_progress_callback=on_progress)
        
        # 사용 가능한 가장 높은 해상도의 스트림 선택
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not video_stream:
            print("No suitable stream found for the video.")
            return False
        
        # 진행 상황과 타임아웃을 사용하여 비디오 다운로드
        print(f"다운로드 중: {yt.title}")

        start_time = time.time()
        download_with_timeout(video_stream, output_path, filename, timeout_duration=10)
        end_time = time.time()
        
        print(f"다운로드 완료. 저장 위치: {output_path}")
        print(f"총 소요 시간: {end_time - start_time:.2f}초")
        return True
    except TimeoutException as e:
        print(f"Timeout 오류 발생: {e}")
        return False
    except urllib.error.HTTPError as e:
        print(f"HTTP 오류 발생: {e.code} - {e.reason}")
        return False
    except Exception as e:
        print(f"오류 발생: {e}")
        return False

# 사용 예시
if __name__ == '__main__':
    video_url = 'https://www.youtube.com/watch?v=FwSh1PzhdPs'  # 사용할 비디오 URL로 교체하세요
    download_youtube_video(video_url, output_path='downloads', filename='my_video.mp4')
