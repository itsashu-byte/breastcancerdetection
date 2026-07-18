import os
import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.callbacks import ModelCheckpoint

# ==========================================
# SETTINGS
# ==========================================

DATASET_PATH = "dataset"

IMG_HEIGHT = 128
IMG_WIDTH = 128

BATCH_SIZE = 32
EPOCHS = 10

# ==========================================
# CREATE SAVE FOLDER
# ==========================================

os.makedirs("trained_model", exist_ok=True)

# ==========================================
# DATA AUGMENTATION
# ==========================================

datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.20,
    rotation_range=15,
    zoom_range=0.15,
    horizontal_flip=True
)

train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training',
    shuffle=True
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

print("\nClass Mapping:")
print(train_data.class_indices)

# ==========================================
# MOBILENETV2
# ==========================================

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(128,128,3)
)

base_model.trainable = False

# ==========================================
# CUSTOM HEAD
# ==========================================

x = base_model.output

x = GlobalAveragePooling2D()(x)

x = Dense(
    128,
    activation='relu'
)(x)

x = Dropout(0.30)(x)

output = Dense(
    1,
    activation='sigmoid'
)(x)

model = Model(
    inputs=base_model.input,
    outputs=output
)

# ==========================================
# COMPILE
# ==========================================

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# CALLBACKS
# ==========================================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    filepath="trained_model/best_model.h5",
    monitor='val_accuracy',
    save_best_only=True,
    verbose=1
)

# ==========================================
# TRAIN MODEL
# ==========================================

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    callbacks=[
        early_stop,
        checkpoint
    ]
)

# ==========================================
# SAVE FINAL MODEL
# ==========================================

model.save(
    "trained_model/breast_cancer_model.h5"
)

print("\n====================================")
print("MODEL TRAINED SUCCESSFULLY")
print("====================================")