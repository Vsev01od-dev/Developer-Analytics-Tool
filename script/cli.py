import argparse
import sys
from pathlib import Path
from .reports import get_report_generator
from .reader import read_csv_files


def main():
    parser = argparse.ArgumentParser(
        description="Анализ эффективности работы разработчиков",
        prog="dev-analytics"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчета (performance)",
    )

    args = parser.parse_args()

    # Проверка файлов
    missing_files = []
    for file_path in args.files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"Ошибка: следующие файлы не найдены:", file=sys.stderr)
        for f in missing_files:
            print(f"  - {f}", file=sys.stderr)
        sys.exit(1)

    # Чтение данных
    try:
        data = read_csv_files(args.files)
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка в данных: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неизвестная ошибка при чтении файлов: {e}", file=sys.stderr)
        sys.exit(1)

    # Генерация отчета
    try:
        report_generator = get_report_generator(args.report)
        report_data = report_generator.generate(data)
        report_generator.display(report_data)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при генерации отчета: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()