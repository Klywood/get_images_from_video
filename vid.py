"""
Moduel for saving frames from video file as images

Examples of using moduel:

1)  Saves 5 frames taken uniformly from the entire video:
#slice_video("vid_2.mp4", uniform=True, limit=5)

2)  Saves every 24 frame:
#slice_video("video.mp4", 24)

"""
import threading
import os
import pathlib
import time

import cv2
from numpy import linspace
from transliterate import translit


def slice_video(video: str, folder: str = None, frame_interval: int = None, uniform_frames: int = None):
    """Saves frames as images from video

    You should choose 1 type of slicing:
        'frame_interval' parameter allows you to save each specified frame
        'uniform_frames' allows you to save the specified number of frames evenly distributed across the video

    :param video: name of video in videos folder
    :param folder: name of folder with video (None as default - video in root folder)
    :param frame_interval: interval between frames that will be saved
    :param uniform_frames: if True - saves the specified number of images taken uniformly from the entire video
    """
    if frame_interval is None and uniform_frames is None:
        raise AttributeError("Set only one attribute - how video should be sliced")

    eng_vid_name = translit('_'.join(video.split('.')[0].split()), language_code='ru', reversed=True)
    #  create folder to save images
    default_folder = f'every_{frame_interval}_frame_{eng_vid_name}'
    uniform_folder = f'uniformly_{uniform_frames}_frames_{eng_vid_name}'
    #  open video
    path_to_video = os.path.join(folder, video) if folder else video
    cap = cv2.VideoCapture(path_to_video)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f'There are {total_frames} frames in video')
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if ret:
            #  saves the limit number of images taken uniformly from the entire video
            if uniform_frames:
                if current_frame in linspace(0, total_frames, uniform_frames, endpoint=False, dtype=int):
                    save_frame(frame, uniform_folder, current_frame)
            #  else: every 'frame_interval' frame with limit on total saved frames count
            else:
                if current_frame % frame_interval == 0:
                    save_frame(frame, default_folder, current_frame)
            current_frame += 1
        else:
            break
    cv2.destroyAllWindows()


def save_frame(frame, folder, file_name):
    """Saves frame to specified folder

    :param frame: frame to be saved
    :param folder: name of folder to save
    :param file_name: name of file to save
    """
    folder_to_save = os.path.join('results', folder)
    os.makedirs(folder_to_save, exist_ok=True)
    path = os.path.join(folder_to_save, f"{file_name}.jpg")
    cv2.imwrite(path, frame)
    print(f"Frame saved as: {path}")


def rename_files_in_folder(path, from_type='mp4', to_type=None):
    """Renames files in given folder to nums ascending"""
    to_type = to_type if to_type else from_type
    main_path = pathlib.Path(path)
    for i, path in enumerate(main_path.glob(f'*.{from_type}')):
        new_name = os.path.join(main_path, f"{i}.{to_type}")
        try:
            path.rename(new_name)
        except FileExistsError:
            print(f"File '{new_name}' already exists. Going to next")
            continue


def slice_all_videos_in_folder(folder, frame_interval=None, uniform_frames=None):
    """Get frames from all videos in folder in multi-threaded mode"""
    for video in os.listdir(folder):
        threading.Thread(target=slice_video,
                         args=(video, folder, frame_interval, uniform_frames)
                         ).start()


if __name__ == '__main__':
    # slice_video("1.mp4", 60)
    since = time.time()

    slice_all_videos_in_folder('videos', frame_interval=60)

    print(time.time() - since)
