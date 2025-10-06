# changed "None" to "Done" as "None" is a python keyword
# P4HW2- Salary Calculator
# request employee information
name = input("Enter employee's name or \"Done\" to terminate: ")
# create accumulator variables for overtime pay, reg pay , gross pay and one to count number of employees entered
overTime_total = 0.0
regPay_total =0.0
gross_total = 0.0
Employee_count = 0
while name !="Done":
    # add one to Employee_count var
    Employee_count +=1
    # ask for employee information
    hoursWorked = float(input("How many hours did "+name+" work? "))
    payRate = float(input("What is "+name+"'s pay rate? "))
    #evalute overtime
    if hoursWorked >40 :
        #calculate overtime
        overtimeHours = hoursWorked - 40
        #Calculate overPay
        overPay = overtimeHours * (payRate * 1.5)
        # update accumulatar var for overtime pay
        overTime_total += overPay
        #calculate salary for reg hours
        regPay = 40 * payRate
        # update accumulator var for reg pay
        regPay_total +=regPay
        # calculate gross pay
        grossPay = regPay + overPay
        # update gross pay total
        gross_total += grossPay
    else:
        overPay = 0.0
        overtimeHours = 0.0
        overTime_total += overPay
        #calculate salary for reg hours
        regPay = hoursWorked * payRate
        # update accumulator var for reg pay
        regPay_total +=regPay
        grossPay = regPay
        # update gross pay total
        gross_total += grossPay
    # Display output
    print("\nEmployee name:  ",name,"\n")
    print(f'{"Hours Worked":<15}{"Pay Rate":<12}{"OverTime":<12}{"OverTime Pay":<20}{"RegHour Pay":<20}{"Gross Pay"}')
    print('----------------------------------------------------------------------------------------')
    print(f'{hoursWorked:<15}{payRate:<12.2f}{overtimeHours:<12}{overPay:<20.2f}{"$"}{regPay:<20.2f}{"$"}{grossPay:.2f}')
    print()
    # ask user for another employee name
    name = input("\nEnter employee's name or \"Done\" to terminate: ")
# Display final results
# display overtime total , regular pay total ,gross pay total and number of employees entered
print("\nTotal number of employees entered: ", Employee_count, sep="")
print("Total amount paid for overtime: $", format(overTime_total,".2f"), sep="")
print("Total amount paid for regular hours: $", format(regPay_total,".2f"), sep="")
print("Total amount paid in gross: $", format(gross_total,".2f"), sep="")
