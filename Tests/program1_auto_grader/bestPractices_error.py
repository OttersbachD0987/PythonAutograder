"""
Instructor Comments:

Your code runs well, but you imported a library that you never used. 
Also, consider adding some blank lines throughout your code to make it visually easier to read.

"""


# John Smith
# 9/18/2024
# P3HW2
# get pay rate and ot and clacl pay for employee and display it all
import math
#ask employee name, hours worked, and pay rate
employees = 0
total_ot = 0
total_pay = 0
total_gross = 0
name = input("Enter employee's name: ")
while name != "Done":
    hours = (float(input("Enter number of hours worked: ")))
    pay_rate = float(input("Enter employee's pay rate: "))
    #determine if the user has overtime hours, and if so calc pay for OT hours
    if hours > 40:
        base_pay = 40 * pay_rate
        ot = hours - 40
        ot_pay = ot * (pay_rate * 1.5)
    else:
        base_pay = hours * pay_rate
        ot_pay = 0
        ot = 0
    #calc gross pay
    gross_pay = base_pay + ot_pay
    #show employee name, hours worked, pay rate, OT, OT pay, normal pay, and gross pay
    print("-" * 37)
    print("Employee name:   " + name)
    print()
    print(f"{'Hours Worked':<15}{'Pay Rate':<12}{'OverTime':<12}{'OverTime Pay':<20} {'RegHour Pay':<20}{'Gross Pay':<19}")
    print("-" * 99)
    #print(str(hours) + " " + str(pay_rate) + " " + str(ot) + " " + str(ot_pay) + " $" + str(base_pay) + " $" +str(gross_pay))
    print(f"{hours:<15}${pay_rate:<11.2f}{ot:<12}${ot_pay:<19.2f} ${base_pay:<19.2f}${gross_pay:<18.2f}")
    #calculate each employees pays to the whole pay of all employees
    employees += 1
    total_ot += ot_pay
    total_pay += base_pay
    total_gross = total_ot + total_pay
    #get new input for variable
    print()
    name = input("Enter employee's name or \"Done\" to terminate: ")
#loop ends here
#print cumulitive employees and pay
print()
print("Total number of employees entered: " + str(employees))
print(f"Total amount paid for overtime: ${total_ot:.2f}")
print(f"Total amount paid for regular hours: ${total_pay:.2f}")
print(f"Total amount paid in gross: ${total_gross:.2f}")
