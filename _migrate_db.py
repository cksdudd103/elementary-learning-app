import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'learning.db')
conn = sqlite3.connect(db_path)

# Attempt table additions
for col, typ in [
    ('time_limit_seconds', 'INTEGER'),
    ('question_count', 'INTEGER'),
    ('is_comprehensive', 'BOOLEAN'),
    ('auto_submitted', 'BOOLEAN'),
]:
    try:
        conn.execute(f'ALTER TABLE attempt ADD COLUMN {col} {typ}')
        print(f'Added attempt.{col}')
    except sqlite3.OperationalError as e:
        print(f'attempt.{col}: {e}')

# AttemptItem table additions
for col, typ in [
    ('image_url', 'TEXT'),
    ('max_points', 'INTEGER'),
]:
    try:
        conn.execute(f'ALTER TABLE attempt_item ADD COLUMN {col} {typ}')
        print(f'Added attempt_item.{col}')
    except sqlite3.OperationalError as e:
        print(f'attempt_item.{col}: {e}')

# Question table additions
for col, typ in [
    ('image_url', 'TEXT'),
    ('max_points', 'INTEGER'),
]:
    try:
        conn.execute(f'ALTER TABLE question ADD COLUMN {col} {typ}')
        print(f'Added question.{col}')
    except sqlite3.OperationalError as e:
        print(f'question.{col}: {e}')

conn.commit()
conn.close()
print('Migration done')
