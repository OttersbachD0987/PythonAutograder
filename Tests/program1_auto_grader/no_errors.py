#John Smith
#P4HW2
#3/30/2025
#working on loops in this program that collects an employee's work hours and pay


#getting the input of the user
user_name = input("Enter employee's name or 'Done' to terminate: ")
# Counter variable to count 
employee_count = 0
total_overtime=0
total_reg_pay=0
total_gross=0

#starting the loop
while user_name.lower() != "done":
   #increment the counter of employee's
    employee_count +=1

    # Getting input for hours worked and pay rate
    hours_worked = float(input("Enter number of hours worked: "))
    pay_rate = float(input("Enter employee's pay rate: "))
    

    # Calculations for regular and overtime pay
    reg_pay = (pay_rate * 40)

    #added employee's regular pay 
    total_reg_pay +=reg_pay

    if hours_worked > 40:
        ot_hours = hours_worked - 40
        ot_pay_rate = pay_rate * 1.5
        ot_pay = ot_hours * ot_pay_rate
        #adding total overtime pay
        total_overtime += ot_pay
    else:
        ot_hours = 0
        ot_pay = 0

    # Gross pay calculation
    gross_pay = reg_pay + ot_pay

    #added amount of employee's gross pay
    total_gross +=gross_pay

    # Displaying the employee's details
    print("----------------------------------------------------------------")
    print(f"{'Employee name:':<20}{user_name}")
    print()
    print(f"{'Hours Worked':<20}{'Pay Rate':<20}{'OverTime':<20}{'OverTime Pay':<20}{'RegHour Pay':<20}{'Gross Pay':<20}")
    print("-------------------------------------------------------------------------------------------------------------")
    print(f"{hours_worked:<20.2f}{pay_rate:<20.2f}{ot_hours:<20.2f}{ot_pay:<20.2f}{reg_pay:<20.2f}{gross_pay:<20.2f}")
    print("----------------------------------------------------------------")

    # Prompting for the next employee's name
    user_name = input("Enter employee's name or 'Done' to terminate: ")
print()
#breaking the loop/displaying  
print(f"Total number of employees entered: {employee_count}")
print(f"total amount paid for overtime: {total_overtime:.2f} ")
print(f"Total amount paid for regular hours: {total_reg_pay:.2f} ")
print(f"Total amount paid in gross:{total_gross:.2f} ")
