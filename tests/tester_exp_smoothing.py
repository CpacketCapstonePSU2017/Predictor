from unittest import TestCase
from PModules.ExpSmoothing import ExpSmoothing as eps

class TesterExpSmoothing(TestCase):

    def test_call_model(self):
        EPS = eps.ExpSmoothing()
        result = EPS.call_model()
        self.assertIsNotNone(result)
        self.assertEquals(6624.2419795543365, result[-1, 1])
        self.assertEquals(6162, result[0, 1])
