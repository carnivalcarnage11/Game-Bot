import shutil
import os

def remove_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Removed: {path}")
    else:
        print(f"Not found: {path}")

def main():
    # Paths to clear
    paths = [
        'Data/Train_Data/Keyboard',
        'Data/Train_Data/Mouse',
        'Data/npy_train_data',
        'Data/Checkpoints',
        'Data/Model',
    ]
    for path in paths:
        remove_dir(path)
    print("Training data and model checkpoints cleared.")

if __name__ == '__main__':
    main()
