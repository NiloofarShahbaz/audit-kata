from datetime import datetime

from audit import AuditManager
from file_types import FileContent, FileUpdate


class TestAuditManager:
    def test_add_record_WHEN_no_files_exist_THEN_create_first_file(self):
        audit_manager = AuditManager(3, [])
        result = audit_manager.add_record('Alice', datetime.fromisoformat('2019-04-06T18:00:00'))
        assert FileUpdate("audit_1.txt", "Alice;2019-04-06 18:00:00") == result

    def test_add_record_GIVEN_file_not_reached_max_limit_THEN_add_record_to_that_file(self):
        audit_manager = AuditManager(
            3,
            [FileContent('audit_1.txt', "Peter;2019-04-06 16:30:00\nJane;2019-04-06 16:40:00")]
        )
        result = audit_manager.add_record('Alice', datetime.fromisoformat('2019-04-06T18:00:00'))
        assert FileUpdate(
            "audit_1.txt", "Peter;2019-04-06 16:30:00\nJane;2019-04-06 16:40:00\nAlice;2019-04-06 18:00:00"
        ) == result

    def test_add_record_WHEN_current_file_overflows_THEN_create_new_file(self):
        file_contents = [
            FileContent(
                'audit_2.txt',
                "Peter;2019-04-06 16:30:00\nJane;2019-04-06 16:40:00\nJack;2019-04-06 17:00:00"
            ),
            FileContent('audit_1.txt', ''),
        ]
        audit_manager = AuditManager(3, file_contents)
        result = audit_manager.add_record('Alice', datetime.fromisoformat('2019-04-06T18:00:00'))
        assert FileUpdate("audit_3.txt", "Alice;2019-04-06 18:00:00") == result

    def test_add_multiple_records(self):
        file_contents = [
            FileContent(
                'audit_2.txt',
                "Peter;2019-04-06 16:30:00\nJane;2019-04-06 16:40:00\nJack;2019-04-06 17:00:00"
            ),
            FileContent('audit_1.txt', ''),
        ]
        audit_manager = AuditManager(3, file_contents)
        results = [
            audit_manager.add_record('Alice', datetime.fromisoformat('2019-04-06T18:00:00')),
            audit_manager.add_record('Niloo', datetime.fromisoformat('2019-04-09T18:00:00'))
        ]
        assert [
                   FileUpdate("audit_3.txt", "Alice;2019-04-06 18:00:00"),
                   FileUpdate("audit_3.txt", "Niloo;2019-04-09 18:00:00")
               ] == results
