import unittest
from unittest import mock

from prediction_evaluation import predict_message_mood, SomeModel


class TestPredictMessageMood(unittest.TestCase):
    def setUp(self):
        self.message = 'some mess'
        self.model = SomeModel()

    def test_call_predict_with_correct_arg(self):
        with mock.patch('prediction_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.return_value = 0.3
            self.assertEqual(predict_message_mood(self.message, self.model, 0.4),
                             'неуд')
            self.assertEqual([mock.call(self.message)], mock_predict.mock_calls)

    @mock.patch('prediction_evaluation.SomeModel.predict', return_value=0.498)
    def test_invalid_threshold_pair(self, predict_mock):
        thresholds = [(0.5, 0.3), (0.4, 0.4)]
        with self.subTest():
            for bt, gt in thresholds:
                with self.assertRaises(ValueError) as err:
                    predict_message_mood(self.message, self.model,
                                         bt, gt)
                self.assertEqual(str(err.exception),
                                 'bad_threshold must be lower that good_threshold')

    def test_boundary_values(self):
        bad_thresholds, good_thresholds = 0.32, 0.87
        with mock.patch('prediction_evaluation.SomeModel.predict') as mock_predict:
            mock_predict.return_value = bad_thresholds
            self.assertEqual(predict_message_mood(self.message,
                                                  self.model,
                                                  bad_thresholds=bad_thresholds),
                             'норм')
            mock_calls = [mock.call(self.message)]
            self.assertEqual(mock_calls, mock_predict.mock_calls)

            mock_predict.return_value = good_thresholds
            self.assertEqual(predict_message_mood(self.message,
                                                  self.model,
                                                  good_thresholds=good_thresholds),
                             'норм')
            mock_calls.append(mock.call(self.message))
            self.assertEqual(mock_calls, mock_predict.mock_calls)

    @mock.patch('prediction_evaluation.SomeModel.predict')
    def test_some_values(self, mock_predict):
        bad_thresholds, good_thresholds = 0.32, 0.87
        value_result = [
            (0, 'неуд'), (0.2, 'неуд'), (0.32, 'норм'),
            (0.4, 'норм'), (0.6, 'норм'), (0.7, 'норм'),
            (0.87, 'норм'), (0.9, 'отл'), (0.95, 'отл')
        ]
        mock_calls = []
        with self.subTest():
            for value, result in value_result:
                mock_predict.return_value = value
                mock_calls.append(mock.call(self.message))
                self.assertEqual(predict_message_mood(self.message,
                                                      self.model,
                                                      bad_thresholds=bad_thresholds,
                                                      good_thresholds=good_thresholds),
                                 result)
                self.assertEqual(mock_calls, mock_predict.mock_calls)

    def test_invalid_model(self):
        model = list
        with self.assertRaises(TypeError) as err:
            predict_message_mood(self.message,
                                 model)
        self.assertEqual(str(err.exception), f'model must be instance of SomeModel, not {list}')