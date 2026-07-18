import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = os.path.join(
    "trained_model",
    "breast_cancer_model.h5"
)

model = tf.keras.models.load_model(MODEL_PATH)

print("AI MODEL LOADED SUCCESSFULLY")
print("MODEL INPUT SHAPE:", model.input_shape)


def predict_mammogram(image_path):

    try:

        img = Image.open(image_path).convert("RGB")

        # MUST MATCH TRAINING SIZE
        img = img.resize((128, 128))

        img_array = np.array(img).astype("float32")

        img_array = img_array / 255.0

        img_array = np.expand_dims(
            img_array,
            axis=0
        )

        prediction = model.predict(
            img_array,
            verbose=0
        )[0][0]

        print("RAW PREDICTION =", prediction)

        if prediction >= 0.5:

            result = "Malignant"

            confidence = round(
                prediction * 100,
                2
            )

        else:

            result = "Benign"

            confidence = round(
                (1 - prediction) * 100,
                2
            )

        print(
            "RESULT:",
            result,
            "CONFIDENCE:",
            confidence
        )

        return result, confidence

    except Exception as e:

        import traceback

        print("========== AI ERROR ==========")
        traceback.print_exc()
        print("==============================")

        return "Error", 0