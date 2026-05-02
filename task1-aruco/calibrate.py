import json
from pathlib import Path

import cv2
import numpy as np

# TODO(student): fill in your own calibration image folder.
CALIBRATION_IMAGES_DIR = Path(__file__).resolve().parent / "data" / "calibration"

# TODO(student): change this if your image extension is different.
CALIBRATION_IMAGE_GLOB = "*.jpg"

# TODO(student): fill in your own calibration target information.
CALIBRATION_TARGET_TYPE = "chessboard"
PATTERN_SIZE = (9, 6)
SQUARE_SIZE_METERS = 0.025

CAMERA_PARAMS_PATH = Path(__file__).resolve().parent / "output" / "camera_params.json"


def list_calibration_images():
    return sorted(Path(CALIBRATION_IMAGES_DIR).glob(CALIBRATION_IMAGE_GLOB))


def create_board_points(pattern_size, square_size_meters):
    """
    TODO(student):
    Build the 3D corner coordinates of your calibration board.

    Return:
        numpy array with shape (N, 3)
    """
    raise NotImplementedError("implement create_board_points()")


def detect_calibration_points(gray_image, pattern_size):
    """
    TODO(student):
    Detect the calibration points in one image.

    Return:
        found: bool
        image_points: numpy array with shape (N, 1, 2) or (N, 2)
    """
    raise NotImplementedError("implement detect_calibration_points()")


def calibrate_camera(object_points, image_points, image_size):
    """
    TODO(student):
    Run camera calibration from all matched 3D / 2D points.

    Return:
        camera_matrix: numpy array with shape (3, 3)
        dist_coeffs: numpy array
    """
    raise NotImplementedError("implement calibrate_camera()")


def save_camera_params(camera_matrix, dist_coeffs, image_size, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "image_width": int(image_size[0]),
        "image_height": int(image_size[1]),
        "camera_matrix": camera_matrix.tolist(),
        "dist_coeffs": dist_coeffs.reshape(-1).tolist(),
    }
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    image_paths = list_calibration_images()
    if not image_paths:
        raise SystemExit(f"No calibration images found in {CALIBRATION_IMAGES_DIR} matching {CALIBRATION_IMAGE_GLOB}")

    board_points = create_board_points(PATTERN_SIZE, SQUARE_SIZE_METERS)

    object_points = []
    image_points = []
    image_size = None

    for image_path in image_paths:
        image = cv2.imread(str(image_path))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_size = (gray.shape[1], gray.shape[0])

        found, points = detect_calibration_points(gray, PATTERN_SIZE)
        if not found:
            print(f"Skip image without valid points: {image_path.name}")
            continue

        object_points.append(board_points.copy())
        image_points.append(points)
        print(f"Use image: {image_path.name}")

    if not object_points:
        raise SystemExit("No valid calibration images were collected.")

    camera_matrix, dist_coeffs = calibrate_camera(object_points, image_points, image_size)
    save_camera_params(camera_matrix, dist_coeffs, image_size, CAMERA_PARAMS_PATH)

    print(f"Saved camera parameters to: {CAMERA_PARAMS_PATH}")


if __name__ == "__main__":
    main()
