# Arda Mavi
import os
import numpy
from get_dataset import get_dataset
from get_model import get_model, save_model
from keras.callbacks import ModelCheckpoint, TensorBoard

epochs = 100
batch_size = 5

def train_model(model, X, X_test, Y, Y_test):
    checkpoints = []
    if not os.path.exists('Data/Checkpoints/'):
        os.makedirs('Data/Checkpoints/')

    checkpoints.append(ModelCheckpoint('Data/Checkpoints/best_weights.weights.h5', monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=True, mode='auto'))
    checkpoints.append(TensorBoard(log_dir='Data/Checkpoints/./logs', histogram_freq=0, write_graph=True, write_images=False))

    model.fit(X, Y, batch_size=batch_size, epochs=epochs, validation_data=(X_test, Y_test), shuffle=True, callbacks=checkpoints)

    return model

def main():
    X, X_test, Y, Y_test = get_dataset()
    num_classes = Y.shape[1]
    model = get_model(num_classes)
    model = train_model(model, X, X_test, Y, Y_test)
    save_model(model)
    return model

if __name__ == '__main__':
    main()
