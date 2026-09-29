"""Юнит-тесты для delivery_service.py (расчёт стоимости доставки)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.delivery_service import calculate_delivery_cost

ERROR_TUPLE = (-1, "0000-00-00")
SHIP_DATE = "2026-09-03"


class TestDeliveryValidation(unittest.TestCase):
    """Проверка обработки некорректных входных данных."""

    def test_unknown_package_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 100, "стекло"), ERROR_TUPLE)

    def test_empty_package_type_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 100, ""), ERROR_TUPLE)

    def test_weight_below_minimum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(0.05, 100, "обычный"), ERROR_TUPLE)

    def test_weight_above_maximum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(55.0, 100, "обычный"), ERROR_TUPLE)

    def test_negative_weight_returns_error(self):
        self.assertEqual(calculate_delivery_cost(-1.0, 100, "обычный"), ERROR_TUPLE)

    def test_distance_below_minimum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 0, "обычный"), ERROR_TUPLE)

    def test_distance_above_maximum_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, 6000, "обычный"), ERROR_TUPLE)

    def test_negative_distance_returns_error(self):
        self.assertEqual(calculate_delivery_cost(1, -100, "обычный"), ERROR_TUPLE)


class TestDeliveryCost(unittest.TestCase):
    """Проверка тарифных расчётов."""

    def test_lower_bounds_are_accepted(self):
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        self.assertEqual(cost, 205)
        self.assertEqual(date, "2026-09-04")

    def test_upper_bounds_are_accepted(self):
        cost, date = calculate_delivery_cost(50.0, 5000, "обычный")
        self.assertEqual(cost, 37800)
        self.assertEqual(date, "2026-09-13")

    def test_base_cost_is_base_plus_distance_rate(self):
        cost, _ = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_medium_weight_applies_1_2_multiplier(self):
        cost, _ = calculate_delivery_cost(6, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_on_lower_boundary_has_no_multiplier(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_large_weight_applies_1_5_multiplier(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_heavy_weight_uses_single_multiplier_only(self):
        cost, _ = calculate_delivery_cost(30.0, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_fragile_adds_300_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_adds_1000_surcharge(self):
        cost, _ = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)

    def test_weight_and_fragile_surcharges_combine(self):
        cost, _ = calculate_delivery_cost(6, 100, "хрупкий")
        self.assertEqual(cost, 1140)

    def test_all_supported_package_types_are_accepted(self):
        for package_type in ("обычный", "хрупкий", "опасный"):
            with self.subTest(package_type=package_type):
                cost, date = calculate_delivery_cost(1, 100, package_type)
                self.assertGreater(cost, 0)
                self.assertNotEqual(date, "0000-00-00")

    def test_weight_exactly_twenty_uses_heavy_tariff(self):
        cost, _ = calculate_delivery_cost(20.0, 2, "обычный")
        self.assertEqual(cost, 315)

    def test_cost_with_half_ruble_is_rounded_to_nearest_ruble(self):
        cost, _ = calculate_delivery_cost(20.0, 1, "обычный")
        self.assertEqual(cost, 308)

    def test_return_shape_is_cost_and_date(self):
        result = calculate_delivery_cost(1, 100, "обычный")
        self.assertIsInstance(result, tuple)
        cost, date = result
        self.assertIsInstance(cost, int)
        self.assertIsInstance(date, str)


class TestExpressDelivery(unittest.TestCase):
    """Проверка экспресс-доставки (доплата и сроки)."""

    def test_normal_express_ratio_is_premium(self):
        normal_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_delivers_faster_than_normal(self):
        _, normal_date = calculate_delivery_cost(1, 2000, "обычный", is_express=False)
        _, express_date = calculate_delivery_cost(1, 2000, "обычный", is_express=True)
        self.assertLess(express_date, normal_date)

    def test_express_shipment_takes_at_least_one_day(self):
        _, date = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        self.assertGreater(date, SHIP_DATE)

    def test_express_delivery_is_never_delivered_on_shipment_day(self):
        dates = [
            calculate_delivery_cost(1, distance, "обычный", is_express=True)[1]
            for distance in (1, 250, 499, 500, 999, 1000)
        ]
        self.assertGreater(min(dates), SHIP_DATE)

    def test_express_delivery_halves_transport_time(self):
        _, normal_date = calculate_delivery_cost(1, 2000, "обычный", is_express=False)
        _, express_date = calculate_delivery_cost(1, 2000, "обычный", is_express=True)
        self.assertEqual(normal_date, "2026-09-07")
        self.assertEqual(express_date, "2026-09-05")


if __name__ == "__main__":
    unittest.main()