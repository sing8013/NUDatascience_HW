import os
import csv
import pandas as pd

def print_output(str_add,f):
  f.write(str_add + '\n')
  print(str_add)

#set file path of budget_data.csv
data_csv = os.path.join('.','Resources','election_data.csv')

#set output txt file
output_txt=os.path.join('output.txt')
f_output= open(output_txt,'w')

with open(data_csv,'r') as f:
  csv_reader=csv.reader(f,delimiter=',')
  csv_header=next(f)
  #convert to list
  #    'Candidate column
  data_list=[row[2] for row in csv_reader]

  #Total Votes
  #tot_votes = sum(int(i for i in range(len(data_list)))
  tot_votes=len(data_list)
  #create list of unique candidate
  results = [[x,data_list.count(x)] for x in set(data_list)]
  #print(results)

  win_perc=0
  for i in range(len(results)):
    perc_votes= round(float(results[i][1])/tot_votes*100,3)
    results[i].append(perc_votes)
    if perc_votes>win_perc:
      win_perc=perc_votes
      winner = results[i][0]

  #temp_list=results[:]
  #print(temp_list)
  
  win_Idx=max(results[i][2] for i in range(len(results)))
  #print(str(win_Idx))

  #print(results)

print_output('Election Results',f_output)
print_output('-------------------------',f_output)
print_output(f'Total Votes: {tot_votes}',f_output)
print_output('-------------------------',f_output)
print_output(f'{results[0][0]}: {results[0][2]}% ({results[0][1]})',f_output)
print_output(f'{results[1][0]}: {results[1][2]}% ({results[1][1]})',f_output)
print_output(f'{results[2][0]}: {results[2][2]}% ({results[2][1]})',f_output)
print_output(f'{results[3][0]}: {results[3][2]}% ({results[3][1]})',f_output)
print_output('-------------------------',f_output)
print_output(f'Winner: {winner}',f_output)
print_output('-------------------------',f_output)
  
