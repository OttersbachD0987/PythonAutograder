'''
Instructor Comments:

This program is close to being correct. One issue is that your final totals are not showing at the end of the program. (-20 points) 
It is because the code to display final totals is in the wrong part of the while loop.

Your employee count is off as well.

Also, the use of the while True loop is not acceptable as it removes the logic from the while loop. (-10 points)

Please resubmit for a higher grade.

'''

#John Smith
#3/26/2025
#P4HW2
# The program however will calculate gross pay for multiple employees, determined by user, and also calculates total amount paid for overtime, total amount paid for regular pay and total amount paid for all employees.


employee_name = input("Enter employee's name:")
hours_worked = float(input("Enter number of hours worked:"))
hourly_pay_rate = float(input("Enter hourly pay rate:"))
print("------------------------------------------------------")
print("Employee Name:", employee_name)
print()
print("Hours Worked Pay Rate Overtime Overtime Pay RegHour Pay Gross Pay")
print("----------------------------------------------------------------------------")
if hours_worked > 40:
 overtime_hours = hours_worked - 40
 overtime_pay = overtime_hours * (hourly_pay_rate * 1.5)
 reg_hour_pay = 40 * hourly_pay_rate
 gross_pay = reg_hour_pay + overtime_pay
 print(f"{hours_worked:10.2f}{hourly_pay_rate:10.2f}{overtime_hours:10.2f}{overtime_pay:10.2f}{reg_hour_pay:10.2f}{gross_pay:10.2f}")
else:
 overtime_hours = 0
 overtime_pay = 0
 reg_hour_pay = hours_worked * hourly_pay_rate
 gross_pay = reg_hour_pay




total_overtime_pay = 0
total_regular_pay = 0
total_gross_pay = 0
employee_count = 0

while True:


    employee_name = input("Enter employee name (or 'Done' to finish): ")

    if employee_name.lower() == "done":
        break



    pay_rate = float(input(f"Enter pay rate for {employee_name}: "))
    hours_worked = float(input(f"Enter hours worked for {employee_name}: "))


    if hours_worked > 40:
        regular_hours = 40
        overtime_hours = hours_worked - 40
    else:
        regular_hours = hours_worked
        overtime_hours = 0

    regular_pay = regular_hours * pay_rate

    overtime_pay = overtime_hours * pay_rate * 1.5
    gross_pay = regular_pay + overtime_pay

    total_regular_pay += regular_pay
    total_overtime_pay += overtime_pay
    total_gross_pay += gross_pay
    employee_count += 1
    print("\nSummary of Employee Payments:")
    print(f"Total Overtime Pay: ${total_overtime_pay:.2f}")
    print(f"Total Regular Pay: ${total_regular_pay:.2f}")
    print(f"Total Gross Pay: ${total_gross_pay:.2f}")
    print(f"Number of Employees Entered: {employee_count}")