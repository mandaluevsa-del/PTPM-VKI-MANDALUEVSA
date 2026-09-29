"""Юнит-тесты для delivery_service.py (расчёт стоимости доставки)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.delivery_service import calculate_delivery_cost

ERROR_TUPLE = (-1, "0000-00-00")
SHIP_DATE = "2026-09-03"


class TestDeliveryValidation(unittest.TestCase):
    """Проверка обработки неверных входных данных."""

    def test_out_of_range_parameters_return_error(self):
        for weight, distance in ((0.05, 100), (55.0, 100), (1, 0), (1, 6000)):
            with self.subTest(weight=weight, distance=distance):
                self.assertEqual(calculate_delivery_cost(weight, distance, "обычный"),
                                 ERROR_TUPLE)

    def test_unknown_package_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 100, "стекло"), ERROR_TUPLE)


class TestDeliveryCost(unittest.TestCase):
    """Проверка тарифных расчётов."""

    def test_lower_bounds_are_accepted(self):
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        self.assertEqual(cost, 205)
        self.assertEqual(date, "2026-09-04")

    def test_base_cost_includes_distance_rate(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_weight_tariff_multipliers_apply(self):
        for weight, expected in ((6, 840), (20.0, 1050)):
            with self.subTest(weight=weight):
                cost, _ = calculate_delivery_cost(weight, 100, "обычный")
                self.assertEqual(cost, expected)

    def test_package_type_surcharges_apply(self):
        for package_type, expected in (("хрупкий", 1000), ("опасный", 1700)):
            with self.subTest(package_type=package_type):
                cost, _ = calculate_delivery_cost(1, 100, package_type)
                self.assertEqual(cost, expected)

    def test_delivery_date_depends_on_distance(self):
        _, date = calculate_delivery_cost(1, 2000, "обычный")
        self.assertEqual(date, "2026-09-07")

    def test_return_shape_is_cost_and_date(self):
        cost, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertIsInstance(cost, int)
        self.assertIsInstance(date, str)

    def test_cost_with_half_ruble_is_rounded_to_nearest_ruble(self):
        cost, _ = calculate_delivery_cost(20.0, 1, "обычный")
        self.assertEqual(cost, 308)


class TestExpressDelivery(unittest.TestCase):
    """Проверка экспресс-доставки (доплата и сроки)."""

    def test_normal_express_ratio_is_premium(self):
        normal_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_delivery_is_never_delivered_on_shipment_day(self):
        dates = [
            calculate_delivery_cost(1, distance, "обычный", is_express=True)[1]
            for distance in (1, 250, 499, 500, 999, 1000)
        ]
        self.assertGreater(min(dates), SHIP_DATE)


if __name__ == "__main__":
    unittest.main()
