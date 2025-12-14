import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import pytest
from script.processors import group_by_position, calculate_average_performance


def test_group_by_position():
    """Тест группировки по должности."""
    data = [
        {'name': 'Alex', 'position': 'Backend Developer', 'performance': 4.8},
        {'name': 'Maria', 'position': 'Frontend Developer', 'performance': 4.7},
        {'name': 'John', 'position': 'Backend Developer', 'performance': 4.9},
    ]

    grouped = group_by_position(data)

    assert 'Backend Developer' in grouped
    assert 'Frontend Developer' in grouped
    assert len(grouped['Backend Developer']) == 2
    assert len(grouped['Frontend Developer']) == 1


def test_calculate_average_performance():
    """Тест вычисления средней эффективности."""
    developers = [
        {'name': 'Alex', 'performance': 4.0},
        {'name': 'Maria', 'performance': 5.0},
        {'name': 'John', 'performance': 3.0},
    ]

    avg = calculate_average_performance(developers)
    assert avg == pytest.approx(4.0)


def test_calculate_average_performance_empty():
    """Тест вычисления средней эффективности для пустого списка."""
    developers = []
    avg = calculate_average_performance(developers)
    assert avg == 0.0


def test_calculate_average_performance_single():
    """Тест вычисления средней эффективности для одного разработчика."""
    developers = [{'name': 'Alex', 'performance': 4.5}]
    avg = calculate_average_performance(developers)
    assert avg == 4.5