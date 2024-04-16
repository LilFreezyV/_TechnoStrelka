import speech_recognition as sr

class SpeechRecognizer():

    def __init__(self) -> None:
        r = sr.Recognizer()
        text = ""
    
    def Recognize(self, voice_path: str, text_path: str):
        try:
            with sr.AudioFile(voice_path) as f:
                audio_data = self.r.record(f)
                text = self.r.recognize_google(audio_data, language="ru-RU")
                print(text)

            with open(text_path, "w") as f:
                f.write(text)
            
            return 0, "Succces"
        
        except Exception as e:
            return 1, e