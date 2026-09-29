import csv
from collections.abc import Iterator

def clean_code(raw_code: str) -> str:
    code = raw_code.strip()
    if len(code) >= 2 and code.startswith('"') and code.endswith('"'):
        code = code[1:-1]
    return code.replace('""', '"')

def get_csv_codes_iterator(
    filepath: str,
    bad_codes: set[str] | None = None,
    fieldname: str = "Код потребительской упаковки",
    fieldname_shift: str = "Номер смены"
) -> tuple[str, Iterator[str]]:
    """Построчно читает, очищает и возвращает коды из CSV-файла, пропуская bad_codes."""

    bad_codes = bad_codes or set()

    
    file = open(filepath, mode="r", encoding="utf-8-sig", newline="")
    reader = csv.DictReader(file, delimiter=",")

    # Проверка наличия полей
    if not reader.fieldnames:
        file.close()
        raise ValueError(f"Файл '{filepath}' пуст.")

    if fieldname not in reader.fieldnames or fieldname_shift not in reader.fieldnames:
        file.close()
        raise ValueError(f"В файле отсутствуют обязательные поля: '{fieldname}' или '{fieldname_shift}'.")

    # Из 1 строки достаем номер смены
    first_row = next(reader, None)
    if not first_row:
        file.close()
        raise ValueError(f"В файле '{filepath}' нет данных.")

    shift = first_row.get(fieldname_shift, "None_shift")

    def _create_iterator() -> Iterator[str]:
        # Т.к мы уже прокрутили 1 итерацию когда доставали смену, из нее же надо достать код
        try:
            if first_code := first_row.get(fieldname):
                clean = clean_code(first_code)

                if clean and clean not in bad_codes:
                    yield clean

            # Работа с другими кодами
            for row in reader:
                if code := row.get(fieldname, None):
                    clean = clean_code(code)

                    if clean and clean not in bad_codes:
                        yield clean
        finally:
            file.close()

    return shift, _create_iterator()





def get_badcodes(filepath: str) -> set[str]:
    bad_codes = set()
    with open(filepath, encoding="utf-8-sig") as file:
        for code in file:
            c_code = clean_code(code)

            if c_code:
                bad_codes.add(c_code)
    return bad_codes

class stream_codes_as_csv:
    """Записывает коды из генератора в CSV-файл."""
    def __init__(self, filename: str):
        self.filename = filename
        self._file = None

    def __enter__(self):
        self._file = open(self.filename, "w", encoding="utf-8-sig", newline="")
        return self

    def writecode(self, code: str):
        if not self._file:
            raise TypeError("Поток файла csv не открыт")
        self._file.write(f"{code}\n")

    def __exit__(self, exc_type, exc, tb):
        if self._file and not self._file.closed:
            self._file.close()
        self._file = None