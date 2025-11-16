def test_token_count():
    from app.services.token_utils import count_tokens

    assert count_tokens("Hello world!") > 0