from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

class PIIAnonymizer:
    def __init__(self):
        self.engine = AnonymizerEngine()

    def anonymize(self, text, analyzer_results, mode):
        """
        Performs permanent anonymization (Redact or Hash).
        This does NOT store data in the Vault.
        """
        if mode == "redact":
            # Turns "John" into "<PERSON>"
            operators = {"DEFAULT": OperatorConfig("redact", {})}
        elif mode == "hash":
            # Turns "John" into "f7ad9e..."
            operators = {"DEFAULT": OperatorConfig("hash", {})}
        else:
            return text

        result = self.engine.anonymize(
            text=text,
            analyzer_results=analyzer_results,
            operators=operators
        )
        return result.text