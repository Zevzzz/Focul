
import numpy as np
from keras.src.optimizers import Adam
from keras.src.models import Sequential
from keras.src import layers
# from keras.regularizers import l1, l2
from keras.src.callbacks import ModelCheckpoint, CSVLogger
from keras.src.saving import load_model
from os import remove

# Constants
TRAIN_2_TEST_RATIO_SPLIT_PERC = 0.9
MODEL_SAVE_PATH = 'model.keras'

EPOCHS = 50
BATCH_SIZE = 64



class NeuralNet:
    loadedModel = load_model(MODEL_SAVE_PATH)

    def __init__(self):
        # Building the model
        self.model = Sequential([])

        # Hidden layers
        # model.add(layers.Dense(units = 64, input_dim=len(pointsIn[0]), activation= 'relu')) # tune
        # model.add(layers.Dropout(0.5)) # tune

        self.model.add(layers.Dense(units=64, activation='relu', input_shape=(132,)))  # tune
        self.model.add(layers.Dense(units=64, activation='relu'))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(units=64, activation='relu'))

        # Output layers
        self.model.add(layers.Dense(units=1, activation='sigmoid'))

        # Training
        # model.compile(optimizer = Adam(learning_rate = 0.0003), loss = 'binary_crossentropy', metrics = ['accuracy']) # tune;
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

    def trainModel(self, focPointsIn, unfocPointsIn):
        focPoints = focPointsIn.copy()
        unfocPoints = unfocPointsIn.copy()

        np.random.shuffle(focPoints)
        np.random.shuffle(unfocPoints)

        min_size = min(len(focPoints), len(unfocPoints))
        focPoints = focPoints[:min_size]
        unfocPoints = unfocPoints[:min_size]

        focSplitPoint = int(len(focPoints) * TRAIN_2_TEST_RATIO_SPLIT_PERC)
        focPointsTrain = focPoints[:focSplitPoint]
        focPointsTest = focPoints[focSplitPoint:]

        unfocSplitPoint = int(len(unfocPoints) * TRAIN_2_TEST_RATIO_SPLIT_PERC)
        unfocPointsTrain = unfocPoints[:unfocSplitPoint]
        unfocPointsTest = unfocPoints[unfocSplitPoint:]

        focAndUnfocPointsTrain = np.concatenate((focPointsTrain, unfocPointsTrain))
        focAndUnfocPointsTest = np.concatenate((focPointsTest, unfocPointsTest))
        tagsTrain = np.concatenate((np.zeros(len(focPointsTrain)), np.ones(len(unfocPointsTrain))))
        tagsTest = np.concatenate((np.zeros(len(focPointsTest)), np.ones(len(unfocPointsTest))))

        focAndUnfocPointsTrain = focAndUnfocPointsTrain.reshape(len(focAndUnfocPointsTrain), -1)
        focAndUnfocPointsTest = focAndUnfocPointsTest.reshape(len(focAndUnfocPointsTest), -1)

        print(focAndUnfocPointsTrain.shape)
        print(focAndUnfocPointsTest.shape)

        trainingLogs = self.model.fit(
            focAndUnfocPointsTrain, tagsTrain, epochs=EPOCHS, batch_size=BATCH_SIZE,
            validation_data=(focAndUnfocPointsTest, tagsTest))

        try:
            remove('model.keras')
        except FileNotFoundError:
            pass
        self.model.save(MODEL_SAVE_PATH)

        np.save('src/data/TRAINING_HIST_VAL_ACC.npy', np.array(trainingLogs.history['val_accuracy']))


    def loadModel(self):
        self.loadedModel = load_model(MODEL_SAVE_PATH)

    def getModel(self):
        return self.loadedModel

    def predict(self, landmarks):
        landmarksShaped = landmarks.reshape(1, 132)

        return self.loadedModel.predict(landmarksShaped)




