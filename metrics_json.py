#!/usr/bin/python

import pandas
import json
import re
import sys

def process_init_f():
    ### Header for CSV.
    header = ['Counter', 'Operation', 'Node', 'Topic', 'Node_Id', 'Count_all', 'Count_last']

    ### Reading CSV.
    data_df = pandas.read_csv(csvfile, names = header)

    ### Dropping  unused columns.
    data_df.drop(['Node_Id', 'Counter', 'Count_all', 'Node'], axis=1, inplace=True)

    ### Replacing unwanted strings.
    data_df.replace({'NetworkAccessGroup.*smppClient\.': '(NEP) '}, regex=True, inplace=True)
    data_df.replace({'ApplicationAccessGroup.*\.': '(AEP) '}, regex=True, inplace=True)
    data_df.replace({';$': ''}, regex=True, inplace=True)

    ### Swapping columns
    columnsTitles=["Topic","Operation","Count_last"]
    data_df=data_df.reindex(columns=columnsTitles)

    ### Script logic : construcing lists/dicts
    results = {}
    for (ESME), bag in data_df.groupby(['Topic']):
        contents_df = bag.drop(['Topic'], axis=1)
        count = [dict(row) for i,row in contents_df.iterrows()]
        results.update({ESME: count})
    return results

def show_all():
    """Showing all objects"""
    for key in results.keys():
        print('EP:', key)
        for item in results[key]:
            operation = item['Operation']
            count = item['Count_last']
            print('\t\t {:>30} : {:^10}'.format(operation, count))
        print('\n')


def show_ep(ESME_NAME):
    """Showing searched object"""
    print('EP -->', ESME_NAME)
    for item in results[ESME_NAME]:
        operation = item['Operation']
        count = item['Count_last']
        if count != '0':
            print('\t\t {:>40} : {:^10}'.format(operation, count))
    print('\n')

### MAIN

if len(sys.argv) == 1:
    print('''

    USAGE: ''' + sys.argv[0] + ''' <path to metrics file> <regex_string>

    ''')
    sys.exit
elif len(sys.argv) == 2:
    csvfile = sys.argv[1]
    results = process_init_f()
    show_all()
elif len(sys.argv) == 3:
    csvfile = sys.argv[1]
    search_string = sys.argv[2]
    print('FILE: ', csvfile)
    print('SEARCH STRING: ', search_string)

    results = process_init_f()
    results_list = list(results.keys())
    r = re.compile('.*' + search_string + '.+')
    res_list_pp = filter(r.match, results_list)

    search_list = list(res_list_pp)

    for s_string in search_list:
        show_ep(s_string)
