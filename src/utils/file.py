import pathlib


def get_cwd() -> pathlib.Path:
    return pathlib.Path.cwd()


def glob_files(glob_dir: pathlib.Path, file_name: str) -> list[pathlib.Path]:
    return list(glob_dir.glob(f"**/{file_name}"))
