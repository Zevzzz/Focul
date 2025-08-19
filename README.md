# Focul
*A personalized ADHD focus assistant powered by computer vision and machine learning.*

## Overview
Focul is a computer application designed to help users who struggle with focusing or staying on task. It was especially designed for those who struggle with ADHD related focus issues. By using body landmark detection and a personalized neural network trained on each user's unique body language and body focus cues, Focul recognizes signs of distration and gently reminds users to refocus. 

Unlike many other productivity apps, Focul is truly personalized for each user, adapting to unique body language an habits, making it an intuitive and personal tool for focusing. 

### Features
- **Personalized Focus Detection** - Focul tracks the posture and various micro-movements of users (eyes, shoulders, face, etc.) to distinguish between focused and unfocused states
- **AI Powered** - Using a multi-layer perceptron for deep learning, Focul is able to recognize and remember subtle combinations of personalized focus cues that link with focused and unfocused states that users themselves may not even notice
- **Adaptive Model** - Focul is adaptive to each user, training based on study sessions and unfocused sessions to create a user-specific profile
- **Plug-and-play** - Focul comes with a pre-trained model based on a scraped dataset of focused and unfocused samples, so you can use it even before it learns your custom profile. No training needed.
- **Highly secure** - All Focul data is stored locally on your computer. Focul does not require, nor does it use any networking features. Focul also does not store image data of any kind, but rather a numerical model representing your posture patterns. We do not store or collect data of any kind from installed Focul apps. 

## Installation
Simply follow the instructions on the following installation doc (avg 3 min):
https://docs.google.com/document/u/0/d/1B17id3WCf5vyWAENmyov5GPuiHPFEj3u/mobilebasic

## Usage
After downloading the `.exe` file, simply run it to start Focul. A black terminal will open, do not close it as this will cause Focul to close. After a few seconds, the app UI will appear. 

To train a custom profile
1. Record a focused video. Click on the first button, “Record Focus Video”, the app will start to record 60 seconds of video and show the following webcam window, this will be used to train the AI engine, essentially teaching the engine on your focused gestures during study time. Please find a posture that you usually use during study time, like looking at your monitor, or look at your book. Feel free to record multiple gestures within the 60 seconds window, and you can click on the button again to re-record.
2. Record an Unfocused Video. Click on the second button, “Record Unfocused Video”, the app will start to record 60 seconds of video and show the follow webcam window. This will also be used to train the AI engine, so it learns to recognize posture patterns when you are not focused on studying, like playing with your phone, looking around, etc. Feel free to record multiple gestures within the 60 seconds window, and you can click on the button again to re-record.
3. Train your AI model. Click on the 3rd button “Train Model with Recordings”, this will trigger the AI engine to train it self (learn your gestures) based on the recorded videos. The training will take a few seconds and a popup will indicate it is completed. Click on OK to dismiss the pooup.

Now you are ready to use Focul!

To start a focus session simply click the "Start Monitoring Focus" button. A webcam feed will open, showing you the camera feed. In the top left of the window is a blue text box that indicates whether you are focused or not, and with what certainty the AI makes this prediction. When you are unfocused for more than 10 seconds, a popup will display to remind you to focus. You can dismiss it by clicking "OK".

## Future Improvements
We are working hard to implement new features and updates to help you further take back control over your studying and attention. Possible future improvements include:
1. Customizable focus durations and training parameters for flexibility and higher detection accuracy
2. CNN-based models and LSTM/GRU integration for smarter pattern recognition and handling of temporal data
3. A mobile version of the app for on-the-go monitoring (iOS/Android)
4. Pomodoro and smart break integration
5. Integration of music or ambient noise
6. An analytics dashboard to display focus stats and potential unfocused indicators



