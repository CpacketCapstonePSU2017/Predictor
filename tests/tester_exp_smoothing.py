from unittest import TestCase
from PModules.ExpSmoothing import ExpSmoothing as eps

class TesterExpSmoothing(TestCase):

    def test_call_model(self):
        EPS = eps.ExpSmoothing(rows_to_use=None)
        result = EPS.call_model()
        self.assertIsNotNone(result)
        self.assertEquals(1260, int(result[-1, 1]))
        self.assertEquals(795, int(result[0, 1]))
