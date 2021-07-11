from tensorflow import keras
import numpy as np
import glob

from distance_calculator import calc_angle_distance
from properties import MUT_MODELS, num_classes, MISB_TSHD


class Predictor:

    # Load the pre-trained model.
    PREDICTORS = [keras.models.load_model(p, compile=False) for p in glob.glob(MUT_MODELS + '/*.h5')]
    # model = keras.models.load_model(MODEL)
    print("Loaded model from disk")

    @staticmethod
    def predict(predictor_index, img, head_pose, label):
        model = Predictor.PREDICTORS[predictor_index]
        #img = [img,img]
        #img = np.reshape(img, (-1, 36, 60, 1))
        #img = np.array([img])

        #head_pose = (np.array([head_pose]))
        #head_pose = [head_pose, head_pose]
        #head_pose = np.reshape(head_pose, (-1, 2))
        #head_pose = np.array([head_pose])
        #print(head_pose.shape)
         #Predictions vector
        #predictions = model.predict([img, np.array([head_pose])])
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
