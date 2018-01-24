#!/usr/bin/env python

import pandas
import re
import sys
import os
import signal

def sigint_handler(signum, frame):
    """CTRL+C handling"""
    print('Pressing the CTRL+C!')
    exit()

signal.signal(signal.SIGINT, sigint_handler)


mfile = '/home/cqs/Projects/parsing_metrics/metrics_sample/20180118_141500192.168.50.22Metrics.log_modded'

"""Header for CSV."""
header = ['Counter', 'Operation', 'Node', 'Topic', 'Node_Id', 'Count_all', 'Count_last']

"""Reading CSV."""
data_df = pandas.read_csv(mfile, names = header)

"""Dropping  unused columns."""
data_df.drop(['Node_Id', 'Counter', 'Count_all', 'Node'], axis=1, inplace=True)

"""Replacing unwanted strings."""
data_df.replace({'NetworkAccessGroup.*smppClient\.': '(NEP) '}, regex=True, inplace=True)
data_df.replace({'ApplicationAccessGroup.*\.': '(AEP) '}, regex=True, inplace=True)
data_df.replace({';$': ''}, regex=True, inplace=True)

"""Indexing phase."""
indexed_by_Topic = data_df.set_index(['Topic'])
indexed_by_Operation = data_df.set_index(['Operation'])

"""Changing data types in columns"""
indexed_by_Operation[['Count_last']] = indexed_by_Operation[['Count_last']].astype('int')
indexed_by_Topic[['Count_last']] = indexed_by_Topic[['Count_last']].astype('int')

def find_metric(metric_type):
    print('Search based on metric_type - {}'.format(metric_type))
    print('----------------------------------------------------')
    indexed_by_Operation.sort_values(['Count_last'], inplace=True)
    tailed = indexed_by_Operation.loc[metric_type]
    print(tailed.tail(20))
    print('\n Press ENTER for more queries')
    void = input()
    main()

def find_esme(esmename):
    print('Search based on ESME - {}'.format(esmename))
    print('----------------------------------------------------')
    indexed_by_Topic.sort_values(['Operation'], inplace=True)
    tailed = indexed_by_Topic.loc[esmename]
    print(tailed.tail(20))
    print('\n Press ENTER for more queries')
    void = input()
    main()

def match_topic_pattern():
    """Creates a list of Topics based on regexp given"""
    topic_input = input('Provide Regex for Search (SPC for all): ')
    df_list = data_df['Topic'].tolist()
    u_df_list = set(df_list)
    esme_list = []
    for x in u_df_list:
        for match in re.findall(r'(.*{}.*)'.format(topic_input), x, re.IGNORECASE):
            esme_list.append(match)
    if len(esme_list) == 0:
        print('No Match..')
        main()
    return esme_list

def match_operation_pattern():
    """Creates a list of Operation based on regexp given"""
    operation_input = input('Provide Regex for Search ("_" for all): ')
    df_list = data_df['Operation'].tolist()
    u_df_list = set(df_list)
    metric_list = []
    for x in u_df_list:
        for match in re.findall(r'(.*{}.*)'.format(operation_input), x, re.IGNORECASE):
            metric_list.append(match)
    if len(metric_list) == 0:
        print('No Match..')
        main()
    return metric_list

def const_esmemenu(esme_list):
    """Constructing Esme SubMenu"""
    count = -1
    for f in esme_list:
        count += 1
        menu = '[{}] {}'.format(count, f)
        print(menu)

    while True:
        ans_ch = int(input("Select option: "))
        if ans_ch > count:
            print('Wrong selection.')
            continue
        path = esme_list[ans_ch]
        #print("Selection performed: [{}] {} ".format(ans_ch, path))
        find_esme(path)

def const_metricmenu(metric_list):
    """Constructing Metric SubMenu"""
    count = -1
    for f in metric_list:
        count += 1
        menu = '[{}] {}'.format(count, f)
        print(menu)

    while True:
        ans_ch = int(input("Select option: "))
        if ans_ch > count:
            print('Wrong selection.')
            continue
        path = metric_list[ans_ch]
        #print("Selection performed: [{}] {} ".format(ans_ch, path))
        find_metric(path)

def main():
    os.system('clear')
    """MAIN MENU / START"""
    print("""
    Menu for interaction with Metrics
    ---------------------------------
    [0] Main screen
    [1] List all available metrics for AEP or NEP (Usually ESME name)
    [2] List all available endpoints which are writing to a specific metric
    """)

    while True:
        ans_b = int(input('Select option (CTRL-C for exit): '))
        if ans_b == 1:
            print("Selection performed: [{}]\n".format(ans_b))
            res = match_topic_pattern()
            const_esmemenu(res)
            break
        elif ans_b == 2:
            print("Selection performed: [{}]\n".format(ans_b))
            res = match_operation_pattern()
            const_metricmenu(res)
            break
        elif ans_b == 0:
            os.execv(__file__, sys.argv)
        else:
            print('Wrong selection.')
            break

main()
