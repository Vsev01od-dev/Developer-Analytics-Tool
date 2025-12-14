import pytest
import tempfile
import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from pathlib import Path
from script.reader import read_csv_files
from script.reader import detect_delimiter

def create_test_csv(content: str) -> str:
    """Создает временный CSV файл с заданным содержимым."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                     delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name


def test_read_csv_files_single():
    """Тест чтения одного CSV файла."""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript",Web Team,4"""

    file_path = create_test_csv(csv_content)
    try:
        data = read_csv_files([file_path])

        assert len(data) == 2
        assert data[0]['name'] == 'Alex Ivanov'
        assert data[0]['position'] == 'Backend Developer'
        assert data[0]['completed_tasks'] == 45
        assert data[0]['performance'] == 4.8
        assert data[0]['experience_years'] == 5
        assert data[1]['name'] == 'Maria Petrova'
        assert data[1]['performance'] == 4.7
    finally:
        Path(file_path).unlink()


def test_read_csv_files_multiple():
    """Тест чтения нескольких CSV файлов."""
    csv_content1 = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django",API Team,5"""

    csv_content2 = """name,position,completed_tasks,performance,skills,team,experience_years
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript",Web Team,4"""

    file1 = create_test_csv(csv_content1)
    file2 = create_test_csv(csv_content2)

    try:
        data = read_csv_files([file1, file2])

        assert len(data) == 2
        positions = {d['position'] for d in data}
        assert positions == {'Backend Developer', 'Frontend Developer'}
    finally:
        Path(file1).unlink()
        Path(file2).unlink()


def test_read_csv_files_invalid_format():
    """Тест обработки неверного формата CSV."""
    csv_content = """name,position,completed_tasks
Alex Ivanov,Backend Developer,invalid"""

    file_path = create_test_csv(csv_content)
    try:
        with pytest.raises(ValueError, match="Неверный формат данных"):
            read_csv_files([file_path])
    finally:
        Path(file_path).unlink()


def test_read_csv_files_file_not_found():
    """Тест обработки отсутствующего файла."""
    with pytest.raises(FileNotFoundError):
        read_csv_files(['nonexistent.csv'])


def test_detect_delimiter_comma():
    """Тест определения разделителя - запятая."""
    csv_content = "name,position,value\nJohn,Developer,100"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                     delete=False, encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        delimiter = detect_delimiter(file_path)
        assert delimiter == ','
    finally:
        Path(file_path).unlink()


def test_detect_delimiter_tab():
    """Тест определения разделителя - табуляция."""
    csv_content = "name\tposition\tvalue\nJohn\tDeveloper\t100"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                     delete=False, encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        delimiter = detect_delimiter(file_path)
        assert delimiter == '\t'
    finally:
        Path(file_path).unlink()


def test_detect_delimiter_semicolon():
    """Тест определения разделителя - точка с запятой."""
    csv_content = "name;position;value\nJohn;Developer;100"

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv',
                                     delete=False, encoding='utf-8') as f:
        f.write(csv_content)
        file_path = f.name

    try:
        delimiter = detect_delimiter(file_path)
        assert delimiter == ';'
    finally:
        Path(file_path).unlink()


def test_read_csv_files_empty():
    """Тест чтения пустого файла."""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years"""

    file_path = create_test_csv(csv_content)
    try:
        data = read_csv_files([file_path])
        assert data == []
    finally:
        Path(file_path).unlink()


def test_read_csv_files_invalid_numeric():
    """Тест обработки неверных числовых значений."""
    csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,invalid,4.8,Python,API Team,5"""

    file_path = create_test_csv(csv_content)
    try:
        with pytest.raises(ValueError, match="Неверный формат данных"):
            read_csv_files([file_path])
    finally:
        Path(file_path).unlink()


def test_read_csv_files_missing_column():
    """Тест обработки отсутствующего столбца."""
    csv_content = """name,position,completed_tasks,skills,team,experience_years
Alex Ivanov,Backend Developer,45,Python,API Team,5"""

    file_path = create_test_csv(csv_content)
    try:
        with pytest.raises(ValueError, match="Неверный формат данных"):
            read_csv_files([file_path])
    finally:
        Path(file_path).unlink()