"""
Moduel for saving frames from video file as images

Examples of using moduel:

1)  Saves 5 frames taken uniformly from the entire video:
#slice_video("vid_2.mp4", uniform=True, limit=5)

2)  Saves every 24 frame:
#slice_video("video.mp4", 24)

"""

import os
import cv2
from numpy import linspace


def slice_video(video, frame_interval: int = None, uniform_frames: int = None):
    """Saves frames as images from video

    You should choose 1 type of slicing:
        'frame_interval' parameter allows you to save each specified frame
        'uniform_frames' allows you to save the specified number of frames evenly distributed across the video


    :param video: path to video file
    :param frame_interval: interval between frames that will be saved
    :param uniform_frames: if True - saves the specified number of images taken uniformly from the entire video
    """
    #  create folder to save images
    default_folder = f'every_{frame_interval}_frame_{video}'
    uniform_folder = f'uniformly_{uniform_frames}_frames_{video}'
    if frame_interval and not uniform_frames:
        os.makedirs(default_folder, exist_ok=True)
    elif uniform_frames and not frame_interval:
        os.makedirs(uniform_folder, exist_ok=True)
    else:
        raise AttributeError("Set only one attribute - how video should be sliced")
    #  open video
    cap = cv2.VideoCapture(video)

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
            #  else: every 'span' frame with limit on total saved frames count
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
    path = os.path.join(folder, f"{file_name}.jpg")
    print(f"Creating file... {path}")
    cv2.imwrite(path, frame)


if __name__ == '__main__':
    slice_video("1.mp4", uniform_frames=2)
