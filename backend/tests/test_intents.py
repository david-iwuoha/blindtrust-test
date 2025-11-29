from backend.ai.intents import parse_intent

def test_transfer():
    text = "Transfer 2000 to John"
    result = parse_intent(text)
    assert result["intent"] == "transfer"
    assert result["slots"]["recipient"] == "John"
    assert result["slots"]["amount"] == 2000
    print(result)

def test_language():
    text = "I want Yoruba"
    result = parse_intent(text)
    assert result["intent"] == "set_language"
    assert result["slots"]["language"] == "yoruba"
    print(result)

if __name__ == "__main__":
    test_transfer()
    test_language()
