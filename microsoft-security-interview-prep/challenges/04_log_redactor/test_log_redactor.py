import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_log_redactor" if use_practice else "solution_log_redactor"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_redacts_password_kv():
    assert (
        impl.redact("user login: username=alice password=hunter2")
        == "user login: username=alice password=[REDACTED]"
    )


def test_leaves_non_sensitive_kv_untouched():
    text = "nothing sensitive here, just a normal_key=normal_value"
    assert impl.redact(text) == text


def test_redacts_bearer_token():
    assert (
        impl.redact("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.abc.def")
        == "Authorization: Bearer [REDACTED]"
    )


def test_redacts_aws_access_key_without_keyword():
    assert (
        impl.redact("leaked key AKIAABCDEFGHIJKLMNOP in config dump")
        == "leaked key [REDACTED] in config dump"
    )


def test_redacts_credit_card_with_dashes():
    assert impl.redact("card on file: 4111-1111-1111-1111") == "card on file: [REDACTED]"


def test_redacts_credit_card_with_spaces():
    assert impl.redact("card: 4111 1111 1111 1111 exp 12/29") == "card: [REDACTED] exp 12/29"


def test_redacts_credit_card_no_separators():
    assert impl.redact("raw pan 4111111111111111 stored") == "raw pan [REDACTED] stored"


def test_does_not_swallow_trailing_fields():
    result = impl.redact("password=hunter2 next_field=x")
    assert result == "password=[REDACTED] next_field=x"


def test_redacts_various_secret_keywords():
    text = "api_key=abc123 secret: s3cr3t token=tok_9f8g pwd=letmein"
    result = impl.redact(text)
    assert "abc123" not in result
    assert "s3cr3t" not in result
    assert "tok_9f8g" not in result
    assert "letmein" not in result
    assert "api_key=[REDACTED]" in result
    assert "secret: [REDACTED]" in result
    assert "token=[REDACTED]" in result
    assert "pwd=[REDACTED]" in result


def test_redacts_quoted_value():
    result = impl.redact('password="hunter 2 is my pw"')
    assert result == "password=[REDACTED]"


def test_case_insensitive_keyword_preserves_key_casing():
    result = impl.redact("PASSWORD=hunter2")
    assert result == "PASSWORD=[REDACTED]"


def test_empty_string():
    assert impl.redact("") == ""
