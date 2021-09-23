Plese check my approach and questions.

********************************************

Approach:

1.Read the data & clean it (get rid of any dups&NaN, change the data types)

2.Filter out all Not OTE values and Group the payslips by year&quarter with sum

3. shift Disbursements by 28 days and Group it by year&quarter with sum

4. Merge the two groups with 'outer' and cal variances


Question

1. I'm not sure if my understanding to the disbursements was correct:
	1. pay_period_from and pay_period_to would not affact the outcomes even if the period is between two different quarters
	2. Whether or not the disbursement belongs to a specific quarter purely depends on the payment_made 
	   for example:
		Super earned between 1st Jan and the 31 st of March (Q1) will need to be paid/Disbursed between the 29th Jan - 28th of Apr.
		So any disbursements later than 28th of Apr belongs to the next quarter and any disbursements earlier than 29th Jan belongs to the pervious quarter.
