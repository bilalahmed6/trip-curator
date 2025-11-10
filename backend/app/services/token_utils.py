# token_utils.py
try:
    import tiktoken
    _TIK = True
except Exception:
    _TIK = False

def count_tokens(text: str, model: str = "gpt2") -> int:
    if _TIK:
        try:
            enc = tiktoken.encoding_for_model(model)
            return len(enc.encode(text))
        except Exception:
            pass  
         # Try OpenAI / tiktoken
        try:
            from transformers import autoTokenizer
            tokenizer = autoTokenizer.from_pretrained(model)
            return len(tokenizer.encode(text))
        except Exception:
            pass
        # Fallback to simple word count
        return len(text.split())

        

   
   
        



    # Fallback estimate
    return max(1, len(text)//4)