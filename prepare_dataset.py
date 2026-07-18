import os
import shutil

source_folder = r"E:\Code Data\cancer_detection\IDC_regular_ps50_idx5"
target_folder = r"E:\Code Data\cancer_detection\dataset"

benign_folder = os.path.join(target_folder, "benign")
malignant_folder = os.path.join(target_folder, "malignant")

os.makedirs(benign_folder, exist_ok=True)
os.makedirs(malignant_folder, exist_ok=True)

for root, dirs, files in os.walk(source_folder):
    for file in files:
        if file.endswith(".png"):
            src = os.path.join(root, file)

            if "class0" in file:
                shutil.copy(src, benign_folder)

            elif "class1" in file:
                shutil.copy(src, malignant_folder)

print("Dataset organized successfully!")