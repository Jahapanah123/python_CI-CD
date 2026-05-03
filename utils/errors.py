class TodoError(Exception):
    """Base class for all Todo exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationError(TodoError):
    """Raised for invalid input, empty titles, or non-positive IDs (400)"""
    pass

class ConflictError(TodoError):
    """Raised for duplicate titles (409)"""
    pass

class NotFoundError(TodoError):
    """Raised when a task doesn't exist in the database (404)"""
    pass