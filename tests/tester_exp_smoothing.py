from unittest import TestCase
from PModules.ExpSmoothing import ExpSmoothing as eps

class TesterExpSmoothing(TestCase):

    def test_call_model(self):
        EPS = eps.ExpSmoothing()
        result = EPS.call_model()
        self.assertIsNotNone(result)
        self.assertEquals(1463.7009935823864, result[-1, 1])
        self.assertEquals(754.2621777, result[0, 1])
