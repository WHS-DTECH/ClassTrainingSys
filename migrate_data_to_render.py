#!/usr/bin/env python
"""
Data migration script: Neon (old) → Render Postgres (new)
Copies all tables and data while preserving relationships and IDs.
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker

OLD_DATABASE_URL = os.environ.get("OLD_DATABASE_URL") or os.environ.get("SOURCE_DATABASE_URL")
NEW_DATABASE_URL = os.environ.get("NEW_DATABASE_URL") or os.environ.get("TARGET_DATABASE_URL")

def migrate_data():
    """Migrate all data from old DB to new DB."""
    try:
        if not OLD_DATABASE_URL or not NEW_DATABASE_URL:
            raise RuntimeError(
                "Set OLD_DATABASE_URL (or SOURCE_DATABASE_URL) and NEW_DATABASE_URL (or TARGET_DATABASE_URL) before running this script."
            )

        print("[1] Connecting to old database (Neon)...")
        old_engine = create_engine(OLD_DATABASE_URL, echo=False)
        old_conn = old_engine.connect()
        print("✓ Connected to old database")
        
        print("\n[2] Connecting to new database (Render)...")
        new_engine = create_engine(NEW_DATABASE_URL, echo=False)
        new_conn = new_engine.connect()
        print("✓ Connected to new database")
        
        # Get all table names from old database
        inspector_old = inspect(old_engine)
        table_names = inspector_old.get_table_names()
        print(f"\n[3] Found {len(table_names)} tables to migrate:")
        for table_name in table_names:
            print(f"   - {table_name}")
        
        # Preserve relationships by inserting parent tables before child tables.
        print("\n[4] Preparing dependency-safe table order...")
        preferred_order = [
            "alembic_version",
            "users",
            "courses",
            "lessons",
            "sections",
            "enrollments",
            "assignments",
            "quizzes",
            "quiz_questions",
            "assignment_rubrics",
            "rubric_criteria",
            "submissions",
            "quiz_attempts",
            "lesson_progress",
            "comment_feedback",
            "comment_checks",
            "debug_checks",
            "notifications",
            "grade_details",
        ]
        ordered_table_names = [name for name in preferred_order if name in table_names]
        ordered_table_names.extend(name for name in table_names if name not in ordered_table_names)
        print("✓ Table order prepared")

        data_tables = [name for name in ordered_table_names if name != "alembic_version"]
        if data_tables:
            print("\n[4b] Clearing target tables...")
            truncate_sql = "TRUNCATE TABLE " + ", ".join(data_tables) + " RESTART IDENTITY CASCADE"
            new_conn.execute(text(truncate_sql))
            new_conn.commit()
            print("✓ Target tables cleared")
        
        # Copy each table
        print("\n[5] Copying data...")
        for table_name in ordered_table_names:
            try:
                if table_name == "alembic_version":
                    print(f"   ✓ {table_name}: already present")
                    continue

                # Get column info
                # Query all data from old table
                select_query = text(f"SELECT * FROM {table_name}")
                old_rows = old_conn.execute(select_query).fetchall()
                
                if not old_rows:
                    print(f"   ✓ {table_name}: 0 rows (table empty)")
                    continue
                
                # Insert using reflected SQLAlchemy tables so reserved identifiers are quoted correctly.
                metadata = MetaData()
                target_table = Table(table_name, metadata, autoload_with=new_engine)
                row_dicts = [dict(row._mapping) for row in old_rows]
                new_conn.execute(target_table.insert(), row_dicts)
                
                new_conn.commit()
                print(f"   ✓ {table_name}: {len(old_rows)} rows copied")
            
            except Exception as e:
                print(f"   ✗ {table_name}: ERROR - {str(e)}")
                new_conn.rollback()
                continue

        # Reset sequences so future inserts don't collide with imported IDs.
        print("\n[6] Resetting ID sequences...")
        for table_name in ordered_table_names:
            try:
                if table_name == "alembic_version":
                    continue

                sequence_name = new_conn.execute(
                    text("SELECT pg_get_serial_sequence(:table_name, 'id')"),
                    {"table_name": table_name},
                ).scalar()

                if not sequence_name:
                    continue

                max_id = new_conn.execute(
                    text(f"SELECT COALESCE(MAX(id), 0) FROM {table_name}")
                ).scalar()

                if max_id and int(max_id) > 0:
                    new_conn.execute(
                        text("SELECT setval(:sequence_name, :next_value, true)"),
                        {"sequence_name": sequence_name, "next_value": int(max_id)},
                    )
                else:
                    new_conn.execute(
                        text("SELECT setval(:sequence_name, 1, false)"),
                        {"sequence_name": sequence_name},
                    )
            except Exception as e:
                print(f"   ✗ {table_name}: sequence reset error - {str(e)}")
                new_conn.rollback()
                continue

        new_conn.commit()
        print("✓ ID sequences reset")
        
        # Verify row counts
        print("\n[7] Verifying data transfer...")
        all_match = True
        for table_name in table_names:
            try:
                old_count = old_conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                new_count = new_conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                
                match = "✓" if old_count == new_count else "✗"
                print(f"   {match} {table_name}: old={old_count}, new={new_count}")
                
                if old_count != new_count:
                    all_match = False
            except Exception as e:
                print(f"   ✗ {table_name}: verification failed - {str(e)}")
                all_match = False
        
        # Final summary
        print("\n" + "="*60)
        if all_match:
            print("✓ DATA MIGRATION COMPLETE - All tables verified!")
            print("="*60)
            return True
        else:
            print("✗ DATA MIGRATION INCOMPLETE - Row count mismatches detected!")
            print("="*60)
            return False
    
    except Exception as e:
        print(f"\n✗ MIGRATION FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        try:
            old_conn.close()
            new_conn.close()
        except:
            pass

if __name__ == '__main__':
    print("╔════════════════════════════════════════════════════════╗")
    print("║  Data Migration: Neon → Render Postgres               ║")
    print("╚════════════════════════════════════════════════════════╝")
    
    success = migrate_data()
    sys.exit(0 if success else 1)
