from app import db
from sqlalchemy import inspect

inspector = inspect(db.engine)

print("Table: sections")
for col in inspector.get_columns('sections'):
    print(f"  {col['name']} ({col['type']})")

print("\nForeign Keys for sections:")
for fk in inspector.get_foreign_keys('sections'):
    print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

print("\nTable: lessons2")
for col in inspector.get_columns('lessons2'):
    print(f"  {col['name']} ({col['type']})")

print("\nForeign Keys for lessons2:")
for fk in inspector.get_foreign_keys('lessons2'):
    print(f"  {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
