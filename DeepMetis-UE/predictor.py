from tensorflow import keras
import numpy as np

from distance_calculator import calc_angle_distance
from properties import MODELS, MISB_TSHD

import glob


class Predictor:

    # Load the pre-trained model.
    PREDICTORS = [keras.models.load_model(p, compile=False) for p in glob.glob(MODELS + '/*.h5')]
    #model = keras.models.load_model(MODEL)
    print("Loaded model from disk")

    @staticmethod
    def predict(predictor_index, img, head_pose, label):
        model = Predictor.PREDICTORS[predictor_index]
        #shape is (1, 36, 60, 1)
        # other shape is (1,2)
         #Predictions vector
        predictions = model.predict([img, head_pose])

        predictions1 = list()
        confidences = list()

        for i in range(len(predictions)):
            prediction1 = predictions[i]
            explabel = label[i]

            diff = calc_angle_distance(prediction1, explabel)
            diff = np.abs(np.degrees(diff))
            confidence = MISB_TSHD - diff

            predictions1.append(prediction1)
            confidences.append(confidence)

        return predictions1, confidences
