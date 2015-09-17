""" simulated cameralink device test cases
"""

import unittest

from wasatchcameralink import simulation

class TestSimulatedSLED(unittest.TestCase):
    def setUp(self):
        self.dev = simulation.SimulatedCobraSLED()
    
    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 2048)

        self.assertTrue(self.dev.close_pipe())
   
    def test_data_in_range(self):
        self.assertTrue(self.dev.setup_pipe())
        result, data = self.dev.grab_pipe()

        # Verify that the min/max is in range 
        result, data = self.dev.grab_pipe()
        self.assertGreater(data[0], 100)
        self.assertLess(data[0], 4000)
        self.assertGreater(data[1024], 2000)
        self.assertLess(data[1024], 4000)

        # Take 10 reads, make sure at least one is different to show
        # noise application
        found_other = 0
        start_val = data[0]
        for i in range(10):
            result, data = self.dev.grab_pipe()

            if data[0] != start_val:
                found_other += 1

        self.assertGreater(found_other, 0)

class TestSimulatedSpectra(unittest.TestCase):

    def setUp(self):
        self.dev = simulation.SimulatedSpectraDevice()

    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 2048)

        self.assertTrue(self.dev.close_pipe())

    def test_pipe_random_pattern(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 2048)


        # Roll through a bunch of simulated acquisitions, repeat
        for i in range(500):
            result, data = self.dev.grab_pipe()

            # Psuedo-verify the randomness
            self.assertNotEqual(data[0], 0)
            self.assertNotEqual(data[-1], 0)

            self.assertNotEqual(data[0], data[-1])
            self.assertNotEqual(data[100], data[-100])


class TestSimulatedPipe(unittest.TestCase):
    
    def setUp(self):
        self.dev = simulation.SimulatedPipeDevice()

    def test_pipe_cycle(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 1024)

        self.assertTrue(self.dev.close_pipe())

    def test_pipe_test_pattern(self):
        self.assertTrue(self.dev.setup_pipe())

        result, data = self.dev.grab_pipe()
        self.assertTrue(result)
        self.assertEqual(len(data), 1024)
        self.assertEqual(data[0], 0)
        self.assertEqual(data[1023], 1000)

        # Roll through half the test pattern
        for i in range(500):
            result, data = self.dev.grab_pipe()

        self.assertEqual(data[0], 500)
        self.assertEqual(data[1023], 1500)
   
        # roll through the rest of the test pattern, make sure it wraps 
        for i in range(500):
            result, data = self.dev.grab_pipe()
    
        self.assertEqual(data[0], 0)
        self.assertEqual(data[1023], 1000)

if __name__ == "__main__":
    unittest.main()
