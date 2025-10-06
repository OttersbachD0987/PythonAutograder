'''
Instructor Comments:

Each time you add an employee, the program should calculate their individual pay and display it.
Once you enter "Done", the totals paid to all employees should be displayed.

This program does not display the individual pay after an employee is entered.
It also does not properly accumulate the totals paid to all employees.
At then end, when it should display the totals for all employees, it only disaplays the last employee's information.
I have to enter "Done" twice to end the program.

'''


# John Smith
# 11/18/2024
# P4HW2
# Program calculates paycheck based on over time or no over time

employee_name = input("Enter employee's name or Done to terminate: ")

# Input
while employee_name.lower() != "done":
    hours = int(input("Enter number of hours worked: "))
    pay_rate = float(input("Enter employee's pay rate: "))
    print("-" * 84)

    # Display result aka pay

    print(f"Employee name:    {employee_name}")
    print()
    print(f"{'Hours worked':<15}{'Pay rate':<15}{'OverTime':<15}{'OverTime Pay':<15}{'RegHour Pay':<15}{'Gross pay':<15}")
    print("-" * 84)
    employee_name = input("Enter employee's name or Done to terminate: ")

    # If
    if hours > 40:
        OT_hours = hours - 40
        reg_pay = pay_rate * 40
        T_pay_rate =  pay_rate * 1.5
        OT_pay = OT_pay_rate * OT_hours
        Gross_pay = reg_pay + OT_pay

    else: 
        OT_hours = 0
        reg_pay = hours * pay_rate
        OT_pay_rate =  pay_rate * 1.5
        OT_pay = OT_pay_rate * OT_hours
        Gross_pay = reg_pay

# Display
print(f"{hours:<15}{pay_rate:<15.2f}{OT_hours:<15.2f}{OT_pay:<15.2f}${reg_pay:<15.2f}${Gross_pay:<15.2f}")
employee_name = input("Enter employee's name or Done to terminate: ")


