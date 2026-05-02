import json
from pathlib import Path

import cv2
import numpy as np

# TODO(student): fill in your camera parameter file from calibrate.py.
CAMERA_PARAMS_PATH = Path(__file__).resolve().parent / "output" / "camera_params.json"

# TODO(student): fill in your own ArUco video path.
ARUCO_VIDEO_PATH = Path(__file__).resolve().parent / "data" / "aruco" / "aruco.mp4"

# TODO(student): fill in your own ArUco settings.
ARUCO_DICTIONARY = "DICT_4X4_50"
MARKER_LENGTH_METERS = 0.05

ARUCO_OUTPUT_IMAGE_PATH = Path(__file__).resolve().parent / "output" / "aruco_result.jpg"
ARUCO_OUTPUT_VIDEO_PATH = Path(__file__).resolve().parent / "output" / "aruco_result.mp4"

# TODO(student): use this path if you want to render one of the provided OBJ models.
MODEL_PATH = Path(__file__).resolve().parent / "res" / "models" / "cube.obj"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def load_camera_params(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    camera_matrix = np.array(data["camera_matrix"], dtype=np.float32)
    dist_coeffs = np.array(data["dist_coeffs"], dtype=np.float32)
    return camera_matrix, dist_coeffs


def load_obj(model_path):
    """
    Load an OBJ model.

    The provided OBJ files use lines such as:
    - v x y z
    - f 1/1/1 2/2/2 3/3/3
    """
    if not model_path.exists():
        raise FileNotFoundError(f"OBJ model not found: {model_path}")

    vertices = []
    faces = []

    with model_path.open("r", encoding="utf-8") as file:
        for line_index, raw_line in enumerate(file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("v "):
                # TODO: Add vertex coordinates to vertices list
                pass

            elif line.startswith("f "):
                parts = line.split()[1:]
                # TODO: Add face indices to faces list
                pass

            else:
                # Lines such as vt / vn / usemtl can be ignored for this task.
                continue

    return vertices, faces


def get_aruco_dictionary(name):
    if not hasattr(cv2.aruco, name):
        raise ValueError(f"Unknown ArUco dictionary: {name}")
    return cv2.aruco.getPredefinedDictionary(getattr(cv2.aruco, name))


def detect_markers(frame, dictionary):
    if hasattr(cv2.aruco, "ArucoDetector"):
        detector = cv2.aruco.ArucoDetector(dictionary)
        corners, ids, _ = detector.detectMarkers(frame)
    else:
        corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary)
    return corners, ids


def estimate_marker_pose(marker_corners, marker_length_meters, camera_matrix, dist_coeffs):
    """
    TODO(student): estimate the marker pose from one detected marker.
    TODO(student): choose the 3D corner coordinates of the marker.
    TODO(student): match them with the detected 2D image corners.
    TODO(student): solve for rvec and tvec.

    Return:
        rvec: numpy array with shape (3, 1) or (3,)
        tvec: numpy array with shape (3, 1) or (3,)
    """
    raise NotImplementedError("implement estimate_marker_pose()")


def render_virtual_object(frame, rvec, tvec, camera_matrix, dist_coeffs, vertices, faces):
    """
    TODO(student): rescale the model so its size matches the marker.
    TODO(student): shift / rotate the model so it stands at the desired place.
    TODO(student): use cv2.projectPoints(...) to project all 3D vertices.
    TODO(student): convert projected points to integer pixel coordinates.
    TODO(student): draw every face or edge on frame.

    Expected effect:
    the rendered OBJ model should move with the marker and keep a stable 3D pose.
    """
    raise NotImplementedError("implement render_virtual_object()")


def process_frame(frame, dictionary, camera_matrix, dist_coeffs, vertices, faces):
    output = frame.copy()
    corners, ids = detect_markers(frame, dictionary)

    if ids is None or len(ids) == 0:
        return output

    cv2.aruco.drawDetectedMarkers(output, corners, ids)

    for marker_corners, _ in zip(corners, ids):
        rvec, tvec = estimate_marker_pose(
            marker_corners,
            MARKER_LENGTH_METERS,
            camera_matrix,
            dist_coeffs,
        )
        render_virtual_object(
            output,
            rvec,
            tvec,
            camera_matrix,
            dist_coeffs,
            vertices,
            faces,
        )

    return output


def run_aruco_render(dictionary, camera_matrix, dist_coeffs, capture, vertices, faces):
    ok, frame = capture.read()
    if not ok:
        raise SystemExit("Cannot read the first frame from the source.")

    height, width = frame.shape[:2]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(ARUCO_OUTPUT_VIDEO_PATH),
        cv2.VideoWriter_fourcc(*"mp4v"),
        30.0,
        (width, height),
    )

    try:
        while ok:
            result = process_frame(frame, dictionary, camera_matrix, dist_coeffs, vertices, faces)
            writer.write(result)
            cv2.imshow("aruco", result)

            if cv2.waitKey(1) & 0xFF == 27:
                break

            ok, frame = capture.read()
    finally:
        writer.release()
        capture.release()
        cv2.destroyAllWindows()

    print(f"Saved video result to: {ARUCO_OUTPUT_VIDEO_PATH}")


def main():
    if not CAMERA_PARAMS_PATH.exists():
        raise SystemExit(f"Camera parameters not found: {CAMERA_PARAMS_PATH}")

    camera_matrix, dist_coeffs = load_camera_params(CAMERA_PARAMS_PATH)
    vertices, faces = load_obj(MODEL_PATH)
    dictionary = get_aruco_dictionary(ARUCO_DICTIONARY)
    capture = cv2.VideoCapture(str(ARUCO_VIDEO_PATH))

    if not capture.isOpened():
        raise SystemExit(f"Cannot open video: {ARUCO_VIDEO_PATH}")

    run_aruco_render(dictionary, camera_matrix, dist_coeffs, capture, vertices, faces)


if __name__ == "__main__":
    main()
