'''
import pandas

# for testing solver, format puzzle csv as done in sudoku.csv
df = pandas.read_csv("sudoku.csv")
df = df.set_index("ID")
print(df)
'''


def get_rows(df):
    '''
    Save all the rows with all their values to the rows list
    Later used for solving unknown spaces

    :param df: the puzzle, pandas dataframe
    :return: list of all the rows in the puzzle(list of lists)
    '''

    rows = []
    for row in range(1, 10):
        rows.append(df.loc[row, :])
    return rows


def get_columns(df):
    '''
    Save all the columns with all their values to the columns list
    Later used for solving unknown spaces

    :param df: the puzzle, pandas dataframe
    :return: list of all columns in the puzzle(list of lists)
    '''

    columns = []
    for column in range(1, 10):
        columns.append(df.loc[:, "c" + str(column)])
    return columns


def get_groups(df):
    '''
    Save all the groups with all their values to the groups list
    Later used for solving unknown spaces

    :param df: the puzzle, pandas dataframe
    :return: list of all groups in the puzzle(list of lists of lists XD)
    '''

    groups = []
    for row in range(0, 3):
        for column in range(0, 3):
            groups.append(df.loc[1 + 3*row: 3 + 3*row, "c" + str(1 + 3*column): "c" + str(3 + 3*column)])
    return groups


def find_group(item):
    """
    Used for assigning the group to the item

    :param item: unknown space in the puzzle, int
    :return: index of group where item belongs
    """

    if item[0] <= 2:
        if item[1] <= 2:
            return 0
        elif item[1] <= 5:
            return 1
        else:
            return 2

    elif item[0] <= 5:
        if item[1] <= 2:
            return 3
        elif item[1] <= 5:
            return 4
        else:
            return 5

    else:
        if item[1] <= 2:
            return 6
        elif item[1] <= 5:
            return 7
        else:
            return 8


def find_unknowns(rows):
    '''
    Finds all unknown spaces in the sudoku puzzle

    :param rows: rows list made in get_rows()
    :return: all unknown spaces as a dictionary with
             row and column location and the group it
             is in
    '''

    unknowns = []

    for item in range(len(rows)):
        for place in range(len(rows[item])):
            if rows[item][place] == "_":
                # print(num)
                item_dict = {}
                item_dict["row_num"] = item
                item_dict["column_num"] = place
                item_dict["group_num"] = find_group((item_dict["row_num"], item_dict["column_num"]))
                # print(item_dict)
                unknowns.append(item_dict)
    return unknowns


def check_values(rows, columns, groups, unknowns):
    '''
    Runs through all unknown spaces and assigns all
    possible values to that space

    :param rows: list of all the rows from get_rows()
    :param columns: list of all columns from get_columns()
    :param groups: list of all groups from get_groups()
    :param unknowns: list of all unknowns from find_unknowns
    '''

    for item in unknowns:
        available_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        try:  # for the initial creation of item["value"]
            available_nums = item["value"]
        except KeyError:
            item["value"] = available_nums

        # print(item)
        # print(available_nums)
        # print(rows[item["row_num"]].values)
        # print(columns[item["column_num"]].values)
        # print(groups[item["group_num"]].values)

        for value in rows[item["row_num"]].values:  # runs through rows to find possible values
            try:  # to exclude _ from checks
                if int(value) in available_nums:
                    available_nums.remove(int(value))
            except ValueError:
                pass

        for value in columns[item["column_num"]].values:  # runs through columns to find possible values
            try:  # to exclude _ from checks
                if int(value) in available_nums:
                    available_nums.remove(int(value))
            except ValueError:
                pass

        for num in available_nums:  # runs through columns to find possible values
            if str(num) in groups[item["group_num"]].values or num in groups[item["group_num"]].values:
                available_nums.remove(num)

        item["value"] = available_nums  # assigns possible values to the unknown space


def solve(df):
    '''
    Solves the puzzle by running through check values
    many times

    :param df: the puzzle
    '''

    unsolved = True
    start = True
    iterations = 0

    while unsolved:
        '''USE FOR LOOP FOR TESTING'''

        #print(df)
        rows = get_rows(df)
        columns = get_columns(df)
        groups = get_groups(df)
        # print(groups[2])

        if start:  # initialize unknowns only on start of loop
            unknowns = find_unknowns(rows)
            start = False

        # print(unknowns)
        check_values(rows, columns, groups, unknowns)
        # print(groups[7].values)

        for item in unknowns:

            # print(x)
            # print(len(x["value"]))

            '''
            When item[value] only contains one value
            that num is entered into the puzzle and
            can then be used to solve other spaces
            '''
            if len(item["value"]) == 1:
                # print(x, "VALUE IS", x["value"])
                column = item["row_num"] + 1
                row = "c" + str(item["column_num"] + 1)
                df.at[column, row] = item["value"][0]
                unknowns = find_unknowns(rows)

        '''If there are no more unknowns, break the loop'''
        if unknowns == []:
            # print('IN')
            unsolved = False

        if iterations > 500:
            print("FAILED")

        iterations += 1

'''
solve(df)


print(df)
print("DONE")
'''
