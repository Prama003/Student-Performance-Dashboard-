

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3


conn = sqlite3.connect("students.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS student_marks (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    subject TEXT,
    marks INTEGER
)
""")

sample_data = [
    (1, "Amit", "Math", 85),
    (2, "Priya", "Math", 78),
    (3, "Rohan", "Science", 92),
    (4, "Sneha", "Science", 66),
    (5, "Arjun", "English", 74),
    (6, "Riya", "English", 88),
    (7, "Kabir", "Math", 59),
    (8, "Meera", "Science", 81)
]

cursor.executemany("INSERT OR IGNORE INTO student_marks VALUES (?, ?, ?, ?)", sample_data)
conn.commit()


df = pd.read_sql_query("SELECT * FROM student_marks", conn)
print("Student Data:")
print(df)


print("\nAverage marks per subject:")
avg_marks = df.groupby('subject')['marks'].mean()
print(avg_marks)

avg_marks.plot(kind='bar', color=['skyblue', 'lightgreen', 'salmon'])
plt.title("Average Marks by Subject")
plt.xlabel("Subject")
plt.ylabel("Average Marks")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

top_students = df.sort_values(by='marks', ascending=False).head(3)
print("\nTop 3 Performing Students:")
print(top_students[['name', 'subject', 'marks']])

performance_bins = [0, 60, 75, 90, 100]
labels = ['Below Avg', 'Average', 'Good', 'Excellent']
df['Category'] = pd.cut(df['marks'], bins=performance_bins, labels=labels, include_lowest=True)

category_count = df['Category'].value_counts()
category_count.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
plt.title("Performance Distribution")
plt.ylabel("")
plt.show()

conn.close()
