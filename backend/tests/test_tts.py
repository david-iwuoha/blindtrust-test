# backend/tests/test_tts.py

import os
import asyncio
import pytest
from backend.ai.tts import text_to_speech

@pytest.mark.asyncio
async def test_english_tts():
    text = "Hello, this is a test."
    output_file = await text_to_speech(text, language_code="english", output_format="mp3")
    assert output_file.endswith(".mp3")
    assert os.path.exists(output_file)
    os.remove(output_file)

@pytest.mark.asyncio
async def test_yoruba_tts():
    text = "Bawo ni, eyi ni idanwo."
    output_file = await text_to_speech(text, language_code="yoruba", output_format="mp3")
    assert output_file.endswith(".mp3")
    assert os.path.exists(output_file)
    os.remove(output_file)

@pytest.mark.asyncio
async def test_igbo_tts():
    text = "Ndewo, nke a bụ ule."
    output_file = await text_to_speech(text, language_code="igbo", output_format="mp3")
    assert output_file.endswith(".mp3")
    assert os.path.exists(output_file)
    os.remove(output_file)

@pytest.mark.asyncio
async def test_hausa_tts():
    text = "Sannu, wannan gwaji ne."
    output_file = await text_to_speech(text, language_code="hausa", output_format="mp3")
    assert output_file.endswith(".mp3")
    assert os.path.exists(output_file)
    os.remove(output_file)
