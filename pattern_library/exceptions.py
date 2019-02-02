

class PatternLibraryException(Exception):
    pass


class TemplateIsNotPattern(PatternLibraryException):
    pass


class PatternLibraryEmpty(PatternLibraryException):
    pass
