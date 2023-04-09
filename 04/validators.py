class MinLengthValidator:
    def __init__(self, min_length=6):
        self.min_length = min_length

    def validate(self, value: str):
        if len(value) < self.min_length:
            raise ValueError(f'Password is too small.'
                             f' It must be {self.min_length} at least')


class EntirelyNumericValidator:
    def validate(self, value):
        if value.isdigit():
            raise ValueError('Password can`be be entirely numeric')
