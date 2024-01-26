from user.models import Student


class StudentToken:
    BASE_STUDENT_TOKENS = 10

    def __init__(self, _: Student):
        pass

    def tokens(self) -> int:
        return self.BASE_STUDENT_TOKENS
