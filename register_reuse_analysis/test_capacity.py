import unittest
from capacity_report import minimum_safe, pressure_onset
from run import parse_reg_points
from sweep import capacity_points


class CapacityAnalysisTest(unittest.TestCase):
    def test_safe_threshold_requires_all_larger_points(self):
        points = [(96, {'ipc_loss': .1}), (128, {'ipc_loss': .005}),
                  (160, {'ipc_loss': .03}), (192, {'ipc_loss': .0})]
        self.assertEqual(minimum_safe(points, .01), 192)
        self.assertEqual(minimum_safe(points, .05), 128)

    def test_pressure_bracket(self):
        points = [(96, {'pressure': .1}), (128, {'pressure': .02}),
                  (160, {'pressure': .002}), (192, {'pressure': 0})]
        self.assertEqual(pressure_onset(points, 'pressure'), (128, 160))

    def test_explicit_points(self):
        self.assertEqual(parse_reg_points('base:224:256,i128:128:256'),
                         [('base', 224, 256), ('i128', 128, 256)])
        with self.assertRaises(ValueError):
            parse_reg_points('a:224:256,a:128:128')
        with self.assertRaises(ValueError):
            parse_reg_points('../a:224:256')
        with self.assertRaises(ValueError):
            parse_reg_points('bad:32:64')

    def test_axis_holds_other_class_constant(self):
        text = capacity_points('float', [128, 192, 256], 512)
        self.assertIn('fp128:224:128', text)
        self.assertNotIn('fp256', text)
        self.assertEqual(text.count('baseline'), 1)


if __name__ == '__main__':
    unittest.main()
