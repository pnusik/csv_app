import csv
from collections.abc import Iterator


def get_csv_codes_iterator(
    filepath: str,
    bad_codes: set[str] | None = None,
    fieldname: str = "Код потребительской упаковки",
) -> Iterator[str]:
    """Построчно читает, очищает и возвращает коды из CSV-файла, пропуская bad_codes."""
    if bad_codes is None:
        bad_codes = set()

    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=",")

        for row in reader:
            code = row.get(fieldname)
            if not code:
                continue

            code = code.strip()

            #Снимаем внешние кавычки
            if len(code) >= 2 and code.startswith('"') and code.endswith('"'):
                code = code[1:-1]

            #Заменяем сдвоенные кавычки на одинарные
            code = code.replace('""', '"')

            if code and code not in bad_codes:
                yield code

def write_codes_via_itrator(filename, codes_stream: Iterator[str]):
    """Записывает коды из генератора в CSV-файл."""
    with open(filename, "w", encoding="utf-8-sig") as file:
        file.writelines(f"{code}\n" for code in codes_stream if code)