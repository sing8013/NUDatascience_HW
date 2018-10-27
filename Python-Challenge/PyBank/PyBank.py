
## PyBank
'''
![Revenue](Images/revenue-per-lead.jpg)

* In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. 
  You will give a set of financial data called [budget_data.csv](PyBank/Resources/budget_data.csv). 
  The dataset is composed of two columns: `Date` and `Profit/Losses`. 
  (Thankfully, your company has rather lax standards for accounting so the records are simple.)

* Your task is to create a Python script that analyzes the records to calculate each of the following:

  * The total number of months included in the dataset

  * The total net amount of "Profit/Losses" over the entire period

  * The average change in "Profit/Losses" between months over the entire period

  * The greatest increase in profits (date and amount) over the entire period

  * The greatest decrease in losses (date and amount) over the entire period

* As an example, your analysis should look similar to the one below:

  ```text
  Financial Analysis
  ----------------------------
  Total Months: 86
  Total: $38382578
  Average  Change: $-2315.12
  Greatest Increase in Profits: Feb-2012 ($1926159)
  Greatest Decrease in Profits: Sep-2013 ($-2196167)
  ```

* In addition, your final script should both print the analysis to the terminal and export a text file with the results.
'''

# Code Begins here....
import os
import csv

def print_output(str_add,f):
  f.write(str_add + '\n')
  print(str_add)

#print(os.getcwd)
#set file path of budget_data.csv
budget_csv = os.path.join('.','Resources','budget_data.csv')

#set output txt file
output_txt=os.path.join('output.txt')
f_output= open(output_txt,'w')
#print(budget_csv)
total_months=0
net_revenue=0
max_change=0
min_change=0
with open(budget_csv,'r') as f:
  budget_reader=csv.reader(f,delimiter=',')
  
  #skip header
  csvheader=next(f)
  #print(f'CSV Header {csvheader}')

  #read file content in a list
  data_list=[]
  data_list = [[row[0],row[1]] for row in budget_reader]
  # The total number of months included in the dataset
  total_months = len(data_list)
  # The total net amount of "Profit/Losses" over the entire period
  #net_revenue=sum(float(data_list[:][1]))
  net_revenue = sum(int(data_list[i][1]) for i in range(len(data_list)))
  # The average change in "Profit/Losses" between months over the entire period
  avg_change = round(net_revenue/total_months,2) 
  sum_change=0
  #collect change in Profit/Losses for each month against last month
  for i in range(1,len(data_list)-1):
    rev_change= int(data_list[i-1][1]) -int(data_list[i][1])
    #append change in revenue as additonal column to the list
    data_list[i].append(rev_change)
  # The greatest increase in profits (date and amount) over the entire period
    if rev_change>max_change:
      max_change=rev_change
      max_change_date=data_list[i][0]
      max_change_amount = data_list[i][1]
  # The greatest decrease in losses (date and amount) over the entire period
    if rev_change<min_change:
      min_change=rev_change
      min_change_date=data_list[i][0]
      min_change_amount = data_list[i][1]

    sum_change=rev_change+sum_change

avg_change=round(sum_change/total_months,2)
print_output('Financial Analysis',f_output)
print_output('------------------------',f_output)
print_output(f'Total Months: {total_months}',f_output)  
print_output(f'Total: ${net_revenue}',f_output)  
print_output(f'Average Change: ${avg_change}',f_output)
print_output(f'Greatest Increase in Profits: {max_change_date} (${max_change})',f_output)
print_output(f'Greatest Decrease in Profits: {min_change_date} (${min_change})',f_output)
f_output.close

  