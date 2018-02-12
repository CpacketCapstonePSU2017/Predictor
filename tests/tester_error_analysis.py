from PModules.SimpleMovingAverage import SimpleMovingAverage
from PModules.ErrorAnalysis import ErrorAnalysis
from unittest import TestCase

class TesterErroranalysis(TestCase):
    def test_metrics_generation_weekly_stride(self):
        model_predictions = SimpleMovingAverage.SimpleMovingAverage(default_stride=SimpleMovingAverage.Stride.DAILY, window_length=7)
        error_analysis_object = ErrorAnalysis(model_predictions.call_model())
        error_analysis_object.compute_error()
        self.assertEquals(272228.33564768662, error_analysis_object.meanSquaredError)
        self.assertEquals(253.44560119895044, error_analysis_object.meanAbsoluteError)

    def test_metrics_generation_monthly_stride(self):
        model_predictions = SimpleMovingAverage.SimpleMovingAverage(default_stride=SimpleMovingAverage.Stride.WEEKLY, window_length=8)
        error_analysis_object = ErrorAnalysis(model_predictions.call_model())
        error_analysis_object.compute_error()
        self.assertEquals(437554.18669923965, error_analysis_object.meanSquaredError)
        self.assertEquals(333.85647898015367, error_analysis_object.meanAbsoluteError)
