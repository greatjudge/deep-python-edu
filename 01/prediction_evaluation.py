class SomeModel:
    def predict(self, message: str) -> float:
        pass


def predict_message_mood(message: str,
                         model: SomeModel,
                         bad_thresholds: float = 0.3,
                         good_thresholds: float = 0.8) -> str:
    if bad_thresholds >= good_thresholds:
        raise ValueError('bad_threshold must be lower that good_threshold')
    if not isinstance(model, SomeModel):
        raise TypeError(f'model must be instance of SomeModel, not {type(model)}')

    prediction = model.predict(message)
    if prediction < bad_thresholds:
        return 'неуд'
    elif prediction > good_thresholds:
        return 'отл'
    return 'норм'
