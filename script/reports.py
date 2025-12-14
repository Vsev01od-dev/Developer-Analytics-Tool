from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from .processors import group_by_position, calculate_average_performance


# Абстрактный базовый класс для отчетов
class Report(ABC):

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> List[Tuple[str, Any]]:
        """Генерирует данные отчета."""
        pass

    @abstractmethod
    def display(self, report_data: List[Tuple[str, Any]]) -> None:
        """Отображает отчет в консоли."""
        pass


class PerformanceReport(Report):
    def generate(self, data: List[Dict[str, Any]]) -> List[Tuple[str, float]]:
        grouped_data = group_by_position(data)

        report = []
        for position, developers in grouped_data.items():
            avg_performance = calculate_average_performance(developers)
            report.append((position, avg_performance))

        # Сортировка по эффективности (по убыванию)
        report.sort(key=lambda x: x[1], reverse=True)

        return report

    def display(self, report_data: List[Tuple[str, float]]) -> None:
        try:
            from tabulate import tabulate
            headers = ["Должность", "Средняя эффективность"]
            table_data = [(position, f"{performance:.2f}")
                          for position, performance in report_data]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except ImportError:
            print("Должность\t\t\tСредняя эффективность")
            print("-" * 50)
            for position, performance in report_data:
                print(f"{position:30} {performance:10.2f}")


class ReportFactory:
    _reports = {
        'performance': PerformanceReport,
    }

    @classmethod
    def register_report(cls, name: str, report_class: type) -> None:
        if not issubclass(report_class, Report):
            raise TypeError("Класс отчета должен наследоваться от Report")
        cls._reports[name] = report_class

    @classmethod
    def create_report(cls, name: str) -> Report:
        if name not in cls._reports:
            raise ValueError(
                f"Неизвестный отчет: {name}. "
                f"Доступные отчеты: {', '.join(cls._reports.keys())}"
            )
        return cls._reports[name]()


def get_report_generator(report_name: str) -> Report:
    return ReportFactory.create_report(report_name)

# РАСКОММЕНТИРОВАТЬ ДЛЯ АКТИВАЦИИ НОВОГО ОТЧЕТА
"""
class SkillsReport(Report):
    # Отчёт по популярности технологий среди сотрудников.

    def generate(self, data: List[Dict[str, Any]]) -> List[Tuple[str, int]]:
        tech_counter = {}

        for developer in data:
            # Получаем строку с навыками, чистим её и разбиваем по запятым
            skills_str = developer.get('skills', '')
            # Убираем лишние пробелы, разделяем, очищаем каждый элемент
            tech_list = [tech.strip() for tech in skills_str.split(',') if tech.strip()]

            for technology in tech_list:
                tech_counter[technology] = tech_counter.get(technology, 0) + 1

        # Преобразуем словарь в список кортежей и сортируем по убыванию популярности
        report = list(tech_counter.items())
        report.sort(key=lambda x: x[1], reverse=True)

        return report

    def display(self, report_data: List[Tuple[str, int]]) -> None:
        try:
            from tabulate import tabulate
            headers = ["Технология", "Количество сотрудников"]
            table_data = [(technology, f"{count}") for technology, count in report_data]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except ImportError:
            print("Технология\t\t\tКоличество сотрудников")
            print("-" * 60)
            for technology, count in report_data:
                print(f"{technology:35} {count:10}")


ReportFactory.register_report('skills', SkillsReport)
"""