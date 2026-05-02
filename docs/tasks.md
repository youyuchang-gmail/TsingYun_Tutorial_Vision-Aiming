# Tasks

## Task 1: ArUco Detection

### 任务目标

了解相机标定的方法、作用及实际效果。

### 建议流程

1. **准备标定板**  
   使用平板或打印的棋盘格标定图片。

2. **采集标定图像**  
   使用相机拍摄足够数量（建议 15–20 张）且角度、距离各不相同的标定图片。

3. **实现标定程序**  
   完善基于 OpenCV 的相机标定程序，输出内参、畸变系数等标定结果。

4. **准备 ArUco 标记板**  
   打印或使用平板显示 ArUco 标记图。

5. **采集 ArUco 视频**  
   使用同一相机拍摄一段包含 ArUco 标记的视频。

6. **实现姿态渲染程序**  
   完善 OpenCV 模型渲染程序，将虚拟 3D 物体叠加到 ArUco 标记上，验证标定效果。

## Task 2: CV & CNN Recognition

## Task 3: Kalman Filter Tracking

## Run

After completing the above three tasks, execute:

```bash
python run/run.py
```

to start the simulator.
