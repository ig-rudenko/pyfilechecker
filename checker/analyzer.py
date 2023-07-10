import io
import pathlib
from contextlib import redirect_stdout

from flake8.main.application import Application


def _validate_file_path(f: pathlib.Path) -> str:
    return f.absolute().as_posix() if f.is_file() and f.suffix == ".py" else ""


def analyze_file(file: pathlib.Path) -> str:
    # создаем объект приложения flake8
    valid_file = _validate_file_path(file)
    if not valid_file:
        return ""

    app = Application()

    out = io.TextIOWrapper(buffer=io.BytesIO())
    with redirect_stdout(out):
        # запускаем анализ файла
        app.run(valid_file)
        app.formatter.start()

    out.seek(0)
    data = out.read()
    out.close()
    return data
