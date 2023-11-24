import os
import cv2
import json
import numpy as np
import asyncio
import tensorflow as tf
from tensorflow import keras
from typing import Union
from sklearn.model_selection import train_test_split



IS_UNKNOWN = 0

IS_KNOWN = 1

IS_BLACKLISTED = 2



def get_model(model_path:str) -> keras.Sequential:

    loaded_model = keras.models.load_model(model_path)

    return loaded_model




class SecurityModel():

    def __init__(self, path_to_data:str, path_to_model:str):

        self.path_to_data = path_to_data

        self.path_to_model = path_to_model


    async def get_train_test_data(self, path:str) -> tuple:

        X = []

        y = []

        class_ids = []

        count = 0

        for entry in os.scandir(path):

            if entry.is_dir():

                class_id = entry.path.split("\\")[-1]

                for inner_entry in os.scandir(entry.path):
                
                    img_cv2 = cv2.imread(inner_entry.path)

                    grayscale_image = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)

                    scaled_cropped_grayscale_image = cv2.resize(grayscale_image, (40, 40))

                    X.append(scaled_cropped_grayscale_image)

                    y.append(count)

                count += 1

                class_ids.append(class_id)

        
        with open("class_dict.json", "w") as json_file:
            json.dump(class_ids, json_file)

        
        X = np.array(X)/ 255.0

        y = np.array(y)

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        return x_train, x_test, y_train, y_test


    async def train_evaluate_update(self, lenght_of_user:int):

        _train_test_task = asyncio.create_task(self.get_train_test_data(self.path_to_data))

        lenght_of_class_dict = len(await SecurityModel.get_class_dict())


        print("loaded test and training data.......")

        model = tf.keras.models.Sequential([

            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(40, 40, 1)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(lenght_of_class_dict, activation='softmax')
        ])


        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

        x_train, x_test, y_train, y_test = await _train_test_task

        model.fit(x_train, y_train, epochs=30, batch_size=32)

        test_loss, test_acc = model.evaluate(x_test, y_test)

        model.save(self.path_to_model)

        return (test_loss, test_acc)


    @staticmethod
    def get_class_dict(path:str=None)-> Union[dict, list]:

        with open(path, "r") as json_file:
            class_dict = json.load(json_file)

        return class_dict










    





