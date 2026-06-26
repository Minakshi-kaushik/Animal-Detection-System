from pathlib import Path
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent.parent

model = YOLO("yolov8n.pt")

model.train(
    data=str(ROOT / "dataset" / "data.yaml"),
    epochs=50,
    imgsz=640,
    batch=8,
    device="cpu",
)
