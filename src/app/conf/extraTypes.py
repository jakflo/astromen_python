from typing import TypedDict


class ErrorReturned(TypedDict):
    error: str


class ValidationErrorReturned(TypedDict):
    validation_error: str
