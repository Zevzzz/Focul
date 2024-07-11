
import numpy as np
from keras.src.optimizers import Adam
from keras.src.models import Sequential
from keras.src import layers
from keras.regularizers import l1, l2
from keras.src.callbacks import ModelCheckpoint, CSVLogger

class NeuralNet():
    def __init__(self):
        # Building the model
        self.model = Sequential([])

        # Hidden layers
        # model.add(layers.Dense(units = 64, input_dim=len(pointsIn[0]), activation= 'relu')) # tune
        # model.add(layers.Dropout(0.5)) # tune
        # model.add(layers.Dense(units=32, activation='relu')) # tune
        self.model.add(layers.Dense(units=32, activation='relu'))
        self.model.add(layers.Dropout(0.5))
        self.model.add(layers.Dense(units=32, activation='relu'))

        # Output layers
        self.model.add(layers.Dense(units=1, activation='sigmoid'))

        # Training
        # model.compile(optimizer = Adam(learning_rate = 0.001), loss = 'binary_crossentropy', metrics = ['accuracy']) # tune;
        self.model.compile(optimizer=Adam(learning_rate=0.0003), loss='binary_crossentropy', metrics=['accuracy'])

    def trainModel(self, focPointsIn, unfocPointsIn):
        focPoints = focPointsIn.copy()
        unfocPoints = unfocPointsIn.copy()
        np.random.shuffle(focPoints)
        np.random.shuffle(unfocPoints)

        foc80Point = int(len(focPoints) * 0.8)
        focPointsTrain = focPoints[:foc80Point]
        focPointsTest = focPoints[foc80Point:]

        unfoc80Point = int(len(unfocPoints) * 0.8)
        unfocPointsTrain = unfocPoints[:unfoc80Point]
        unfocPointsTest = unfocPoints[unfoc80Point:]

        trainingLog = self.model.fit(focPointsTrain, tagsTrain, epochs=epochs, batch_size=64,
                                     validation_data=(pointsTest, tagsTest))  # tune
        model.save(modelPath)





