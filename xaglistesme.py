#!/usr/bin/python

import re

f = open('OI_data/omglistesme.OI.out', 'r')
lines = f.readlines()
f.close()

# Deleting first 5 lines
del lines[0:5+1]

# Parsing omglistesme output
omglistesme_parsed = []
for line in lines:
    splitted1 = line.replace('//', ' ')
    splitted2 = splitted1.replace('>>> ', '')
    splitted3 = splitted2.replace('::', '')
    splitted4 = splitted3.replace('', '')
    splitted5 = splitted4.replace('\n', '')
    splitted6 = splitted5.replace(' : ', ' ')
    splitted7 = splitted6.replace('ClientSocketConnection', 'CLIENT')
    splitted8 = splitted7.replace('ServerSocketConnection', 'SERVER')
    regex_line = re.search(r"(^\w+)(\.\d+)\W+(\w+)\W+(\w+)\W+(.+):(.+) (.+):(.+)", splitted8)
    regex_result = list(regex_line.group(1, 3, 4, 5, 6, 7, 8))
    omglistesme_parsed.append(regex_result)

# ESMENAME = input('Provide EndPoint to list: ')
ESMENAME = 'ota4'

esme_aep = []
for item in omglistesme_parsed:
    if item[0] == ESMENAME and item[2] == 'SERVER':
        esme_aep.append(item)
    continue

esme_nep = []
for item in omglistesme_parsed:
    if item[0] == ESMENAME and item[2] == 'CLIENT':
        esme_nep.append(item)
        continue

print('=== AEP ====== {} {}'.format(esme_aep[0][0], '='*50))
for item in esme_aep:
    print('[{}] {:>25} : {:5} {:>20} : {:5}'.format(item[1], item[3], item[4], item[5], item[6]))



print('=== NEP ====== {} {}'.format(esme_nep[0][0], '='*50))
for item in esme_nep:
        print('[{}] {:>25} : {:5} {:>20} : {:5}'.format(item[1], item[3], item[4], item[5], item[6]))

print('({}:{}:{}:{}:{}:{})'.format('Name', 'Type', 'Remote Address', 'Remote port', 'Local Address', 'Local port'))
