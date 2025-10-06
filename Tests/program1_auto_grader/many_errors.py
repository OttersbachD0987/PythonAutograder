"""
Instructor Comments:

It looks like you used AI to write this program for you. There are many advanced concepts used that we haven't covered in class. (-10 points)

Additionally, the program should calculate the overtime hours, not ask the user to enter them: (-10 points)

The program should end and display the final paid totals when the user enters 'Done', not 'q'.

When the user inputs a 'q' the program should show the total number of employees entered and the totals for the amounts paid to all employees. 
All this program does is end without giving the total outputs. (-15 points)

"""


# P4HW2
# John Smith
# 11/7/2024

import sys

# Loop to keep asking for employees until the user quits
while True:
    # Input for employee name
    employee = input("Enter employee name or 'q' to quit: ")
    if employee.lower() == 'q':  # check for quit input
        sys.exit("Exiting program.")
    
    # Input for regular hours, pay rate, and overtime
    try:
        hours_worked = float(input("How many hours did they work? "))
        pay_rate = float(input("What is their hourly pay rate? $"))
        overtime_hours = float(input("How many overtime hours did they work? "))
    except ValueError:
        print("Invalid input, please enter numeric values.")
        continue  # skip to the next iteration of the loop if input is invalid

    # Calculate regular pay and overtime pay
    overtime_rate = pay_rate * 1.5  # Assuming overtime is paid at 1.5 times the regular rate
    regular_pay = hours_worked * pay_rate
    overtime_pay = overtime_hours * overtime_rate

    # Total gross pay
    gross_pay = regular_pay + overtime_pay

    # Display the results
    print("\n" + "-"*40)
    print(f"Employee: {employee}")
    print(f"Hours Worked: {hours_worked}")
    print(f"Overtime: {overtime_hours}")
    print(f"Hourly Pay Rate: ${pay_rate:.2f}")
    print(f"Overtime Pay Rate: ${overtime_rate:.2f}")
    print(f"Gross Pay: ${gross_pay:.2f}")
    print("-"*40 + "\n")
