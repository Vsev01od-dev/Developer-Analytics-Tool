import csv
from typing import List, Dict, Any


def detect_delimiter(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as file:
        sample = file.read(1024)
        file.seek(0)

        comma_count = sample.count(',')
        tab_count = sample.count('\t')
        semicolon_count = sample.count(';')

        if comma_count > tab_count and comma_count > semicolon_count:
            return ','
        elif tab_count > comma_count and tab_count > semicolon_count:
            return '\t'
        elif semicolon_count > comma_count and semicolon_count > tab_count:
            return ';'
        else:
            return ','


def read_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    all_data: List[Dict[str, Any]] = []

    for file_path in file_paths:
        delimiter = detect_delimiter(file_path)

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)

            try:
                for row in reader:
                    row_dict = dict(row)
                    # Преобразуем числовые поля
                    row_dict['completed_tasks'] = int(row_dict['completed_tasks'])
                    row_dict['performance'] = float(row_dict['performance'])
                    row_dict['experience_years'] = int(row_dict['experience_years'])

                    all_data.append(row_dict)

            except (ValueError, KeyError) as e:
                raise ValueError(
                    f"Неверный формат данных в файле {file_path}: {e}"
                )

    return all_data