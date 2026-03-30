import hashlib
from pathlib import Path

class FileHashCalculator:
    def __init__(self, file_path: str):
        """
        Initialize the calculator with the file path.
        :param file_path: path to the file as a string
        """
        self.file_path = Path(file_path)

        # Check if the file exists
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    def calculate_hashes(self, chunk_size=16 * 1024 * 1024) -> dict:
        """
        Compute MD5 and SHA-256 hashes of the file.
        :param chunk_size: size of each block read from the file (default: 4 MB)
        :return: dictionary containing the computed hashes
        """

        # Create hash objects
        md5_hash = hashlib.md5()
        sha256_hash = hashlib.sha256()

        # Open the file in binary mode
        with open(self.file_path, 'rb') as f:

            # Read the file in chunks to avoid loading it entirely into memory
            while True:
                chunk = f.read(chunk_size)

                # If chunk is empty, we reached the end of the file
                if not chunk:
                    break

                # Update both hashes with the same chunk
                md5_hash.update(chunk)
                #sha256_hash.update(chunk)

        # Return the hashes in hexadecimal format
        return {
            'md5': md5_hash.hexdigest(),
            'sha256': ""#sha256_hash.hexdigest()
        }