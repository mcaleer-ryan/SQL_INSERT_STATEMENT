'''Author: Ryan McAleer
   Description: takes a csv file, representing a data table, as input and writes the SQL CREATE TABLE &
                INSERT INTO statements to a text-file named 'final_query.txt' in the same directory as the program.
                THE PRIMARY KEY MUST BE IN THE LEFTMOST COLUMN.'''


import csv
import os
#  PRIMARY KEY MUST BE IN THE LEFTMOST COLUMN


#  Change to the directory containing your csv files
os.chdir("YOUR_PATH_HERE")


file_name = input('Please enter the name of the CSV file containing your data-table: ')

#  csv.reader() parses for commas and '\n', and returns an iterable with each row as
#  a list of strings, the values that had been separated by a comma in the file
#  append each row to a list, rows, in order to work with the data

file = open(file_name, 'r')
csvReader = csv.reader(file)
rows = []
for row in csvReader:
    rows.append(row)
file.close()


table_name = input('enter the desired name for your table: ')

#  gather data types for query
#  this is used in for both create_table() and insert_into()
#  type_string_list contains the finalized TYPE(LENGTH) strings needed in create_table() EX. ['VARCHAR2(10)', INT(5)]
#  data_type_list contains simply the data-types as strings needed in insert_into() EX. ['VARCHAR2', 'INT']

data_type_list = []
type_string_list = []
input_lengths_list = []
for i in rows[0]:
    input_text = str('What is the type for ' + i + ': ')
    input_length = input('enter the length for ' + i + ': ')
    data_type = input(input_text).upper()
    type_string = str(data_type+'('+input_length+')')
    data_type_list.append(data_type)
    type_string_list.append(type_string)
    input_lengths_list.append(input_length)


def valid_types(input_lengths_list, rows):
    lenghts = []
    for i in range(len(input_lengths_list)):
        if len(rows[1:][i]) > int(input_lengths_list[i]):
            print('\nfield length for ' + rows[0][i] + " is out of whack")
            return False

    return True

def create_table(table_name):
    query_str = 'CREATE TABLE '
    query_str += table_name + '(\n'
    #  loop over the headers
    for i in rows[0]:
        #  Primary key
        if rows[0].index(i) < 1:
            query_str += i +' ' + type_string_list[rows[0].index(i)] + ' NOT NULL PRIMARY KEY\n'
        elif rows[0].index(i) < len(rows[0]) - 1:
            query_str += i +' ' + type_string_list[rows[0].index(i)] + ' NOT NULL\n'
        #  last header, query needs to end with ');'
        else:
            query_str += i + ' ' + type_string_list[rows[0].index(i)] + ' NOT NULL\n' + ');'
    return query_str


def insert_into():
    # will use to check which values must be wrapped with ' ' EX. varchar --> 'value'
    string_dtypes = ['VARCHAR2', 'VARCHAR']
    query_string = str('INSERT INTO ' + table_name + '(')
    # loop over headers, and concatenating them with the first half of the insert statement
    for i in range(len(rows[0])):
        if i < len(rows[0]) - 1:
            query_string += rows[0][i] + ', '
        else:
            query_string += rows[0][i] + ') VALUES'
    # EX. INSERT INTO TABLENAME(Header1, Header2, Header3, HeaderN) VALUES
    first_half_of_insert = query_string
    counter = 0
    insert_intos = []
    #  loop through each row list besides the headers
    for i in rows[1:]:
        lengths_counter = 0
        # each row from the csv will need its own INSERT INTO STATEMENT
        temp_insert_string = first_half_of_insert
        # loop over each element in each row
        for column in i:
            # first element will need and open parenthesis
            if i.index(column) < 1:
                if data_type_list[counter] in string_dtypes:

                    temp_insert_string += " (" + "'" + i[i.index(column)] +"'"
                    counter += 1
                else:
                    temp_insert_string += ' (' + i[i.index(column)]
                    counter += 1

            #  second through n-1 elements will just need be seperated by comma and space
            elif i.index(column) < len(rows[1]) - 1:
                if data_type_list[counter] in string_dtypes:
                    temp_insert_string += ", '" + i[i.index(column)] + "'"
                    counter += 1
                else:
                    temp_insert_string += ',' + ' ' + i[i.index(column)]
                    counter += 1

            #  last element will need the query ended with ');' and counter set back to 0
            else:
                if data_type_list[counter] in string_dtypes:
                    temp_insert_string += ", '" + i[i.index(column)] + "');"
                    counter = 0
                    insert_intos.append(temp_insert_string)
                else:
                    temp_insert_string += ', ' + i[i.index(column)] + ');'
                    counter = 0
                    insert_intos.append(temp_insert_string)

            lengths_counter+= 1

    return insert_intos


#  takes list of insert into-statements, returns string representation of whole list, seperating elems by '\n'
def generate_insert_intos(L1):
    return_string = ''
    for i in L1:
        return_string += i + '\n'
    return return_string


# writes the return values of create_table() & generate_insert_intos() to file named 'final_query.txt' in your cwd
def main():

    if valid_types(input_lengths_list, rows):
        # change to a directory you want the final_query.txt to be written to
        os.chdir("YOUR_PATH_Here")
        b = create_table(table_name)
        a = insert_into()
        c = generate_insert_intos(a)
        file = open('final_query.txt', 'w')
        file.write(b)
        file.write('\n')
        file.write(c)
        file.write('COMMIT;')
        file.close()
    else:
        print('\n\n********************ERROR**************\nsomething went wrong with youre input lengths\ncould not'+
              ' write your queries to text file')

if __name__ == '__main__':
    main()