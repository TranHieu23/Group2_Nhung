import speech_recognition as sr

def listen_for_command():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Đang lắng nghe...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        print(f"Nhận diện lệnh: {text}")
        return text
    except sr.UnknownValueError:
        print("Không thể nhận dạng giọng nói")
        return None
    except sr.RequestError as e:
        print(f"Lỗi khi gửi yêu cầu đến Google Speech Recognition service; {e}")
        return None

def match_command(text, commands):
    text = text.lower()
    best_match = 0
    max_similarity = 0

    for i, command in enumerate(commands):
        similarity = sum(word in text for word in command.lower().split())
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = i

    return best_match

def main():
    commands = [
        "Không phải lệnh",
        "Mở cửa",
        "Bật đèn",
        "Tắt đèn"
    ]

    print("Chương trình đang chạy. Nói 'thoát' để dừng chương trình.")
    while True:
        text = listen_for_command()
        
        if text:
            if "thoát" in text.lower():
                break
            
            result = match_command(text, commands)
            print(result)

    print("Chương trình đã kết thúc.")

if __name__ == "__main__":
    main()