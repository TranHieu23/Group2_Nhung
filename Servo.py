import speech_recognition as sr
import RPi.GPIO as GPIO # type: ignore
import time

# Thiết lập cho servo
GPIO.setmode(GPIO.BCM)
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

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

def set_angle(angle):
    duty = (angle / 18) + 2.5
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def main():
    commands = [
        "Không phải lệnh",
        "Mở cửa",
        "Bật đèn",
        "Tắt đèn"
    ]

    print("Chương trình đang chạy. Nói 'thoát' để dừng chương trình.")
    try:
        while True:
            text = listen_for_command()
            
            if text:
                if "thoát" in text.lower():
                    break
                
                result = match_command(text, commands)
                print(f"Kết quả nhận dạng: {result}")
                
                if result == 1:  # "Mở cửa"
                    print("Di chuyển servo đến góc 180 độ")
                    set_angle(180)
                elif result == 2:  # "Bật đèn"
                    print("Bật đèn (mô phỏng)")
                elif result == 3:  # "Tắt đèn"
                    print("Tắt đèn (mô phỏng)")
                else:
                    print("Không thực hiện hành động")

    except KeyboardInterrupt:
        print("Chương trình bị ngắt bởi người dùng")
    finally:
        pwm.stop()
        GPIO.cleanup()
        print("Chương trình đã kết thúc.")

if __name__ == "__main__":
    main()