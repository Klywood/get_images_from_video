# Script for slicing frames from video in 2 different ways

- will save every specified frame:
```
  slice_video("video.mp4", frame_interval=60) # every 60th frame will be saved
```
- will save the specified number of frames evenly distributed across the video:
```
  slice_video("video.mp4", uniform_frames=20) # total 20 frames will be saved
```
