from gtts import gTTS  
import os  

def text_to_speech(text, lang="hi", filename="news_analysis.mp3"):
    print("Generating speech...")  # Debugging print statement

    tts = gTTS(text, lang=lang)  
    tts.save(filename)  
    print(f"Speech saved as {filename}")  # Confirm the file is saved

    os.system(f"start {filename}")  # Play the file (for Windows)

if __name__ == "__main__":
    sample_text = "यह हिंदी में एक परीक्षण संदेश है।"
    text_to_speech(sample_text)


