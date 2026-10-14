import pandas as pd

file_path =r"C:\Users\user\Downloads\employees.csv"

df = pd.read_csv(file_path)
print(df.head(10))
print(df.info())

#average salary by department

average_salary=df.groupby('department')['salary'].mean()
print("The Average Salary By Department: ",average_salary)

#count Employee By Gneder

geneder_count = df['gender'].value_counts()
print("Count by Gneder: ", geneder_count)

#save it employees to the new csv
it_employees = df[df['department'] == 'IT']
print(it_employees)

it_employees.to_csv('it_employee.csv', index=False)
