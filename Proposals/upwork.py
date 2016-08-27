##import necessary modules
import argparse, sys

## parse the string from command line
## listOfStrings - list of strings. can handle empty list
## reverse - sort in ascending or descending. Default False, Ascending
arparser = argparse.ArgumentParser()
arparser.add_argument("-l", "--listOfStrings", nargs='+', required = True, help="list of strings")
arparser.add_argument("-r", "--reverse", help="list of strings")
args = arparser.parse_args()

if int(args.reverse) == 1:
    reverse = True
else:
    reverse = False

def getInstanceType(s):
    if isinstance(s, str):
        return 1
    elif isinstance(s, int):
        return 2


if not args.listOfStrings:
    print 'No Arguments provided. Exiting!'
    sys.exit(1)
else:
    lst = [l.replace('[','').replace(']','') for l in args.listOfStrings]
    if len(lst)>0:
        new_lst = []
        for string in lst:
            index = []
            string_split = string.split()
            str_list = []
            int_list = []
            for s in string_split:
                try:
                    index.append(getInstanceType(int(s)))
                    int_list.append((s))
                except:
                    index.append(getInstanceType(s))
                    str_list.append((s))
            int_list.sort(reverse = reverse)
            str_list.sort(reverse = reverse)
        
            string_split = []
            for i in index:
                if i ==1:
                    string_split.append(str_list.pop(0))
                elif i==2:
                    string_split.append(int_list.pop(0))
            new_lst.append(' '.join(string_split).strip())
        print lst, '\n', new_lst
    else:
        print 'No strings in the list'

