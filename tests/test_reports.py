import pytest
import sys
import os
from unittest.mock import patch
sys.path.insert(0, os.path.abspath('.'))
from script.reports import (
    PerformanceReport, ReportFactory, get_report_generator
)
#from script.reports import SkillsReport

def test_performance_report_generate():
    """Тест генерации отчета по эффективности."""
    data = [
        {'name': 'Alex', 'position': 'Backend Developer', 'performance': 4.0},
        {'name': 'Maria', 'position': 'Frontend Developer', 'performance': 5.0},
        {'name': 'John', 'position': 'Backend Developer', 'performance': 3.0},
        {'name': 'Anna', 'position': 'Frontend Developer', 'performance': 4.0},
    ]

    report = PerformanceReport()
    result = report.generate(data)

    # Проверяем, что есть две должности
    assert len(result) == 2

    # Проверяем, что отсортировано по убыванию эффективности
    positions = [pos for pos, _ in result]
    assert positions[0] == 'Frontend Developer'  # Средняя: (5.0 + 4.0) / 2 = 4.5
    assert positions[1] == 'Backend Developer'  # Средняя: (4.0 + 3.0) / 2 = 3.5

    # Проверяем значения
    for position, avg in result:
        if position == 'Frontend Developer':
            assert avg == pytest.approx(4.5)
        elif position == 'Backend Developer':
            assert avg == pytest.approx(3.5)


def test_performance_report_generate_empty():
    """Тест генерации отчета для пустых данных."""
    data = []
    report = PerformanceReport()
    result = report.generate(data)
    assert result == []


def test_performance_report_display(capsys):
    """Тест отображения отчета."""
    report_data = [
        ('Frontend Developer', 4.5),
        ('Backend Developer', 3.5),
    ]

    report = PerformanceReport()

    with patch.dict('sys.modules', {'tabulate': None}):
        report.display(report_data)
        captured = capsys.readouterr()
        assert "Должность" in captured.out
        assert "Frontend Developer" in captured.out
        assert "4.5" in captured.out


def test_report_factory():
    """Тест фабрики отчетов."""
    report = ReportFactory.create_report('performance')
    assert isinstance(report, PerformanceReport)


def test_report_factory_invalid_report():
    """Тест фабрики отчетов с неверным именем."""
    with pytest.raises(ValueError, match="Неизвестный отчет"):
        ReportFactory.create_report('invalid_report')


def test_get_report_generator():
    """Тест функции get_report_generator."""
    report = get_report_generator('performance')
    assert isinstance(report, PerformanceReport)


def test_register_new_report():
    """Тест регистрации нового отчета."""
    from script.reports import Report

    class NewReport(Report):
        def generate(self, data):
            return []

        def display(self, report_data):
            print("New report")

    # Регистрируем новый отчет
    ReportFactory.register_report('new', NewReport)

    # Проверяем, что можем создать новый отчет
    report = ReportFactory.create_report('new')
    assert isinstance(report, NewReport)

    # Проверяем, что старый отчет все еще доступен
    report2 = ReportFactory.create_report('performance')
    assert isinstance(report2, PerformanceReport)

    # Тест на неверный класс
    class NotAReport:
        pass

    with pytest.raises(TypeError):
        ReportFactory.register_report('invalid', NotAReport)


# РАСКОММЕНТИРОВАТЬ ДЛЯ ТЕСТИРОВАНИЯ РЕГИСТРАЦИИ НОВОГО ОТЧЕТА
"""
def test_skills_report():
    # Тест нового отчёта по популярности технологий
    data = [
        {'name': 'Alex', 'position': 'Backend Developer', 'skills': 'Python, Django'},
        {'name': 'Maria', 'position': 'Frontend Developer', 'skills': 'JavaScript, React'},
        {'name': 'John', 'position': 'Backend Developer', 'skills': 'Python, PostgreSQL'},
        {'name': 'Anna', 'position': 'Frontend Developer', 'skills': 'JavaScript, Vue.js'},
        {'name': 'Mike', 'position': 'DevOps Engineer', 'skills': 'Docker, Python'},
    ]

    report = SkillsReport()
    result = report.generate(data)

    # Преобразуем результат в словарь для удобных проверок
    result_dict = dict(result)

    # Ожидаем 7 уникальных технологий
    assert len(result) == 7

    # Проверяем количество для каждой технологии
    assert result_dict.get('Python') == 3    # Встречается 3 раза
    assert result_dict.get('JavaScript') == 2 # Встречается 2 раза
    assert result_dict.get('Django') == 1    # Встречается 1 раз
    assert result_dict.get('React') == 1     # Встречается 1 раз
    assert result_dict.get('PostgreSQL') == 1 # Встречается 1 раз
    assert result_dict.get('Vue.js') == 1    # Встречается 1 раз
    assert result_dict.get('Docker') == 1    # Встречается 1 раз

    # Проверяем сортировку по убыванию (первые две позиции)
    assert result[0] == ('Python', 3)       # Самая частая технология
    assert result[1] == ('JavaScript', 2)   # Вторая по частоте


def test_skills_report_display(capsys):
    # Тест отображения нового отчёта

    report_data = [
        ('Python', 5),
        ('JavaScript', 3),
        ('Docker', 2),
    ]

    report = SkillsReport()

    with patch.dict('sys.modules', {'tabulate': None}):
        report.display(report_data)
        captured = capsys.readouterr()

        assert "Технология" in captured.out
        assert "Количество" in captured.out
        assert "Python" in captured.out
        assert "5" in captured.out


def test_skills_report_registration():
    # Тест регистрации нового отчёта в фабрике
    # Регистрируем новый отчет
    ReportFactory.register_report('skills', SkillsReport)

    # Проверяем, что можем создать новый отчет
    report = ReportFactory.create_report('skills')
    assert isinstance(report, SkillsReport)

    # Проверяем, что старый отчет все еще доступен
    report2 = ReportFactory.create_report('performance')
    assert isinstance(report2, PerformanceReport)
"""
