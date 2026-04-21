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
├── bin/                      # Mint AI 칩 전용 바이너리 (음성 모델 학습 파일)
├── models/
│   └── best.pt               # YOLOv5 차량 인식 최적 가중치 파일
├── src/
│   ├── detect_car.py         # [Main] 실시간 차량 탐지 및 상황 판단 로직
│   ├── raspberrypi_send_signal.py  # Mint AI 칩 신호 수신 및 Serial 전송
│   |── pitch.py              # 데이터 증강(Augmentation)용 음성 피치 조절 코드
│   ├── best.pt               # YOLOv5 학습 모델
│   ├── cross_guide.mp3       # 보행 안전 음성 출력 파일
│   └── warning_guide.mp3     # 보행 위험 음성 출력 파일
├── notebooks/
│   └── yolo_train.ipynb      # YOLOv5 모델 학습 과정 기록
└── README.md
```

---

## 🧠 System Architecture

본 시스템은 하드웨어 가속기(Mint AI)와 메인 프로세서(PC/Raspberry Pi) 간의 긴밀한 상호작용을 통해 실시간 안정성을 확보합니다.

1. **Voice Trigger (Edge)**: 사용자가 "도와주세요", "확인해 주세요" 등의 명령어를 발화하면 **Mint AI 칩**이 이를 실시간으로 인식합니다. 초저전력 PIM 아키텍처 덕분에 항상 깨어있는(Always-on) 상태를 유지할 수 있습니다.
2. **Signal Transmission**: Mint AI 칩이 음성을 인식하면 특정 **GPIO 핀**을 통해 라즈베리파이에 신호를 보냅니다. 라즈베리파이는 이 신호를 감지하여 **Serial 통신**으로 PC의 메인 분석 로직을 호출합니다.
3. **Vision Analysis**: PC에 연결된 카메라를 통해 실시간 영상을 획득하고, **YOLOv5** 모델이 차량 객체(Car, Truck, Bus, Motorcycle, Bicycle)를 탐지합니다. 
4. **Decision Logic**: **0.5초 간격의 프레임 비교**를 통해 차량의 위치 변화 및 객체 수 변화를 분석하여 "차가 접근 중인 상황"인지를 최종 판단합니다.
5. **Audio Feedback**: 판단 결과에 따라 스피커를 통해 상황별 맞춤형 안내 멘트("20m 전방에 차가 오고 있습니다" 등)를 출력합니다.
<img width="1020" height="307" alt="Image" src="https://github.com/user-attachments/assets/2c58cf93-239a-40c6-a468-8aeced2d3715" />

---

## 📊 Data Engineering & Training

### 1. Voice Recognition (Mint AI Chip)
* **Dataset Construction**: 
    * 제공된 데이터셋과 직접 녹음 및 클로바더빙을 활용한 고품질 음성 데이터 확보.
    * **Data Augmentation**: `pitch.py`를 활용하여 약 400개의 기본 데이터를 피치 조절을 통해 **3,300개**로 확장하여 데이터 부족 문제를 해결했습니다.
    * 최종적으로 명령어당 약 5,000개의 데이터셋을 구축하여 학습에 활용했습니다.
* **Training**: 인식 정확도를 극대화하기 위해 Epoch 100회 학습을 진행하여 Mint AI 칩에 최적화된 바이너리 파일을 생성했습니다.
<img width="482" height="323" alt="Image" src="https://github.com/user-attachments/assets/2591b409-9dec-4d90-b1a3-d0f6e2375ff5" />

### 2. Object Detection (YOLOv5)
* **Dataset**: Microsoft COCO 오픈소스 데이터셋 활용.
* **Filtering**: 80개의 클래스 중 프로젝트 목적에 맞는 5가지 차량 클래스(car, truck, bus, motorcycle, bicycle)만 필터링하여 실시간 처리 속도를 높였습니다.
* **Hyperparameters**:
    * **Image Size**: 640
    * **Batch Size**: 16
    * **Epochs**: 100
<img width="513" height="257" alt="Image" src="https://github.com/user-attachments/assets/b52e2640-f6dc-4b8f-a515-81cbd483845c" />

---

## ⚠️ Important Note (Usage & Compatibility)
* **Hardware Dependent**: 본 리포지토리의 `bin/` 폴더 내 파일은 **Pebble Square Mint AI 칩(3세대 뉴로모픽 PIM 아키텍처)** 전용으로 빌드된 바이너리입니다. 해당 하드웨어 가속기가 연결된 환경에서만 음성 인식 트리거가 작동합니다.
* **Version Info**: 본 프로젝트는 2024년 개발된 Mint AI 칩 버전을 기준으로 제작되었습니다. 칩의 펌웨어 버전이나 SDK 업데이트 상황에 따라 호환성 및 업로드 방식이 다를 수 있습니다.
* **Environment**: `detect_car.py` 실행을 위해서는 카메라(Webcam)와 스피커가 연결된 컴퓨팅 환경이 필요하며, YOLOv5 구동을 위한 PyTorch 환경 설정이 선행되어야 합니다.

---

## 💡 Key Features & Expectations
* **접근성(Accessibility) 개선**: 기존 음향신호기는 물리적 버튼 위치를 찾기 어렵다는 단점이 있으나, 본 시스템은 **비접촉 음성 인터페이스**를 통해 시각장애인의 접근성을 비약적으로 높였습니다.
* **실시간 안전성(Safety) 강화**: 단순히 신호등의 상태를 읽어주는 것을 넘어, **YOLOv5 기반의 실시간 객체 추적**을 통해 실제 차량의 접근 여부를 판단하므로 비신호 횡단보도에서도 안전한 보행이 가능합니다.
* **높은 경제성(Efficiency)**: 고가의 지능형 신호등 설치가 어려운 이면도로나 골목길 등에 **초저전력 엣지 AI 칩**을 활용한 저비용 안내 시스템을 구축함으로써 사회적 안전망을 확대할 수 있습니다.

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
