from file_types import FileUpdate, FileContent


class Persister:
    def __init__(self, directory_path: str):
        self._directory_path = directory_path

    def read_directory(self) -> list[FileContent]:
        pass

    def write_file_update(self, file_update: FileUpdate):
        pass