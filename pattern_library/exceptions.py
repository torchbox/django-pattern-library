

class PatternLibraryException(Exception):
    pass


class TemplateIsNotPattern(PatternLibraryException):
    pass


class PatternLibraryEmpty(PatternLibraryException):
    def __init__(self, message):
        self.message = message
