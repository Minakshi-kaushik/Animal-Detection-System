# 🦁 WildVision AI – Smart Wildlife Detection & Monitoring System

## Overview

The Smart Wildlife Detection & Monitoring System is a computer vision application developed using Python, OpenCV, Tkinter, and YOLOv8. The system is capable of detecting and classifying multiple animal species from images, videos, and live webcam streams in real time.

The application highlights carnivorous animals using red bounding boxes, displays detection statistics, generates processed outputs, and provides a user-friendly graphical interface for wildlife monitoring and surveillance applications.

---

## Features

### 🖼 Image Detection

* Upload and analyze images.
* Detect multiple animals simultaneously.
* Display confidence scores.
* Highlight carnivores in red.
* Save processed images automatically.
* Show detection statistics and species summary.

### 🎥 Video Detection

* Upload and process recorded videos.
* Real-time frame-by-frame animal detection.
* Save annotated output videos.
* Generate species statistics after processing.
* Carnivore monitoring throughout the video.

### 📷 Real-Time Webcam Detection

* Live animal detection using webcam feed.
* Continuous species monitoring.
* Real-time carnivore counter.
* Instant detection visualization.

### 📊 Detection Analytics

* Total animals detected.
* Carnivores detected.
* Herbivores detected.
* Unique species detected.
* Detection summaries displayed in GUI.

### 🖥 User-Friendly GUI

* Modern Tkinter interface.
* Scrollable dashboard.
* Detection statistics panel.
* Status monitoring.
* Interactive controls for Image, Video, and Webcam detection.

---

## Technology Stack

### Programming Language

* Python 3.13

### Computer Vision & Deep Learning

* YOLOv8
* OpenCV
* PyTorch
* Ultralytics

### GUI Development

* Tkinter
* Pillow (PIL)

### Data Processing

* NumPy

---

## Project Structure

```text
animal_detection/
│
├── assets/
│   └── banner.webp
│
├── gui/
│   └── animal_gui.py
│
├── inference/
│   ├── detect_images.py
│   ├── detect_video.py
│   ├── detect_webcam.py
│   └── carnivore_counter.py
│
├── models/
│   └── weights/
│       └── best.pt
│
├── training/
│   └── train.py
│
├── utils/
│   └── constants.py
│
├── outputs/
│   ├── images/
│   └── videos/
│
├── dataset/
│
├── requirements.txt
├── README.md
└── __init__.py
```

---

## Model Training

The model was trained using YOLOv8 on a custom wildlife dataset containing multiple animal species.

### Training Configuration

* Model: YOLOv8 Nano (yolov8n)
* Image Size: 640 × 640
* Batch Size: 8
* Epochs: 50
* Framework: Ultralytics YOLOv8
* Device: CPU

### Performance Snapshot

| Metric    | Value |
| --------- | ----- |
| Precision | 0.755 |
| Recall    | 0.732 |
| mAP@50    | 0.791 |
| mAP@50-95 | 0.561 |

Best validation performance was achieved around Epoch 25.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Minakshi-kaushik/Emotion-Detection-Attendance-System
cd animal_detection
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Run the GUI:

```bash
python -m animal_detection.gui.animal_gui
```

---

## Outputs

### Image Detection

Processed images are stored in:

```text
outputs/images/
```

### Video Detection

Processed videos are stored in:

```text
outputs/videos/
```

---

## Carnivore Monitoring

The system identifies carnivorous animals and:

* Highlights them using red bounding boxes.
* Displays carnivore counts.
* Generates carnivore alerts.
* Provides monitoring statistics for surveillance scenarios.

---

## Future Enhancements

* Animal population analytics.
* PDF detection reports.
* Detection history database.
* GPS-enabled wildlife monitoring.
* Multi-camera support.
* Cloud deployment.
* Mobile application integration.
* Real-time dashboard visualization.

---

## Learning Outcomes

This project demonstrates practical implementation of:

* Object Detection using YOLOv8
* Deep Learning Model Training
* Real-Time Computer Vision
* OpenCV Image Processing
* GUI Development using Tkinter
* Wildlife Monitoring Applications
* End-to-End AI Project Development

---

## Author

**Minakshi Kaushik**

Computer Vision • Artificial Intelligence • Machine Learning • Python Development

---

## License

This project is developed for educational and academic purposes.
