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