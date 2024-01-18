
# Smart Door Bell

A Smart Door alert system on raspiberry pi using raspiberry pi camera module 5mp.

The face is trained using "haarcascade_frontalface".It gave around 70% accurate result with ideal lighting condition

House door opens automatically if the person registered in database comes in front else guest have the option to press the door bell to let the owner know via call bell or telegram bot.

This smart door system have intrusion detection system and a interative telegram update features.





## Installation

_Capturing Images_

```bash
  cd smart-door/face-detection
  python 01_face_capture_dataset.py
```
👆 This will start capturing 1000 Images

_Model Training_

```bash
  cd smart-door/face-detection
  python 02_face_training.py
```
👆 Model is now trained

_To check the accuracy of current registered face_

```bash
  cd smart-door/face-detection
  python 03_face_recogition.py
```
👆 This program will show the accuracy of the face on which it is trained, you can change the lighting condition to get better results.



## Main Program execution

```bash
  cd smart-door/face-detection
  python main.py
```
👆 Now you can play with the door bell
## Circuit and Flow Diagram
_Circuit_
![Circuit](https://cdn.discordapp.com/attachments/1197634717806247950/1197634872483778700/circuitdiagram.png?ex=65bbfb64&is=65a98664&hm=a791d245662eda6a427fdc14980fa05afb4ca4087f611cfb8e478a1b49476a40&)

_Flow Diagram_
![Flow Diagram](https://media.discordapp.net/attachments/1197634717806247950/1197634872878047292/flow.png?ex=65bbfb64&is=65a98664&hm=8a7f2b30eb1b07d196a1c5a13d0e1ebdaa0e3ff1f12b8bbc5088d424c65f0f7e&=&format=webp&quality=lossless&width=604&height=660)


## Components
- [Raspberry Pi 4](https://www.indianhobbycenter.com/products/raspberry-pi-5-model-b-with-4-gb-ram?_pos=5&_sid=90d82726b&_ss=r)
- [5MP camera Module](https://www.indianhobbycenter.com/products/raspberry-pi-camera-module?_pos=1&_sid=356a5ed8f&_ss=r)
- [SG90 Mini Servo - 180 Degree Rotation](https://www.indianhobbycenter.com/products/sg90-micro-servo-motor?_pos=1&_sid=5d334fdcf&_ss=r)
- [Digital IR Sensor Module IR Proximity LM393](https://www.indianhobbycenter.com/products/ir-sensor-module?_pos=1&_sid=d9ff90827&_ss=r)
- [16x2 1602 LCD Display (Yellow / Green) with i2c module](https://www.indianhobbycenter.com/products/0829u8outcy-jce-16-x-2-lcd-display?_pos=1&_sid=24913f4a4&_ss=r)

## 🔗 Contributors
![portfolio](https://img.shields.io/badge/Aman-000?style=for-the-badge&logo=ko-fi&logoColor=white)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/p-aman-kumar-subudhi-112a55227/)
[![github](https://img.shields.io/badge/github-1DA1F2?style=for-the-badge&logo=github&logoColor=white)](https://github.com/amansubudhi)

![portfolio](https://img.shields.io/badge/Ayush-000?style=for-the-badge&logo=ko-fi&logoColor=white)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ayush-jee-773a08209/)
[![github](https://img.shields.io/badge/github-1DA1F2?style=for-the-badge&logo=github&logoColor=white)](https://github.com/AyuushJee)

