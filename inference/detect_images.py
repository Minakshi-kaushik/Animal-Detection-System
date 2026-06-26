import cv2
from ultralytics import YOLO
from datetime import datetime
from pathlib import Path

from utils.constants import CARNIVORES, RED, GREEN
from inference.carnivore_counter import count_carnivores

# ==========================
# Paths
# ==========================

import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "models" / "weights" / "best.pt"

OUTPUT_DIR = BASE_DIR / "outputs" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ==========================
# Load Model
# ==========================

model = YOLO(str(MODEL_PATH))

# ==========================
# Detection Function
# ==========================


def detect_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    results = model(image)[0]

    detected_animals = []

    for box in results.boxes:
        cls_id = int(box.cls[0])

        animal = model.names[cls_id]

        confidence = float(box.conf[0])

        label = f"{animal} {confidence:.2f}"

        detected_animals.append(animal)

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        color = RED if animal.lower() in CARNIVORES else GREEN

        # Bounding Box
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color,
            3,
        )

        # Label Background
        (text_width, text_height), _ = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            2,
        )

        cv2.rectangle(
            image,
            (x1, y1 - text_height - 12),
            (x1 + text_width + 10, y1),
            color,
            -1,
        )

        # Animal Name + Confidence
        cv2.putText(
            image,
            label,
            (x1 + 5, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

    carnivore_count = count_carnivores(detected_animals)

    # Carnivore Counter
    cv2.putText(
        image,
        f"Carnivores Detected: {carnivore_count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_path = OUTPUT_DIR / f"result_{timestamp}.jpg"

    cv2.imwrite(str(output_path), image)

    return str(output_path), carnivore_count, detected_animals


# ==========================
# Standalone Testing
# ==========================

if __name__ == "__main__":
    image_path = input("Enter image path: ").strip()

    output_path, count, animals = detect_image(image_path)

    print(f"\nOutput saved to: {output_path}")
    print(f"Carnivores detected: {count}")
    print(f"Animals detected: {', '.join(set(animals))}")

    result = cv2.imread(output_path)

    cv2.imshow("Detection Result", result)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
