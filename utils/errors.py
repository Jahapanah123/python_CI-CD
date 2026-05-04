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


class AuthError(Exception):
    """Base class for all authentication exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsError(AuthError):
    """Raised when attempting to register an email that is already in use"""
    pass

class InvalidCredentialsError(AuthError):
    """Raised when email/password combination doesn't match"""
    pass

class InvalidTokenError(AuthError):
    """Raised when a JWT cannot be decoded or is structurally malformed"""
    pass

class TokenExpiredError(AuthError):
    """Raised when a JWT's exp claim is in the past"""
    pass

class RefreshTokenNotFoundError(AuthError):
    """Raised when the refresh token string isn't in the DB"""
    pass

class RefreshTokenRevokedError(AuthError):
    """Raised when the refresh token exists but has been revoked"""
    pass

class RefreshTokenExpiredError(AuthError):
    """Raised when the refresh token exists but has passed its expiry"""
    pass

class UserNotFoundError(AuthError):
    """Raised when a user_id from a token doesn't match any DB record"""
    pass

class UserInactiveError(AuthError):
    """Raised when authenticating with a deactivated account"""
    pass