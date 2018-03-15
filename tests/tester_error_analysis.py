from PModules.SimpleMovingAverage import SimpleMovingAverage
from PModules.ErrorAnalysis import ErrorAnalysis
from predictor_resources.config import Stride
from unittest import TestCase


class TesterErroranalysis(TestCase):
    def test_metrics_generation_weekly_stride(self):
        model_predictions = SimpleMovingAverage.SimpleMovingAverage(default_stride=Stride.DAILY, window_length=7)
        error_analysis_object = ErrorAnalysis(model_predictions.call_model())
        error_analysis_object.compute_error()
        self.assertEquals(14661386, int(error_analysis_object.meanSquaredError))
        self.assertEquals(2064, int(error_analysis_object.meanAbsoluteError))

    def test_metrics_generation_monthly_stride(self):
        model_predictions = SimpleMovingAverage.SimpleMovingAverage(default_stride=Stride.WEEKLY, window_length=8)
        error_analysis_object = ErrorAnalysis(model_predictions.call_model())
        error_analysis_object.compute_error()
        self.assertEquals(28950922, int(error_analysis_object.meanSquaredError))
        self.assertEquals(2643, int(error_analysis_object.meanAbsoluteError))
