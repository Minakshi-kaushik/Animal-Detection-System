import cv2
from ultralytics import YOLO
from pathlib import Path
from datetime import datetime

from animal_detection.utils.constants import CARNIVORES, RED, GREEN


# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "weights" / "best.pt"

OUTPUT_DIR = BASE_DIR / "outputs" / "videos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================
# Load Model
# ==========================

model = YOLO(str(MODEL_PATH))


# ==========================
# Detection Function
# ==========================


def detect_video(video_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0:
        fps = 30

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = OUTPUT_DIR / f"result_{timestamp}.mp4"

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    # ==========================
    # Statistics
    # ==========================

    all_animals = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)[0]

        for box in results.boxes:
            cls_id = int(box.cls[0])

            animal = model.names[cls_id]

            all_animals.append(animal)

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            color = RED if animal.lower() in CARNIVORES else GREEN

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

            cv2.putText(
                frame,
                animal,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

        writer.write(frame)

        cv2.imshow("Animal Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    writer.release()

    cv2.destroyAllWindows()

    # ==========================
    # Final Statistics
    # ==========================

    carnivore_count = sum(1 for animal in all_animals if animal.lower() in CARNIVORES)

    return (
        str(output_path),
        carnivore_count,
        all_animals,
    )


# ==========================
# Testing
# ==========================

if __name__ == "__main__":
    video_path = input("Enter video path: ").strip()

    output_path, carnivore_count, animals = detect_video(video_path)

    print(f"\nSaved to: {output_path}")
    print(f"Carnivores: {carnivore_count}")
    print(f"Animals: {animals}")
