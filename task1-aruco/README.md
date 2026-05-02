# Task 1 Framework

This folder only provides scaffolding for task 1.

Students still need to implement the key methods by themselves:
- camera calibration
- marker pose estimation
- OBJ model loading
- OBJ model rendering

## Files

- `calibrate.py`: fill in your calibration image path and calibration code
- `aruco_render.py`: fill in your ArUco video path and rendering code

## Input

Put your own files here, or directly change the TODO paths in the code:
- `data/calibration/`
- `data/aruco/`

## Run

```bash
python task1-aruco/calibrate.py
python task1-aruco/aruco_render.py
```

## Student TODO

Implement these functions:
- `create_board_points(...)`
- `detect_calibration_points(...)`
- `calibrate_camera(...)`
- `load_obj(...)`
- `estimate_marker_pose(...)`
- `render_virtual_object(...)`
