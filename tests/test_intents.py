from app.intents import classify

def test_basic_classify():
    intent, slots = classify("What is the score of Berlin FC vs Munich United?")
    assert intent == "score_match"
    assert "a" in slots and "b" in slots

def test_team_scorers():
    intent, slots = classify("Who scored for Berlin FC")
    assert intent == "who_scored_team"
    assert "team" in slots

def test_matches_today():
    intent, slots = classify("Show matches today")
    assert intent == "matches_today"
