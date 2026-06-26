from animal_detection.utils.constants import CARNIVORES


def count_carnivores(animal_names):
    count = 0

    for animal in animal_names:
        if animal.lower() in CARNIVORES:
            count += 1

    return count
