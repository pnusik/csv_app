import csv
from collections.abc import Iterator


def get_csv_codes_generator(
        filepath: str, 
        bad_codes: set | None = None,
        fildname="Код потребительской упаковки"
    ) -> Iterator[str]:
    """Построчно читает и возвращает коды из CSV-файла, пропуская bad_codes."""
    with open(filepath, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=",")

        if bad_codes is None:
            bad_codes = set()

        for row in reader:
            code = row.get(fildname)
            
            if code and code not in bad_codes:
                yield str(code)