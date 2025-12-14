import sys
import os
sys.path.insert(0, os.path.abspath('.'))
import tempfile
from pathlib import Path
from script.cli import main
import pytest


def test_cli_with_valid_args(capsys, monkeypatch):
    """Тест CLI с валидными аргументами."""
    # Создаем временный CSV файл
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript",Web Team,4"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False,
                                     encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        test_args = ['script.py', '--files', file_path, '--report', 'performance']
        monkeypatch.setattr(sys, 'argv', test_args)

        main()

        captured = capsys.readouterr()
        assert "Должность" in captured.out or "Backend Developer" in captured.out
        assert "Frontend Developer" in captured.out
    finally:
        Path(file_path).unlink()


def test_cli_with_nonexistent_file(capsys, monkeypatch):
    """Тест CLI с несуществующим файлом."""
    test_args = ['script.py', '--files', 'nonexistent.csv', '--report', 'performance']
    monkeypatch.setattr(sys, 'argv', test_args)

    # ОЖИДАЕМ, что будет SystemExit (скрипт завершится с ошибкой)
    with pytest.raises(SystemExit) as e:
        main()

    # Проверяем, что код ошибки = 1
    assert e.value.code == 1

    # Проверяем вывод ошибки
    captured = capsys.readouterr()
    assert "не найдены" in captured.err


def test_cli_with_invalid_report(capsys, monkeypatch):
    """Тест CLI с неверным отчетом."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("name,position,completed_tasks,performance,skills,team,experience_years\n")
        file_path = f.name

    try:
        test_args = ['script.py', '--files', file_path, '--report', 'invalid_report']
        monkeypatch.setattr(sys, 'argv', test_args)

        # ОЖИДАЕМ SystemExit
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Неизвестный отчет" in captured.err
    finally:
        Path(file_path).unlink()


def test_cli_with_multiple_files(capsys, monkeypatch):
    """Тест CLI с несколькими файлами."""
    csv_content1 = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django",API Team,5"""

    csv_content2 = """name,position,completed_tasks,performance,skills,team,experience_years
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript",Web Team,4"""

    file1 = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    file1.write(csv_content1)
    file1.close()

    file2 = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    file2.write(csv_content2)
    file2.close()

    try:
        test_args = ['script.py', '--files', file1.name, file2.name,
                     '--report', 'performance']
        monkeypatch.setattr(sys, 'argv', test_args)

        main()

        captured = capsys.readouterr()
        assert "Backend Developer" in captured.out
        assert "Frontend Developer" in captured.out
    finally:
        Path(file1.name).unlink()
        Path(file2.name).unlink()


def test_cli_with_invalid_csv_data(capsys, monkeypatch):
    """Тест CLI с неверными данными в CSV."""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,not_a_number,4.8,Python,API Team,5"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False,
                                     encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        test_args = ['script.py', '--files', file_path, '--report', 'performance']
        monkeypatch.setattr(sys, 'argv', test_args)

        # Ожидаем SystemExit с кодом ошибки
        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Ошибка в данных" in captured.err or "Неверный формат" in captured.err
    finally:
        Path(file_path).unlink()


def test_cli_with_report_generation_error(capsys, monkeypatch):
    """Тест CLI с ошибкой при генерации отчета."""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,Python,API Team,5"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False,
                                     encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        # Импортируем модуль cli, чтобы подменить функцию в нём
        from script import cli

        def mock_get_report_generator(report_name):
            raise Exception("Искусственная ошибка генерации")

        monkeypatch.setattr(cli, 'get_report_generator', mock_get_report_generator)

        test_args = ['script.py', '--files', file_path, '--report', 'performance']
        monkeypatch.setattr(sys, 'argv', test_args)

        with pytest.raises(SystemExit) as e:
            main()

        assert e.value.code == 1
        captured = capsys.readouterr()
        assert "Ошибка при генерации отчета" in captured.err
    finally:
        Path(file_path).unlink()