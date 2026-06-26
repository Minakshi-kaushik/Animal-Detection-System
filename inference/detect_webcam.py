import cv2
from ultralytics import YOLO
from pathlib import Path

from animal_detection.utils.constants import CARNIVORES, RED, GREEN
from animal_detection.inference.carnivore_counter import count_carnivores


# ==========================
# Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "weights" / "best.pt"

model = YOLO(str(MODEL_PATH))


# ==========================
# Webcam Detection
# ==========================


def detect_webcam():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise ValueError("Could not access webcam")

    all_animals = []

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)[0]

        detected_animals = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            animal = model.names[cls_id]

            detected_animals.append(animal)
            all_animals.append(animal)

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            color = RED if animal.lower() in CARNIVORES else GREEN

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                2,
            )

            cv2.putText(
                frame,
                animal,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2,
            )

        carnivore_count = count_carnivores(detected_animals)

        cv2.putText(
            frame,
            f"Carnivores: {carnivore_count}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

        cv2.imshow("Wild Animal Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # ==========================
    # Final Statistics
    # ==========================

    final_carnivore_count = sum(
        1 for animal in all_animals if animal.lower() in CARNIVORES
    )

    return (
        None,
        final_carnivore_count,
        all_animals,
    )


# ==========================
# Testing
# ==========================

if __name__ == "__main__":
    output_path, carnivore_count, animals = detect_webcam()

    print(f"Carnivores: {carnivore_count}")
    print(f"Animals: {sorted(set(animals))}")
