from presidio_analyzer import Pattern,AnalyzerEngine,PatternRecognizer
from app.core.config import CONFIDENCE_THRESHOLD, SUPPORTED_ENTITIES

class PIIHandler:
    def __init__(self):
        self.analyzer = AnalyzerEngine(default_score_threshold=CONFIDENCE_THRESHOLD,)
        self._add_custom_recognizers()
    
    def _add_custom_recognizers(self):
        project_id_pattern=Pattern(
            name="project_id_pattern",
            regex=r"\bPROJ-\d{3.6}\b",
            score=0.8
        )

        project_recognizer=PatternRecognizer(
            supported_entity="PROJECT_ID",
            patterns=[project_id_pattern],
            context=["project","task","sprint","assignment"]
        )

        self.analyzer.registry.add_recognizer(project_recognizer)
    
    def analyze_text(self, text:str):
        entities_to_find = SUPPORTED_ENTITIES + ["PROJECT_ID"]
        result=self.analyzer.analyze(text=text,language='en',entities=SUPPORTED_ENTITIES)
        return [res for res in result if res.score >= CONFIDENCE_THRESHOLD]
    
