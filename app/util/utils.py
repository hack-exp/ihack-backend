import uuid
from app.core.config import settings


class IDGenerator:
    """
    Utility class for generating unique IDs and random 6-letter words.

    Methods:
    - generate_unique_id() -> str:
      Generates a unique ID using UUID.

    - generate_6letter_word() -> str:
      Generates a random 6-letter word composed of uppercase and lowercase letters.

    Returns:
    - str: A string representation of the generated unique ID or 6-letter word.
    """

    @staticmethod
    def generate_unique_id() -> str:
        """
        Generates a unique ID using UUID.

        Returns:
        - str: A string representation of the generated unique ID.
        """
        return str(uuid.uuid4())