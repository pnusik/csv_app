import csv
from collections.abc import Iterator


def get_csv_codes_iterator(
    filepath: str,
    bad_codes: set[str] | None = None,
    fieldname: str = "Код потребительской упаковки",
    fieldname_shift: str = "Номер смены"
) -> tuple[str, Iterator[str]]:
    """Построчно читает, очищает и возвращает коды из CSV-файла, пропуская bad_codes."""

    if bad_codes is None:
        bad_codes = set()

    def _create_iterator():
        with open(filepath, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")

            if not reader.fieldnames or fieldname not in reader.fieldnames:
                raise ValueError(f"В файле {filepath} нет поля '{fieldname}'")

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

    with open(filepath, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=",")

        if not reader.fieldnames or fieldname_shift not in reader.fieldnames:
            raise ValueError(f"В файле {filepath} нет поля '{fieldname_shift}'")

        first_row = next(reader, None)
        if not first_row:
            raise TypeError(f"В файле '{filepath}' нет строк")
        
        shift = str(first_row.get(fieldname_shift)).strip()
        return shift, _create_iterator()




def get_badcodes(filepath: str) -> set[str]:
    bad_codes = set()
    with open(filepath, encoding="utf-8-sig") as file:
        for line in file:
            c_line = line.strip()

            if c_line:
                bad_codes.add(c_line)
    return bad_codes

def stream_codes_as_csv(filename: str, codes_stream: Iterator[str]):
    """Записывает коды из генератора в CSV-файл."""
    with open(filename, "w", encoding="utf-8-sig") as file:
        file.writelines(f"{code}\n" for code in codes_stream if code)