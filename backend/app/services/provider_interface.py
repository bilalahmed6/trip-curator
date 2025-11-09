class BaseLLMProvider:
    def generate_response(self, prompt: str,max_tokens: int=None, temperature: float=0.0,**kwargs) -> str:
        raise NotImplementedError("This method should be overridden by subclasses")
    def generate_plan(self, prompt: str) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses")
    def generate_chat(messages: list[dict], max_tokens:int=None, temperature:float=0.0) -> dict:
        raise NotImplementedError("This method should be overridden by subclasses")
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError("This method should be overridden by subclasses")
    def token_count(self, text: str) -> int:
        raise NotImplementedError("This method should be overridden by subclasses")

class StubProvider(BaseLLMProvider):
    def generate_response(self, prompt: str) -> str:
        return f"Echo (stub): {prompt}"
    def generate_plan(self, prompt: str) -> dict:
        return {
            "title": f"Plan for: {prompt}",
            "days": [
                {"day": 1, "items": [{"time": "09:00", "place": "Sample Place", "notes": "Sample Notes"}]},
                {"day": 2, "items": [{"time": "10:00", "place": "Another Place", "notes": "More Notes"}]},
            ]
        }