# Arda Mavi
import numpy as np
from PIL import Image

def predict(model, X):
    X = np.array(Image.fromarray(X).resize((150, 150), Image.BILINEAR)).astype('float32')/255.
    Y = model.predict(X.reshape(1,150,150,3))
    return Y

if __name__ == '__main__':
    # Simple test: create a dummy model and input, and call predict
    import numpy as np
    class DummyModel:
        def predict(self, x):
            print('DummyModel.predict called with shape:', x.shape)
            return np.array([[0.1, 0.2, 0.3, 0.4]])
    dummy_img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
    result = predict(DummyModel(), dummy_img)
    print('Prediction result:', result)
