# -*- coding: utf-8 -*-
# python 3.6
from __future__ import print_function

import os
import datetime
# importing necessary packages
import pprint
import urllib.request
import re
import pandas as pd
from bs4 import BeautifulSoup
import sys

today = datetime.datetime.today()
today_formal = today.strftime("%A_%d_%B_%Y_%I%M_%p")
print(today_formal)

example_lnk_missouri = "https://jobs.mo.gov/content/missouri-warn-notices-py-2017"
example_table_link_FDA = "https://www.fda.gov/Drugs/DrugSafety/DrugRecalls/default.htm"
example_link_with_two_tables = "https://www.genelex.com/patients/conditions/heart-disease/"



def to_string(s):
    """
    makes a string
    input example: 10000
    output example: '1000'
    """
    try:
        return str(s)
    except:
        # Change the encoding type if needed
        return s.encode('utf-8')

def remove_control_chart(s):
    """
    :param s: string that may not be utf-8 encode
    :return:
    """
    s = re.sub(r'\n', ' ', s)
    s = s.replace('\xa0', '')
    s = re.sub(r' +', ' ', s)
    return to_string(s)


def mkdir_if_not_exist(path):
    if not os.path.isdir(path):
        os.mkdir(path)



def parse_html_table(table):
    n_columns = 0
    n_rows = 0
    column_names = []

    for row in table.find_all('tr'):

        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows += 1
            if n_columns == 0:

                n_columns = len(td_tags)

        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())


    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0, n_columns)
    df = pd.DataFrame(columns=columns,
                      index=range(0, n_rows))
    row_marker = 0
    for row in table.find_all('tr'):
        column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker, column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1

    for col in df:
        try:
            df[col] = df[col].astype(float)
        except ValueError:
            pass

    return df



def HTML_table_parse(link):
    """
    this fxn takes a web link and returns a pandas data-frame as a table
    :param link: any link from the web
    :return: dictionary that contains pandas data-frame
    """
    with urllib.request.urlopen(link) as response:
        the_page = response.read()
        bs = BeautifulSoup(the_page,'html.parser')#features="lxml")
        fl_rich_text_containers = bs.find_all('div', class_ = 'fl-rich-text')
      #  pt_quote_containers = bs.find_all('div', class_ = 'patients-quote-text')
        original_table_names = [b.find('span').text for b in bs.find_all(["h4"],
                                       class_=lambda x: x != 'hidden')]

        tables = bs.find_all(lambda tag: tag.name == 'table')
        counter = 0
        article = [to_string(x.p.text) for x in fl_rich_text_containers]
        description ='URL_link:\t' + str(link) + '\nDatetime_Accessed:\t' + str(datetime.datetime.today()) #to_string(' '.join(article))
        table_dictionary = {'DESCR': description, 'df_key_list': [], 'df_list': [], 'df_table_orig_names': original_table_names}
        print("the number of tables on this webpage:", len(tables))
        for table in tables:
            counter += 1
            key = "TABLE_" + str(counter)
            table_dictionary['df_key_list'].append(key)
            df = parse_html_table(table)
            table_dictionary['df_list'].append(df)

    return table_dictionary

example_2 = HTML_table_parse(example_link_with_two_tables)

def write_out_json(pandas_dict, out_file_path):
    """
    this fxn writes out json file
    :param pandas_dict: the table dictionary
    :param out_file_path:
    :return: written out dictionary
    """
    #TO DO: finish fxn



pprint.pprint(HTML_table_parse(example_link_with_two_tables))
pprint.pprint(HTML_table_parse(example_table_link_FDA))
pprint.pprint(HTML_table_parse(example_lnk_missouri))
# if __name__ == '__main__':
#     '''Convert data and normalize it in different ways.
#         For example: if you want to convert a text file to a fully cleaned file, then you run as following:
#             python htmltableparse.py FULLCLEAND <link> <output_file>
#         Input data format is just path to text file.
#     '''
#     # args = parser.parse_args()
#     if sys.argv[1].upper() == "NORMALISED":
#         NORMALISED(sys.argv[2], sys.argv[3])
#     elif sys.argv[1].upper() == "FULLCLEAND":
#         FULLCLEAND(sys.argv[2], sys.argv[3])
#     else:
#         print("Argument error: sys.argv[1] should belongs to \"NORMALISED/FULLCLEAND\"")
#     # main(os.path.abspath(args.infile), os.path.abspath(args.outfile), 2, False)