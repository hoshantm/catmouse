import unittest
from catmouse import CAT_TO_MOUSE_SPEED_RATIO
from catmouse import diffTimeCatMouse
from catmouse import distanceToEdge
from catmouse import distanceViaEdge
from catmouse import maxDiffTimeCatMouse
import math

class Test_CatMouse(unittest.TestCase):
    def testDiffCatMouse(self):
        for alpha in (i * math.pi / 18 for i in range(37)):
            for beta in (j * math.pi / 18 for j in range(37)):
                for distance in (i * 10.0 for i in range(11)):
                    if beta <= math.pi:
                        diffTime1 = beta - CAT_TO_MOUSE_SPEED_RATIO * distanceToEdge(distance, alpha, beta)
                    else:
                        diffTime1 = 2 * math.pi - beta - CAT_TO_MOUSE_SPEED_RATIO * distanceToEdge(distance, alpha, beta)
                    
                    diffTime2 = diffTimeCatMouse(distance, alpha, beta)
                    self.assertAlmostEqual(diffTime1, diffTime2, 6)

    def testDistanceViaEdge(self):
        self.assertEqual(distanceViaEdge(math.pi), math.pi)
        self.assertEqual(0, 0)
        self.assertEqual(distanceViaEdge(math.pi / 2.0), math.pi / 2.0)
        self.assertEqual(distanceViaEdge(math.pi * 1.5), math.pi / 2.0)

    def testmaxDiffTimeCatMouse(self):
        self.assertEqual(maxDiffTimeCatMouse(0.5, math.pi)[0], math.pi)
        self.assertGreater(maxDiffTimeCatMouse(0.5, math.pi / 2)[0], math.pi / 2)
        self.assertLess(maxDiffTimeCatMouse(0.5, math.pi * 1.5)[0], math.pi * 1.5)

if __name__ == "__main__":
    unittest.main()


