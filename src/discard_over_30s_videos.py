import os
from typing import Callable, Union

import cv2

def get_duration(file_path: str) -> Union[float, None]:
    video = cv2.VideoCapture(file_path)
    
    if not video.isOpened():
        print("Error: Could not open video file.")
        return None

    # 총 프레임 수와 초당 프레임 수 가져오기
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)

    # 비디오 객체 해제
    video.release()
    
    if fps > 0:
        # 총 길이 계산 (초 단위)
        duration = frame_count / fps
        return duration
    else:
        print("Error: FPS value is invalid.")
        return None

def discard_over_30s_videos(get_dura_func: Callable, file_path: str):
    duration = get_dura_func(file_path)
    if duration is not None:
        if duration > 30.0:
            os.remove(file_path)

if __name__ == '__main__':
    discard_over_30s_videos(get_duration, r'C:\Users\HAMA\Videos\Captures\test.mp4')
