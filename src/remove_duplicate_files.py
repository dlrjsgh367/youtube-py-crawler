import os

def remove_duplicate_files(*folder_paths):
    seen_files = set()
    for folder_path in folder_paths:
        files = os.listdir(folder_path)
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                if file_name in seen_files:
                    # 파일명이 중복되는 경우 삭제
                    os.remove(file_path)
                    print(f"Removed duplicate file: {file_path}")
                else:
                    seen_files.add(file_name)

if __name__ == '__main__':
    remove_duplicate_files(
        'C:/Users/HAMA/workspace/youtube-py-crawler/data/lgh',
        'C:/Users/HAMA/workspace/youtube-py-crawler/data/ljh',
        'C:/Users/HAMA/workspace/youtube-py-crawler/data/jhm',
    )