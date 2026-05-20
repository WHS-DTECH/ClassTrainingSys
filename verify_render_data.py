#!/usr/bin/env python
"""Quick verification for restored Render Postgres data."""

import os
import sys
from sqlalchemy import create_engine, text


def main():
    database_url = os.environ.get("DATABASE_URL") or os.environ.get("TARGET_DATABASE_URL")
    if not database_url:
        print("ERROR: Set DATABASE_URL or TARGET_DATABASE_URL before running.")
        return 1

    engine = create_engine(database_url, echo=False)

    tables = [
        "users",
        "courses",
        "lessons",
        "sections",
        "enrollments",
        "comment_feedback",
        "comment_checks",
        "debug_checks",
    ]

    with engine.connect() as conn:
        print("Render Data Verification")
        print("=" * 30)

        for table in tables:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"{table:16} {count}")

        print("\nCourses:")
        rows = conn.execute(
            text("SELECT id, title FROM courses ORDER BY id")
        ).fetchall()
        for row in rows:
            print(f"- {row.id}: {row.title}")

        missing_video_col = conn.execute(
            text(
                """
                SELECT COUNT(*)
                FROM information_schema.columns
                WHERE table_name = 'lessons' AND column_name = 'video_url'
                """
            )
        ).scalar()
        print("\nlessons.video_url present:", "yes" if missing_video_col else "no")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
