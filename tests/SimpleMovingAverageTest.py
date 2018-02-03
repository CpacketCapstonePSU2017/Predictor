from unittest import TestCase
from PModules.SimpleMovingAverage import SimpleMovingAverage as sma

class TesterSimpleMovingAverage(TestCase):

    def test_default_stride(self):
        SMA = sma.SimpleMovingAverage()
        self.assertEquals(SMA.defaultStride,sma.Stride.DAILY)

    def test_default_window_length(self):
        SMA = sma.SimpleMovingAverage()
        self.assertEquals(SMA.windowLength,15)

