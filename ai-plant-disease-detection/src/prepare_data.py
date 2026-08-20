from datasets import load_dataset
from sklearn.model_selection import train_test_split

from config import DATASET_NAME, SELECTED_CLASSES, VALIDATION_SPLIT, RANDOM_SEED


def load_potato_dataset():
    print("Loading dataset from Hugging Face...")

    dataset = load_dataset(DATASET_NAME)

    train_dataset = dataset["train"]
    test_dataset = dataset["test"]

    class_names = train_dataset.features["label"].names

    selected_class_ids = [
        class_names.index(class_name)
        for class_name in SELECTED_CLASSES
    ]

    print("Selected classes:")
    for class_id in selected_class_ids:
        print(f"- {class_id}: {class_names[class_id]}")

    train_dataset = train_dataset.filter(
        lambda example: example["label"] in selected_class_ids
    )

    test_dataset = test_dataset.filter(
        lambda example: example["label"] in selected_class_ids
    )

    train_indices = list(range(len(train_dataset)))

    train_idx, val_idx = train_test_split(
        train_indices,
        test_size=VALIDATION_SPLIT,
        random_state=RANDOM_SEED,
        stratify=train_dataset["label"],
    )

    filtered_train_dataset = train_dataset

    train_dataset = filtered_train_dataset.select(train_idx)

    val_dataset = filtered_train_dataset.select(val_idx)

    print("\nDataset ready:")
    print(f"Train: {len(train_dataset)} images")
    print(f"Validation: {len(val_dataset)} images")
    print(f"Test: {len(test_dataset)} images")

    return train_dataset, val_dataset, test_dataset, SELECTED_CLASSES

if __name__ == "__main__":
    load_potato_dataset()