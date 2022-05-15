"""
Moduel for saving frames from video file as images

Examples of using moduel:

1)  Saves 5 frames taken uniformly from the entire video:
#slice_video("vid_2.mp4", uniform=True, limit=5)

2)  Saves every 24 frame:
#slice_video("video.mp4", 24)

"""

import os
import pathlib
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
    # print(total_frames)
    current_frame = 0

    while True:
        ret, frame = cap.read()
        if ret:
            #  saves the limit number of images taken uniformly from the entire video
            if uniform:
                frames_to_save = linspace(0, total_frames, limit, endpoint=False, dtype=int)
                if current_frame in frames_to_save:
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


if __name__ == '__main__':

    # rename_files_in_folder('videos', 'avi', 'avi')

    sorted_vids = sorted(os.listdir('videos'), key=lambda x: int(x[:x.find('.')]))
    count = 0
    for vid in sorted_vids:
        count += 1
        vid_path = os.path.join('videos', vid)
        slice_video(vid_path, 30)
        print(f"{count} of {len(sorted_vids)} videos done")
