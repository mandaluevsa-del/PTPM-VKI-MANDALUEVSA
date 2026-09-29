"""Юнит-тесты для my_project.py (вычисление треугольника из ЛР1)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.my_project import (
    EQUILATERAL,
    ISOSCELES,
    INVALID_NUMERIC_COORDS,
    NON_NUMERIC_COORDS,
    NOT_TRIANGLE,
    SCALENE,
    compute_triangle,
)


class TestTriangleClassification(unittest.TestCase):
    """Проверка определения вида треугольника."""

    def test_equilateral_returns_ravnostoronniy(self):
        kind, _ = compute_triangle("7", "7", "7")
        self.assertEqual(kind, EQUILATERAL)

    def test_isosceles_returns_ravnobedrenniy(self):
        kind, _ = compute_triangle("5", "5", "8")
        self.assertEqual(kind, ISOSCELES)

    def test_isosceles_when_first_and_last_sides_equal(self):
        kind, _ = compute_triangle("8", "5", "5")
        self.assertEqual(kind, ISOSCELES)

    def test_scalene_returns_raznostoronniy(self):
        kind, _ = compute_triangle("3", "4", "5")
        self.assertEqual(kind, SCALENE)

    def test_nearly_equal_sides_are_equilateral_with_tolerance(self):
        kind, _ = compute_triangle("5", "5", "5.0000000004")
        self.assertEqual(kind, EQUILATERAL)


class TestTriangleValidation(unittest.TestCase):
    """Проверка обработки некорректных данных."""

    def test_non_numeric_sides_return_empty_type(self):
        kind, _ = compute_triangle("abc", "def", "ghi")
        self.assertEqual(kind, "")

    def test_partly_non_numeric_returns_empty_type(self):
        kind, _ = compute_triangle("5", "abc", "8")
        self.assertEqual(kind, "")

    def test_empty_blank_and_none_side_is_non_numeric(self):
        for value in ("", "   ", None):
            with self.subTest(side=value):
                kind, coords = compute_triangle(value, "5", "5")
                self.assertEqual(kind, "")
                self.assertEqual(coords, NON_NUMERIC_COORDS)

    def test_zero_and_negative_sides_are_not_a_triangle(self):
        for sides in (("0", "5", "5"), ("-5", "6", "7"), ("-1", "-1", "-1")):
            with self.subTest(sides=sides):
                kind, coords = compute_triangle(*sides)
                self.assertEqual(kind, NOT_TRIANGLE)
                self.assertEqual(coords, INVALID_NUMERIC_COORDS)

    def test_degenerate_sides_on_straight_line(self):
        kind, coords = compute_triangle("5", "5", "10")
        self.assertEqual(kind, NOT_TRIANGLE)
        self.assertEqual(coords, INVALID_NUMERIC_COORDS)

    def test_infinite_and_nan_sides_are_rejected(self):
        for value in ("inf", "nan"):
            with self.subTest(side=value):
                kind, coords = compute_triangle(value, "5", "6")
                self.assertEqual(kind, NOT_TRIANGLE)
                self.assertEqual(coords, INVALID_NUMERIC_COORDS)

    def test_near_degenerate_side_within_epsilon_is_valid(self):
        kind, _ = compute_triangle("5", "5", "9.9999")
        self.assertEqual(kind, ISOSCELES)


class TestTriangleCoordinates(unittest.TestCase):
    """Проверка расчёта координат вершин."""

    def test_non_numeric_sides_return_minus_two_coords(self):
        _, coords = compute_triangle("abc", "def", "ghi")
        self.assertEqual(coords, NON_NUMERIC_COORDS)

    def test_invalid_numeric_sides_return_minus_one_coords(self):
        _, coords = compute_triangle("0", "0", "0")
        self.assertEqual(coords, INVALID_NUMERIC_COORDS)

    def test_coordinates_contain_exactly_three_vertices(self):
        _, coords = compute_triangle("3", "4", "5")
        self.assertEqual(len(coords), 3)

    def test_coordinates_are_integer_pairs(self):
        _, coords = compute_triangle("6", "7", "8")
        for x, y in coords:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)

    def test_coordinates_within_margin_band(self):
        _, coords = compute_triangle("6", "7", "8")
        for x, y in coords:
            self.assertGreaterEqual(x, 5)
            self.assertGreaterEqual(y, 5)
            self.assertLessEqual(x, 95)
            self.assertLessEqual(y, 95)

    def test_whitespace_padded_sides_parsed_correctly(self):
        kind, coords = compute_triangle("  3 ", " 4 ", "  5  ")
        self.assertEqual(kind, SCALENE)
        self.assertEqual(len(coords), 3)


class TestTriangleOverflowRobustness(unittest.TestCase):
    """Проверка устойчивости при экстремально больших сторонах."""

    def test_huge_sides_do_not_raise(self):
        compute_triangle("1e308", "1e308", "1e308")

    def test_huge_sides_with_overflow_return_invalid_coords(self):
        _, coords = compute_triangle("1e308", "1e308", "1e308")
        self.assertEqual(coords, INVALID_NUMERIC_COORDS)

    def test_huge_sides_do_not_break_kind_detection(self):
        kind, _ = compute_triangle("1e308", "1e308", "1e308")
        self.assertEqual(kind, NOT_TRIANGLE)


if __name__ == "__main__":
    unittest.main()
