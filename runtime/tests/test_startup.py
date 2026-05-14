import os
import pytest
from unittest.mock import patch
from core.startup import validate


def test_missing_openai_key_reported():
    with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
        errors = validate("openai")
    assert any("OPENAI_API_KEY" in e for e in errors)


def test_missing_anthropic_key_reported():
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": ""}, clear=False):
        errors = validate("anthropic")
    assert any("ANTHROPIC_API_KEY" in e for e in errors)


def test_unknown_provider_no_key_error():
    errors = validate("unknown_provider")
    assert not any("API_KEY" in e for e in errors)


def test_returns_list():
    errors = validate("openai")
    assert isinstance(errors, list)


def test_all_errors_are_strings():
    errors = validate("openai")
    for e in errors:
        assert isinstance(e, str), f"Error entry is not a string: {e!r}"


def test_key_set_removes_key_error():
    with patch.dict(os.environ, {"OPENAI_API_KEY": "sk-test-key"}, clear=False):
        errors = validate("openai")
    assert not any("OPENAI_API_KEY" in e for e in errors)
