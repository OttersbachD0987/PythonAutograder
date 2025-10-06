'''
Instructor Comments:

Your code is well written and your logic is sound. The only issue is a syntax error on the very last line. Check your curly brackets.
'''

# John Smith
# 9/25/2024
# P4HW2
# Calculate payrate using if/else statements

# create variables for number of employees and their pay
num_emp = 0
total_ot = 0
total_reg = 0
total_gross = 0

name = input("Enter employee's name or Done to terminate: ")

while name != "Done":
    # Add one to the number of employees
    num_emp += 1
    
    hours = int(input("Enter number of hours worked: "))
    pay_rate = float(input("Enter employee's pay rate: "))

    #Display name (\n can be used to seperate lines)
    print("------------------------------\nEmployee name: ", name)

    #Determine employee pay
    if hours > 40:
     
    #They have some overtime
        reg_pay_amt = 40 * pay_rate
        ot_pay_rate = 1.5 * pay_rate
        ot_hours = hours - 40
        ot_pay_amt = (ot_hours) * ot_pay_rate
        gross_pay = reg_pay_amt + ot_pay_amt
     
    else:

    #No overtime
        reg_pay_amt = hours * pay_rate
        ot_hours = 0
        ot_pay_amt = 0

        # Calculate the gross pay
        gross_pay = reg_pay_amt + ot_pay_amt
        print()

    # Add to employee pay
    total_ot += ot_pay_amt
    total_reg += reg_pay_amt
    total_gross += gross_pay

    # Display headings (F strings dont use commas, curly braces seprate them)
    print(f"{'Hours Worked':<16}{'Pay Rate':<12}{'OverTime':<12}{'OverTime Pay':<15}{'RegHour Pay':<15}{'Gross Pay':<15}")
    print("-" * 100)

    # Formats the result)
    print(f"{hours:<16.1f}${pay_rate:<12.2f}{ot_hours:<10.1f}${ot_pay_amt:<14.2f}${reg_pay_amt:<14.2f}${gross_pay:<15.2f}")

    #Get new inpt for the name bariable - stop the loop
    name = input("Enter employee's name: ")
# Loop ends here
print("Goodbye")

# print total paid and number of employees

print(f"Total number of employees ennter: {num_emp}")
print(f"Total amount paid for overtime: ${total_ot:.2f}")
print(f"Total amount paid for regular hours: ${total_reg:.2f}")
print(f"Total amount paid in gross: ${total_gross:.2f")