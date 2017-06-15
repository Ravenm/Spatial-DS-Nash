import pprint as pretty
import os, sys


DIRPATH = os.path.dirname(os.path.realpath(__file__))

keys = []
crimes = []


got_keys = False
with open(DIRPATH + "/NYPD_CrimeData/Nypd_Crime_01") as f:
    for line in f:
        line = ''.join(x if i % 2 == 0 else x.replace(',',':') for i, x in enumerate(line.split(',')))
        if not got_keys:
            keys = line
            got_keys = True
            continue

        # d = {}
        # for i in range(len(line)):
        #     d[keys[i]] = line[i]
        # crime.append(d)

        pretty.pprint(crime)
        sys.exit()
