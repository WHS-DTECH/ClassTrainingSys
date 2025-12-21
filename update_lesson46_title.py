import sqlite3

db = sqlite3.connect('instance/class_training.db')
db.execute("UPDATE lessons SET title='Lesson 1: Comment Checker' WHERE id=46")
db.commit()
db.close()
print('Lesson title updated to Comment Checker.')
