# 🔊 음성인식 음향신호기: 시각장애인을 위한 비신호 횡단보도 안내 시스템
> **2024 공학설계(캡스톤디자인) 프로젝트**

---

## 📌 Project Overview
시각장애인이 신호등이 없는 비신호 횡단보도를 건널 때 겪는 위험을 줄이기 위한 **지능형 안내 시스템**입니다. 기존 음향신호기의 물리적 버튼 조작 한계를 **음성인식(Mint AI 칩)** 으로 보완하고, **YOLOv5 영상 처리**를 통해 실시간 차량 접근 여부를 판단하여 시각장애인의 안전한 보행을 지원합니다.

## 🛠️ Tech Stack
### Hardware
- **NPU**: Pebble Square Mint AI Chip (3세대 뉴로모픽 아키텍처)
- **Controller**: Raspberry Pi 4
- **Computing**: PC (for Video Processing)

### Software & AI Models
- **Voice Recognition**: Mint AI Chip (Custom Trained Model)
- **Object Detection**: YOLOv5
- **Programming**: Python, PyTorch
- **Tools**: Audacity (Audio Processing), Clover Dubbing

---

## 📂 Repository Structure
```
├── bin/                              # Mint AI 칩 전용 음성인식 바이너리
├── notebooks/
│   └── yolo_train.ipynb              # YOLOv5 모델 학습 과정 기록
├── src/
│   ├── detect_car.py                 # [Main] 실시간 차량 탐지 및 상황 판단 로직
│   ├── raspberrypi_send_signal.py    # Mint AI 칩 신호 수신 및 Serial 전송
│   ├── pitch.py                      # 데이터 증강용 음성 피치 조절 코드
│   ├── best.pt                       # YOLOv5 학습 가중치
│   ├── cross_guide.mp3               # 보행 가능 안내 음성
│   └── warning_guide.mp3             # 차량 접근 경고 음성
└── README.md
```

---

## 🧠 System Architecture

본 시스템은 하드웨어 가속기(Mint AI)와 메인 프로세서(PC/Raspberry Pi) 간의 상호작용을 통해 동작합니다.

1. **Voice Trigger (Edge)**: 사용자가 "도와주세요", "확인해 주세요" 등의 명령어를 발화하면 **Mint AI 칩**이 이를 실시간으로 인식합니다.
2. **Signal Transmission**: Mint AI 칩이 음성을 인식하면 특정 **GPIO 핀**을 통해 라즈베리파이에 신호를 보냅니다. 라즈베리파이는 이 신호를 감지하여 **Serial 통신**으로 PC의 메인 분석 로직을 호출합니다.
3. **Vision Analysis**: PC에 연결된 카메라를 통해 실시간 영상을 획득하고, **YOLOv5** 모델이 차량 객체(Car, Truck, Bus, Motorcycle, Bicycle)를 탐지합니다.
4. **Decision Logic**: **0.5초 간격의 프레임 비교**를 통해 차량의 위치 변화 및 객체 수 변화를 분석하여 "차가 접근 중인 상황"인지를 최종 판단합니다.
5. **Audio Feedback**: 판단 결과에 따라 스피커를 통해 상황별 안내 멘트를 출력합니다.

<img width="1020" height="307" alt="Image" src="https://github.com/user-attachments/assets/2c58cf93-239a-40c6-a468-8aeced2d3715" />

---

## 📊 Data Engineering & Training

### 1. Voice Recognition (Mint AI Chip)
* **Dataset Construction**:
    * 제공된 데이터셋과 직접 녹음 및 클로바더빙을 활용한 음성 데이터 확보
    * **Data Augmentation**: `pitch.py`를 활용하여 약 400개의 기본 데이터를 피치 조절을 통해 **3,300개**로 확장
    * 최종적으로 명령어당 약 5,000개의 데이터셋을 구축하여 학습에 활용
* **Training**: Epoch 100회 학습 후 Mint AI 칩에서 사용할 바이너리 파일 생성

<img width="482" height="323" alt="Image" src="https://github.com/user-attachments/assets/2591b409-9dec-4d90-b1a3-d0f6e2375ff5" />

### 2. Object Detection (YOLOv5)
* **Dataset**: Microsoft COCO 오픈소스 데이터셋 활용
* **Filtering**: 80개 클래스 중 프로젝트 목적에 맞는 5가지 차량 클래스(car, truck, bus, motorcycle, bicycle)를 대상으로 탐지
* **Hyperparameters**:
    * **Image Size**: 640
    * **Batch Size**: 16
    * **Epochs**: 100

<img width="513" height="257" alt="Image" src="https://github.com/user-attachments/assets/b52e2640-f6dc-4b8f-a515-81cbd483845c" />

---

## ⚠️ Usage & Compatibility
* **Hardware Dependent**: `bin/` 폴더의 파일은 **Pebble Square Mint AI 칩** 전용 바이너리이며 해당 하드웨어 환경에서 사용됩니다.
* **Version Info**: 본 프로젝트는 2024년 개발 당시의 Mint AI 칩 환경을 기준으로 제작되었습니다. 펌웨어나 SDK 버전에 따라 사용 방법이 달라질 수 있습니다.
* **Vision Model**: 차량 탐지 가중치는 `src/best.pt`에 포함되어 있습니다.
* **Runtime Environment**: `detect_car.py` 실행 시 카메라와 스피커가 연결된 환경 및 YOLOv5/PyTorch 실행 환경이 필요합니다.

---

## 💡 Key Features
* **Voice-based Interface**: 물리적 버튼 대신 음성 명령을 활용하여 시스템을 호출합니다.
* **Vehicle Approach Detection**: YOLOv5 탐지 결과와 프레임 간 위치 변화를 이용해 차량 접근 여부를 판단합니다.
* **Edge + Host Integration**: Mint AI 칩, Raspberry Pi, PC를 연결해 음성 입력부터 영상 판단 및 음성 안내까지 하나의 파이프라인으로 구성했습니다.

---

## 🎬 Demo Video
시각장애인을 위한 음성인식 기반 비신호 횡단보도 안내 시스템의 실제 동작 시연 영상

[![음성인식 음향신호기 시연 영상](https://img.youtube.com/vi/wU2Vav3Km4s/0.jpg)](https://youtu.be/wU2Vav3Km4s)
> 🔗 [YouTube](https://youtu.be/wU2Vav3Km4s?si=_Jd-LkCpVqHVwnVk)

---

## 📚 References
* **Hardware**: [Pebble Square 공식 웹사이트 (Mint AI Chip)](http://pebble-square.com/)
* **Model**: [Ultralytics YOLOv5 GitHub Repository](https://github.com/ultralytics/yolov5)
* **Dataset**: [Microsoft COCO Dataset](https://cocodataset.org/)
* **Voice**: [Clova Dubbing](https://clovadubbing.naver.com/) (AI 보이스 데이터 생성 활용)
