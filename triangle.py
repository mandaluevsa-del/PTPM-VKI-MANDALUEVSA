"""Метод вычисления вида треугольника и координат его вершин.

Треугольник задаётся тремя сторонами A, B, C, каждая из которых
передаётся строкой, представляющей вещественное положительное число
точности float. Метод возвращает вид треугольника и координаты трёх
вершин (int, int), пригодные для отрисовки в поле 100x100 px.
"""

import math

FIELD_SIZE = 100
MARGIN = 5
EPSILON = 1e-9

EQUILATERAL = "равносторонний"
ISOSCELES = "равнобедренный"
SCALENE = "разносторонний"
NOT_TRIANGLE = "не треугольник"

NON_NUMERIC_COORDS = [(-2, -2), (-2, -2), (-2, -2)]
INVALID_NUMERIC_COORDS = [(-1, -1), (-1, -1), (-1, -1)]


def _parse_float(text):
    """Парсит строку как float. Возвращает None при нечисловых данных."""
    try:
        return float(text.strip())
    except (ValueError, TypeError):
        return None


def compute_triangle(side_a, side_b, side_c):
    """Вычисляет вид треугольника и координаты вершин для поля 100x100 px.

    Аргументы:
        side_a -- длина стороны A (строка)
        side_b -- длина стороны B (строка)
        side_c -- длина стороны C (строка)

    Возвращает кортеж (тип, координаты):
        тип -- "равносторонний", "равнобедренный", "разносторонний",
               "не треугольник" или пустая строка для нечисловых данных.
        координаты -- список из трёх кортежей (int, int). При ошибочных
               числовых данных вершины равны (-1, -1), при нечисловых
               данных -- (-2, -2).
    """
    a = _parse_float(side_a)
    b = _parse_float(side_b)
    c = _parse_float(side_c)

    if a is None or b is None or c is None:
        return "", NON_NUMERIC_COORDS

    if not (math.isfinite(a) and a > 0 and math.isfinite(b) and b > 0
            and math.isfinite(c) and c > 0):
        return NOT_TRIANGLE, INVALID_NUMERIC_COORDS

    if (a + b <= c + EPSILON) or (a + c <= b + EPSILON) or (b + c <= a + EPSILON):
        return NOT_TRIANGLE, INVALID_NUMERIC_COORDS

    if abs(a - b) < EPSILON and abs(b - c) < EPSILON:
        kind = EQUILATERAL
    elif abs(a - b) < EPSILON or abs(b - c) < EPSILON or abs(a - c) < EPSILON:
        kind = ISOSCELES
    else:
        kind = SCALENE

    ax, ay = 0.0, 0.0
    bx, by = c, 0.0
    cx = (a * a + c * c - b * b) / (2.0 * c)
    cy = math.sqrt(max(a * a - cx * cx, 0.0))

    coords = [(ax, ay), (bx, by), (cx, cy)]

    min_x = min(p[0] for p in coords)
    min_y = min(p[1] for p in coords)
    max_x = max(p[0] for p in coords)
    max_y = max(p[1] for p in coords)

    extent = max(max_x - min_x, max_y - min_y)
    usable = FIELD_SIZE - 2 * MARGIN

    if extent <= EPSILON:
        scale = 1.0
    else:
        scale = usable / extent

    result = []
    for px, py in coords:
        nx = MARGIN + (px - min_x) * scale
        ny = FIELD_SIZE - MARGIN - (py - min_y) * scale
        result.append((int(round(nx)), int(round(ny))))

    return kind, result