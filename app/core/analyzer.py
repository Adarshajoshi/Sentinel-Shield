from presidio_analyzer import Pattern,AnalyzerEngine,PatternRecognizer

class PIIHandler:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self._add_custom_recognizers()
    
    def _add_custom_recognizers(self):
        project_id_pattern=Pattern(
            name="project_id_pattern",
            regex=r"\bPROJ-\d{5}\b",
            score=0.5
        )

        project_recognizer=PatternRecognizer(
            supported_entity="PROJECT_ID",
            patterns=[project_id_pattern],
            context=["project","task","sprint","assignment"]
        )

        self.analyzer.registry.add_recognizer(project_recognizer)
    
    def analyze_text(self, text:str):
        return self.analyzer.analyze(text=text,language='en')
    
