from .file import get_cwd, glob_files


class PyPathFinder:
    def __init__(self, directory: str) -> None:
        self._cwd = get_cwd()
        self._target = self._cwd / directory

    def glob_path(self, file_name: str, /, *, as_relative: bool = False) -> list[str]:
        cogs = list(glob_files(self._target, file_name))
        if as_relative:
            cogs = [path.relative_to(self._cwd) for path in cogs]

        return [f.as_posix().removesuffix(f.suffix).replace("/", ".") for f in cogs]
