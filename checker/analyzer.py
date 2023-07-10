import io
import pathlib
from contextlib import redirect_stdout

from flake8.main.application import Application

from checker.models import File, CheckStatus


class Analyzer:
    def __init__(self, file_id: int):
        self._file = File.objects.get(id=file_id)
        self._file_path = pathlib.Path(self._file.file.path)

    def create_result(self) -> CheckStatus:
        check_status = CheckStatus(file=self._file)

        try:
            result = self._analyze_file()
        except BaseException as error:
            print(error)
            check_status.status = CheckStatus.Status.FAIL
            check_status.result = str(error)
        else:
            if result:
                check_status.status = CheckStatus.Status.ERRORS
            else:
                check_status.status = CheckStatus.Status.SUCCESS
            check_status.result = result
        finally:
            check_status.save()
            print(f"END analyze {self._file_path}")
            return check_status

    def _analyze_file(self) -> str:
        print(f"Start analyzing {self._file_path.absolute().as_posix()}")
        valid_file = self._validate_file_path()

        if not valid_file:
            return ""

        app = Application()

        out = io.TextIOWrapper(buffer=io.BytesIO())
        with redirect_stdout(out):
            # запускаем анализ файла
            app.run([valid_file])
            app.formatter.start()

        out.seek(0)
        data = out.read()
        out.close()
        return data

    def _validate_file_path(self) -> str:
        if not self._file_path.exists():
            raise File.DoesNotExist()

        return (
            self._file_path.absolute().as_posix()
            if self._file_path.is_file() and self._file_path.suffix == ".py"
            else ""
        )
