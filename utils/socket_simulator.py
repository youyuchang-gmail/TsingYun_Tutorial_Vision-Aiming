import base64
import json
import socket
from pathlib import Path
import cv2
import numpy as np


HOST = "127.0.0.1"
PORT = 50000
SEED = 12345
FIXED_CAMERA_POINT = {"x": 0.29, "y": 3.5, "z": 20.0}
CAMERA_MATRIX = [
    960.0, 0.0, 640.0,
    0.0, 960.0, 360.0,
    0.0, 0.0, 1.0,
]


def send_message(sock_file, payload):
    sock_file.write(json.dumps(payload) + "\n")
    sock_file.flush()

def detect_red_point_and_aim(image_bytes, camera_matrix, target_distance=1.0):
    
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
    mask2 = cv2.inRange(hsv, np.array([160, 100, 100]), np.array([179, 255, 255]))
    mask = mask1 | mask2
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return (0, 0, target_distance)
    
    largest = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest)
    if M["m00"] == 0:
        return (0, 0, target_distance)
    
    u = int(M["m10"] / M["m00"])
    v = int(M["m01"] / M["m00"])
    
    fx = camera_matrix[0, 0]
    fy = camera_matrix[1, 1]
    cx = camera_matrix[0, 2]
    cy = camera_matrix[1, 2]
    
    x_cam = (u - cx) / fx
    y_cam = (v - cy) / fy
    z_cam = 1.0  # 单位深度
    
    direction = np.array([x_cam, y_cam, z_cam])
    direction = direction / np.linalg.norm(direction)
    
    target_point = direction * target_distance
    
    return (float(target_point[0]), float(target_point[1]), float(target_point[2]))

def main():

    with socket.create_connection((HOST, PORT)) as sock:
        sock_file = sock.makefile("rw", encoding="utf-8", newline="\n")

        send_message(
            sock_file,
            {
                "type": "start",
                "seed": SEED,
                "cameraMatrix": CAMERA_MATRIX,
            },
        )

        while True:
            line = sock_file.readline()
            if not line:
                print("Connection closed by server.")
                break

            message = json.loads(line)
            message_type = message.get("type")

            if message_type == "frame":
                frame_id = message["frameId"]
                image_bytes = base64.b64decode(message["imageBase64"])

                camera_matrix = np.array([CAMERA_MATRIX[:3],CAMERA_MATRIX[3:6],CAMERA_MATRIX[6:]])
                pos = detect_red_point_and_aim(image_bytes, camera_matrix, 10)
                send_message(
                    sock_file,
                    {
                        "type": "aim",
                        "x": pos[0], # FIXED_CAMERA_POINT["x"],
                        "y": pos[1], # FIXED_CAMERA_POINT["y"],
                        "z": pos[2], # FIXED_CAMERA_POINT["z"],
                    },
                )
            elif message_type == "end":
                print(f"Game ended. Final score: {message['score']}, accuracy: {message['accuracy']}, precision: {message['average_to_center_distance']}")
                break


if __name__ == "__main__":
    main()
