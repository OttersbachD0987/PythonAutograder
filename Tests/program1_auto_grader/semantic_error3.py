'''
Instructor Comments:

Usage of "while True" loop constitutes using a concept not learned in class. I know it works, but it is not the proper way to build logic into the while loop (-10 points)



The program runs well, but does not show the hours worked, pay rate, overtime, etc... for each individual employee. (-10 points)
'''


# John Smith
# 4/1/25
# P4HW2
# Show pay information
total_overtime_pay = 0
total_regular_pay = 0
total_gross_pay = 0
total_employees = 0

while True:
    
    employee_name = input("Enter employee name (or 'Done' to terminate): ")

    
    if employee_name.lower() == "done":
        break

    
    pay_rate = float(input("Enter pay rate for " + employee_name + ": "))
    hours_worked = float(input("Enter hours worked by " + employee_name + ": "))

    
    if hours_worked > 40:
        regular_hours = 40
        overtime_hours = hours_worked - 40
    else:
        regular_hours = hours_worked
        overtime_hours = 0

    regular_pay = regular_hours * pay_rate
    overtime_pay = overtime_hours * pay_rate * 1.5

    
    total_regular_pay += regular_pay
    total_overtime_pay += overtime_pay
    total_gross_pay += regular_pay + overtime_pay
    total_employees += 1


print("Results:")
print(f"Total overtime pay: ${total_overtime_pay:.2f}")
print(f"Total regular pay: ${total_regular_pay:.2f}")
print(f"Total gross pay: ${total_gross_pay:.2f}")
print(f"Number of employees entered: {total_employees}")