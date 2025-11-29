# backend/tests/test_yarn_tts_interactive.py

import asyncio
import os
from backend.ai.tts import text_to_speech, LANGUAGE_VOICES

# Directory to store generated audio
AUDIO_DIR = "backend/tests/audio1"
os.makedirs(AUDIO_DIR, exist_ok=True)

async def main():
    print("=== YarnGPT TTS Interactive Test ===\n")
    
    # Show available voices
    print("Available voices/languages:")
    for lang, voice in LANGUAGE_VOICES.items():
        print(f"- {lang.capitalize()}: {voice}")
    
    # User selects language
    language = input("\nEnter language (english/igbo/yoruba/hausa): ").strip().lower()
    if language not in LANGUAGE_VOICES:
        print("Invalid language, defaulting to English.")
        language = "english"
    
    # User enters text
    text = input("Enter text to convert to speech: ").strip()
    if not text:
        print("No text entered. Exiting.")
        return

    # Generate TTS
    print(f"\nGenerating TTS in {language.capitalize()} voice…")
    output_file = await text_to_speech(text, language_code=language)

    # Move file to AUDIO_DIR
    if output_file:
        filename = os.path.basename(output_file)
        final_path = os.path.join(AUDIO_DIR, filename)
        os.replace(output_file, final_path)
        print(f"TTS generated successfully: {final_path}")
    else:
        print("TTS failed.")

if __name__ == "__main__":
    asyncio.run(main())
