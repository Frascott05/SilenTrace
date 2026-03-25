import hashlib
from pathlib import Path

class FileHashCalculator:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
    
    def calculate_hashes(self) -> dict:
        """Calculate MD5 and SHA-256 hashes and return as dict."""
        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()


        with open(self.file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
                
        print("fine calcolo")
        result = {
            'md5': md5_hash.hexdigest(),
            'sha256': sha256_hash.hexdigest()
        }
        
        return result