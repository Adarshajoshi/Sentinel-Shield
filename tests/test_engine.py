import pytest
from app.core.engine import ShieldEngine

def test_pii_masking_integrity():
    engine=ShieldEngine()
    session_id="test_session_001"

    raw_test="Contact me at john@gmail.com"

    masked=engine.protect_prompt(session_id,raw_test) 

    assert "[EMAIL_ADDRESS_1]" in masked
    assert "@" not in masked
    assert "alice" not in masked

def test_rehydration_logic():
    engine=ShieldEngine()
    session_id="test_session_123"

    raw_test="email is john@gmail.com"

    masked=engine.protect_prompt(session_id,raw_test)
    rehydrated=engine.reconstruct_response(session_id,masked)

    assert rehydrated==raw_test

def test_empty_string():
    """Does the engine crash if the input is empty?"""
    engine = ShieldEngine()
    result = engine.protect_prompt("session_999", "")
    assert result == ""

def test_no_pii_present():
    """Does the engine leave normal text untouched?"""
    engine = ShieldEngine()
    # Change "today" to something less 'date-like'
    text = "The weather is quite rainy." 
    result = engine.protect_prompt("session_999", text)
    assert result == text

    
def test_long_document_performance():
    """Does the engine handle a large block of text efficiently?"""
    engine = ShieldEngine()
    # Create a long string with 100 fake names
    long_text = "My name is John Doe. " * 100 
    result = engine.protect_prompt("session_perf", long_text)
    
    # Check if masking happened
    assert "[PERSON_" in result
    assert "John Doe" not in result