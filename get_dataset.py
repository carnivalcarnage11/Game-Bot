# Arda Mavi
import os
import numpy as np
from keras.utils import to_categorical
from PIL import Image
from sklearn.model_selection import train_test_split

def get_img(data_path):
    # Getting image array from path:
    img = Image.open(data_path)
    img = img.resize((150, 150), Image.BILINEAR)
    img = np.array(img)
    return img

def save_img(img, path):
    Image.fromarray((img * 255).astype('uint8')).save(path)
    return

def get_dataset(dataset_path='Data/Train_Data'):
    # Getting all data from data path:
    try:
        X = np.load('Data/npy_train_data/X.npy')
        Y = np.load('Data/npy_train_data/Y.npy')
    except:
        labels = os.listdir(dataset_path) # Geting labels
        X = []
        Y = []
        count_categori = [-1,''] # For encode labels
        for label in labels:
            datas_path = dataset_path+'/'+label
            for data in os.listdir(datas_path):
                img = get_img(datas_path+'/'+data)
                X.append(img)
                # For encode labels:
                if data != count_categori[1]:
                    count_categori[0] += 1
                    count_categori[1] = data.split(',')
                Y.append(count_categori[0])
        # Create dateset:
        X = np.array(X).astype('float32')/255.
        Y = np.array(Y).astype('float32')
        Y = to_categorical(Y, count_categori[0]+1)
        if not os.path.exists('Data/npy_train_data/'):
            os.makedirs('Data/npy_train_data/')
        np.save('Data/npy_train_data/X.npy', X)
        np.save('Data/npy_train_data/Y.npy', Y)
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=0.1, random_state=42)
    return X, X_test, Y, Y_test

if __name__ == '__main__':
    # Test get_dataset and save_img
    X, X_test, Y, Y_test = get_dataset()
    print('Dataset shapes:', X.shape, X_test.shape, Y.shape, Y_test.shape)
    # Save a sample image
    if X.shape[0] > 0:
        save_img(X[0], 'test_img.png')
        print('Saved test_img.png')
