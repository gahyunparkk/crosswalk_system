from pydub import AudioSegment
import os

def change_pitch(input_file, output_file, new_pitch):
    # 음성 파일 불러오기
    audio = AudioSegment.from_file(input_file)

    # 피치 변경하기
    modified_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * new_pitch)
    })

    # 변경된 음성 파일 저장하기
    modified_audio.export(output_file, format="wav")

#  변환할 파일들이 들어있는 디렉토리 설정
input_directory = "C:/Users/asd71/Desktop/newww/folder" #변환할 파일 들어있는 경로
output_directory = "C:/Users/asd71/Desktop/newww/0.6" #변환 후 파일 저장할 경로

# 변환할 파일들의 리스트 가져오기
input_files = os.listdir(input_directory)

# 변환할 피치 설정 (예: 여성 목 소리를 남성 목소리로 변경)
new_pitch = 0.6

# 모든 파일에 대해 변환 수행
for file_name in input_files:
    # 파일 경로 설정
    input_file_path = os.path.join(input_directory, file_name)
    output_file_path = os.path.join(output_directory, file_name)

    # 피치 변경 함수 호출
    change_pitch(input_file_path, output_file_path, new_pitch) 