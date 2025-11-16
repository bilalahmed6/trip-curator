def test_generate_response_monkeypatch(monkeypatch):
    from app.services.providers_hf import HuggingFaceProvider

    def mock_text_generation(prompt, max_new_tokens, temperature):
        return "This is a mocked response."

    monkeypatch.setattr("app.services.providers_hf.InferenceClient.text_generation", mock_text_generation)
    
    provider = HuggingFaceProvider()
    prompt = "Hello, how are you?"
    assert provider.generate_response(prompt) == "This is a mocked response."

def test_text_embedding_monkeypatch(monkeypatch):
    from app.services.providers_hf import HuggingFaceProvider

    def mock_text_embedding(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

    monkeypatch.setattr("app.services.providers_hf.InferenceClient.feature_extraction", mock_text_embedding)
    
    provider = HuggingFaceProvider()
    texts = ["Hello world", "Test embedding"]
    embeddings = provider.generate_embedding(texts)
    
    assert len(embeddings) == 2
    for emb in embeddings:
        assert emb == [0.1, 0.2, 0.3]