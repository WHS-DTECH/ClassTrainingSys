#!/usr/bin/env python
"""
Data migration script: Neon (old) → Render Postgres (new)
Copies all tables and data while preserving relationships and IDs.
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect, MetaData, Table
from sqlalchemy.orm import sessionmaker

# Old database (Neon)
OLD_DATABASE_URL = "postgresql://neondb_owner:npg_oeS4i0cCTtzO@ep-cool-credit-afk10tgv-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# New database (Render Postgres)
NEW_DATABASE_URL = "postgresql://dtech_classwork_db2_user:hnG6S2OxAuQRQ4f8gV4Ikg7ObjiFoLod@dpg-d86fkimq1p3s73bv1se0-a.oregon-postgres.render.com/dtech_classwork_db2?sslmode=require"

def migrate_data():
    """Migrate all data from old DB to new DB."""
    try:
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
        
        # Verify row counts
        print("\n[6] Verifying data transfer...")
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
