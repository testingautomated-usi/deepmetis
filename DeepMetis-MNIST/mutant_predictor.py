from tensorflow import keras
import numpy as np
import glob

from properties import MUT_MODELS, num_classes

#TODO: remove duplicate predictor
class Predictor:

    # Load the pre-trained model.
    PREDICTORS = [keras.models.load_model(p) for p in glob.glob(MUT_MODELS + '/*.h5')]
    # model = keras.models.load_model(MODEL)
    print("Loaded model from disk")

    @staticmethod
    def predict(predictor_index, img, label):
        model = Predictor.PREDICTORS[predictor_index]
        # Predictions vector
        predictions = model.predict(img)

        predictions1 = list()
        confidences = list()
        for i in range(len(predictions)):
            preds = predictions[i]
            explabel = label[i]
            prediction1, prediction2 = np.argsort(-preds)[:2]

            # Activation level corresponding to the expected class
            confidence_expclass = preds[explabel]

            if prediction1 != explabel:
                confidence_notclass = preds[prediction1]
            else:
                confidence_notclass = preds[prediction2]

            confidence = confidence_expclass - confidence_notclass
            predictions1.append(prediction1)
            confidences.append(confidence)

        return predictions1, confidences
