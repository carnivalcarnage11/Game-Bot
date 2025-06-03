# Game Bot
### By Arda Mavi

Game Bot is an artificial intelligence that learns to play any game by watching your actions. It records your keyboard and mouse movements while you play, then trains a deep learning model to mimic your gameplay.

## Features
- Records your keyboard and mouse actions while you play any game
- Trains a neural network to learn your play style
- Lets the AI play the game for you using the trained model

## How It Works
1. **Record Gameplay:** Run the dataset creation script and play your game. The program will record your actions and screenshots.
2. **Train the Model:** Use the training script to teach the AI how you play.
3. **Let the AI Play:** Run the AI script to watch the bot play the game using your style.

## Getting Started

### 1. Install Requirements
- Make sure you have **Python 3.10** installed (recommended for compatibility with TensorFlow and Keras).
- Install the required Python packages:
  ```
  pip install -r requirements.txt
  ```

### 2. Create a Training Dataset
1. Run the dataset creation script:
   ```
   python create_dataset.py
   ```
2. Play your game. The program will record your actions.
3. Stop the script with `Ctrl+C` when done.

### 3. Train the Model
Train the AI using your recorded data:
```
python train.py
```

### 4. Run the AI
Let the AI play the game:
```
python ai.py
```

### 5. (Optional) Use TensorBoard
To monitor training progress:
```
tensorboard --logdir=Data/Checkpoints/logs
```

## Notes
- Tested with Python 3.10.0 and 3.6.0
- This project is still under development
- If you encounter errors about missing data, make sure you have run `create_dataset.py` and played your game to generate training data before training or running the AI.
- If you see errors about missing modules, ensure you are using Python 3.10 and have installed all requirements.

## Windows Installation
1. Download and install Python 3.10.0: https://www.python.org/downloads/release/python-3100/
2. Open Command Prompt and run:
   ```
   pip install -r requirements.txt
   ```

---

Feel free to contribute or open issues. Enjoy teaching your AI to play games!
