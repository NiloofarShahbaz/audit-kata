from dataclasses import dataclass


@dataclass
class FileContent:
    file_path: str
    content: str

    @property
    def line_count(self) -> int:
        return len(self.content.split('\n'))


@dataclass
class FileUpdate:
    file_name: str
    record: str
