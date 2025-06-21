from datetime import date


class ValidatorHelper:
    firstNameMaxLength = 32
    lastNameMaxLength = 32
    skillNameMaxLength = 32

    @staticmethod
    def stringNotEmpty(value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Value cannot be empty")
        return cleaned

    @staticmethod
    def stringNotEmptyMaxLength(value: str, maxLength: int) -> str:
        cleaned = ValidatorHelper.stringNotEmpty(value)
        if len(value) > maxLength:
            raise ValueError("Value too long")
        return cleaned
        
    @staticmethod
    def enDate(value: str) -> str:
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError('dob must be in YYYY-mm-dd format')
        return value
