from datetime import datetime

from file_types import FileContent, FileUpdate


class AuditManager:
    first_file_name = 'audit_1.txt'

    def __init__(self, max_entries_per_file: int, file_contents: list[FileContent]):
        self._max_entries_per_file = max_entries_per_file
        self._file_contents = file_contents
        self._sort_file_contents_by_index()

    def add_record(self, visitor_name: str, time_of_visit: datetime):
        new_record = visitor_name + ';' + time_of_visit.strftime("%Y-%m-%d %H:%M:%S")
        if len(self._file_contents) == 0:
            return self._append_record_to_first_file(new_record)
        return self._append_record_to_existing_file_or_new_file(new_record)

    def _append_record_to_existing_file_or_new_file(self, new_record):
        current_file_index, current_file_content = self._file_contents[-1]
        if current_file_content.line_count < self._max_entries_per_file:
            return self._append_record_to_current_file(current_file_content, new_record)
        else:
            return self._append_record_to_new_file(current_file_index, new_record)

    def _append_record_to_new_file(self, current_file_index, new_record):
        return FileUpdate(f'audit_{current_file_index + 1}.txt', new_record)

    def _append_record_to_current_file(self, current_file_content, new_record):
        new_content = f"{current_file_content.content}\n{new_record}"
        return FileUpdate(current_file_content.file_path, new_content)

    def _append_record_to_first_file(self, new_record):
        return FileUpdate(self.first_file_name, new_record)

    def _sort_file_contents_by_index(self):
        self._file_contents = list(enumerate(sorted(self._file_contents, key=lambda x: x.file_path), start=1))
