'''
Instructor Comments:

The amount of money paid for regular hours worked is incorrect if the employee works any overtime. (-20 points)

Also, usage of "while True" loop constitutes using a concept not learned in class. I know it works, but it is not the proper way to build logic into the while loop (-10 points)

'''


# John Smith
# 3/27/24
# P4HW2
# Calucalate amount of employees and their pay, and implement termination process

employee = []

Total_ot_pay = 0
Total_regular_pay = 0
Total_gross_pay = 0

while True:
    employee_name = (input("Enter employee's name or 'Done' to terminate: "))
    if employee_name == "Done": 
        break
    
    hours_worked = float(input(f"How many hours did {employee_name} work? "))
    pay_rate = float(input(f"What is {employee_name}'s pay rate? "))

    OT_hours = 0
    OT_pay = 0 
    reg_pay = 0

    if hours_worked > 40:
        OT_hours = hours_worked - 40
        reg_hours = 40 
        OT_pay = OT_hours * (pay_rate*1.5)
    else:
        reg_hours = hours_worked
    
    reg_pay = hours_worked * pay_rate
    gross_pay = OT_pay + reg_pay

    Total_ot_pay += OT_pay
    Total_regular_pay += reg_pay
    Total_gross_pay += gross_pay
    
    employee.append([employee_name,hours_worked,pay_rate,OT_hours,OT_pay,reg_pay,gross_pay])

    print(f"employee name: {employee_name}")
    print(f"{'Hours Worked':<20}{'Pay Rate':<20}{'OverTime':<20}{'OverTime pay':<20}{'RegHour Pay':<20}{'Gross Pay':<20}") 
    print("-----" * 22)
    print(f"{hours_worked:<20.2f}${pay_rate:<19.2f}{OT_hours:<20.2f}${OT_pay:<19.2f}${reg_pay:<19.2f}${gross_pay:<19.2f}")
    print()

print()
print("Total number of employees entered:",len(employee))
print(f"Total amount paid for overtime: ${Total_ot_pay:.2f}")
print(f"Total amount paid for regular hours: ${Total_regular_pay:.2f}")
print(f"Total amount paid in gross: ${Total_gross_pay:.2f}")