from pathlib import Path
import base64
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "moondream"

INPUT_FOLDER = Path("input")
OUTPUT_FOLDER = Path("output")

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    return encoded_image

def generate_caption(image_path):
    image_base64 = image_to_base64(image_path)

    prompt = """
Analyze this image carefully.

Return the answer in Markdown format:

# Short Caption
Write one direct sentence describing the image.

# Main Subject
What is the main subject of the image?

# Visible Objects
List the visible objects in the image.

# Scene Description
Describe the scene, background, colors, and visual details.

# Confidence
Explain what you are confident about and what is uncertain.

Do not give a generic answer. Be specific based on the image.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "image": [image_base64],
            "stream": False,
        },
        timeout=300,
    )

    response.raise_for_status()
    data = response.json()

    return data["response"]

def save_caption(caption, image_path):
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    output_file_name = image_path.stem + "_caption.md"
    output_path = OUTPUT_FOLDER / output_file_name

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(caption)
    
    return output_path

def process_image(image_path):
    print(f"\nProcessing: {image_path.name}")

    caption = generate_caption(image_path)
    output_path = save_caption(caption,image_path)

    print(f"Done: {output_path}")

def main():
    if not INPUT_FOLDER.exists():
        INPUT_FOLDER.mkdir()
        print("Create input folder. Please add image files into input.")
        return

    image_files = list(INPUT_FOLDER.glob("*.jpg")) + list(INPUT_FOLDER.glob("*.jpeg"))

    if not image_files:
        print("No image files found in input folder.")
        return
    
    print(f"Found {len(image_files)} image file(s).")

    for image_path in image_files:
        process_image(image_path)
    
    print("\nAll done!")

if __name__ == "__main__":
    main()