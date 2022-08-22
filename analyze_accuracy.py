
import pandas as pd
import os

# print current work directory
print("Working dir:", os.getcwd())

# make a list of all files in the /data folder
data_filelist = []
for root,d_names, f_names in os.walk(os.getcwd()+'/data'):
    for f in f_names:
        if(".xlsx" in f):    
            data_filelist.append(f)
# create empty list
rows = []

# run code for calculating accuracy for every file in the list
for file in data_filelist:
    # read file
    print(file)
    df=pd.read_excel('data/' + file, engine='openpyxl')

    # create dataframe
    data_df = pd.DataFrame(df)

    # extract columns needed for calculations
    dfx= data_df[["Test", "CorrAns","key_resp_3.keys"]]

    # remove all empty cells
    dfx=dfx.dropna()

    # remove index from original dataframe
    dfx = dfx.reset_index(drop=True)

    # split the Test column on / to extract useful variables like Block
    dfx[['Testname', 'Block', 'Number', 'FileName']]=dfx['Test'].str.split('/', expand=True)

    # Split filename further with _ to extract combinations
    dfx[['no use', 'Combinations', 'Event', 'Eventnumber']] = dfx['FileName'].str.split('_', expand=True)

    # select all columns needed for calculation
    dfx = dfx[['Test', 'CorrAns', 'key_resp_3.keys', 'Number','Block', 'FileName', 'Combinations']]

    # put filled in answers and correct answers in a list
    answers = dfx['key_resp_3.keys'].tolist()
    c_answers = dfx['CorrAns'].tolist()

    counter = 0
    right_answers = []

    # for every answer in the list
    for x in answers:
        # check if filled in answer is the same as the correct answer
        if x == c_answers[counter]:
            # add 1 to list
            right_answers.append(1)
        else:
            # add 0 to list
            right_answers.append(0)
        counter +=1

    # add answers with 0 1 to datataframe
    dfx['right_answers'] = right_answers

    # function for calculating accuracy
    def calc_accuracy(df):
        # amount of right answers / amount of wrong answers = accuracy
        return len(df[df['right_answers'] == 1]) / len(df[df['right_answers'] == 0 ])

    overall_accuracy = calc_accuracy(dfx)

    # Define list with columns to calculate
    c_list = ["Block","Combinations"]

    names = []
    accuracies = []
    # add filename and overall accuracy
    names.append("file name")
    names.append("overall accuracy")
    accuracies.append(file)
    accuracies.append(overall_accuracy)

    # for every column in columns to calculate
    for c in c_list:
        # get groups from column. for instance: Block1 and Block2
        unique_values =  dfx[c].unique()
        # for every group in column
        for value in unique_values:
            # select subset with only group
            sub_df =  dfx[dfx[c] == value]
            # add group name
            names.append(value)
            # add accuracy for that group
            accuracies.append(calc_accuracy(sub_df))
    # add list of accuracies to row list
    rows.append(accuracies)

# create new dataframe from rows with variables and use names as column names
final_df = pd.DataFrame(rows,columns=names)
# export final dataframe to excel file
final_df.to_excel('output/accuracies_output.xlsx', index=False)

# I hope this will be good enough, good luck! :)
