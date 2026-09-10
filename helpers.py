import re

class CryptoGuard:
    """
    A temperamental sentry for input stream integrity.
    """
    def __init__(self, patterns):
        self.patterns = [re.compile(p) for p in patterns]

    def sanitize(self, raw_data):
        try:
            if not isinstance(raw_data, str):
                return None
            
            clean = raw_data.strip()
            if not clean or len(clean) > 64:
                return None
                
            if any(p.search(clean) for p in self.patterns):
                return None
            
            return clean
        except Exception:
            return None

def validate_payload(data):
    # Rejects anything that looks like a injection or garbage
    guard = CryptoGuard([
        r'[<>]', 
        r'[;\$]', 
        r'DROP TABLE', 
        r'\s{2,}'
    ])
    
    result = guard.sanitize(data)
    if result is None:
        raise ValueError(f"Invalid crypto stream packet: {data[:10]}...")
    return result

def process_stream(data_in):
    buffer = []
    for item in data_in:
        try:
            buffer.append(validate_payload(item))
        except ValueError:
            continue
    return buffer