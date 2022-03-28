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


def slice_video(video, span=100, uniform=False, limit=5):
    """Saves frames as images from video

    As default: saves every 'span' frame from entire video

    If uniform=True - saves the 'limit' number (5 as default)
    of images taken uniformly from the entire video

    :param video: path to video file
    :param span: interval between frames that will be saved
    :param uniform: if True - saves the limit number of images taken uniformly from the entire video
    :param limit: (use if uniform=True) - the maximum number of saved frames (no limit as default)
    """
    #  create folder to save images
    folder_to_save = f'frames_{video}'
    os.makedirs(folder_to_save, exist_ok=True)
    #  open video
    cap = cv2.VideoCapture(video)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    current_frame = 0
    while True:
        ret, frame = cap.read()
        if ret:
            #  saves the limit number of images taken uniformly from the entire video
            if uniform:
                if current_frame in linspace(0, total_frames, limit, endpoint=False, dtype=int):
                    save_frame(frame, folder_to_save, current_frame)
            #  else: every 'span' frame with limit on total saved frames count
            else:
                if current_frame % span == 0:
                    save_frame(frame, folder_to_save, current_frame)
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

    slice_video("vid_60fps.mp4", 60)
