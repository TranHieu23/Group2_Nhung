import speech_recognition as sr
from pydub import AudioSegment
import os
import google.generativeai as genai

# Cấu hình API key cho Gemini
genai.configure(api_key='')

# Hàm chuyển đổi file âm thanh thành văn bản
def audio_file_to_text(file_path):
    recognizer = sr.Recognizer()
    
    # Kiểm tra định dạng file và chuyển đổi nếu cần
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in ['.wav', '.aiff', '.flac']:
        print(f"Chuyển đổi file {file_extension} sang WAV...")
        audio = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit('.', 1)[0] + '.wav'
        audio.export(wav_path, format="wav")
        file_path = wav_path

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        print(f"Nội dung file âm thanh: {text}")
        return text
    except sr.UnknownValueError:
        print("Không thể nhận dạng giọng nói trong file")
        return None
    except sr.RequestError as e:
        print(f"Lỗi khi gửi yêu cầu đến Google Speech Recognition service; {e}")
        return None

# ... (phần còn lại của mã giữ nguyên)

# Hàm chính
def main():
    input_file = "D:/Downloads/testing voice/testing voice/testing.wav"  # Thay đổi tên file này theo file âm thanh của bạn
    output_file = "response.mp3"

    text = audio_file_to_text(input_file)
    if text:
        processed_text = process_text(text)
        command_response = check_command(text)
        if command_response != "Không phải lệnh đã định nghĩa":
            response = command_response
        else:
            response = processed_text
        print(f"Phản hồi: {response}")
        text_to_speech(response, output_file)

if __name__ == "__main__":
    main()