from unittest import TestCase
from PModules.SimpleMovingAverage import SimpleMovingAverage as sma

class TesterSimpleMovingAverage(TestCase):

    def test_default_stride(self):
        SMA = sma.SimpleMovingAverage()
        self.assertEquals(sma.Stride.WEEKLY, SMA.defaultStride)

    def test_default_window_length(self):
        SMA = sma.SimpleMovingAverage()
        self.assertEquals(8, SMA.windowLength)

    def test_call_model(self):
        SMA = sma.SimpleMovingAverage()
        result = SMA.call_model()
        self.assertIsNotNone(result)
        self.assertEquals(2024.5, result[-1, 1])
        self.assertEquals(1905.0, result[0, 1])

