"""
mkjson is designed to create json entries from a csv file
it might not be glorious, but it will be all mine
you must know the full filepath for the csv file
the csv file must have an equal amount of headers and values (sequential)
"""


def get_file():  # to get the file location
    print("Heyo, where's the fileo? ")
    file_name = raw_input()

    print("So you want me to make \'%s\' into a json file? (y/n)") \
        % (file_name)  # verify that it's the right location
    acknowledge = raw_input()
    if acknowledge.lower() == 'y':
        print("Where would you like the new file? ")
        new_file = raw_input()
        process_file(file_name, new_file)  # run the processing
        return
    elif acknowledge.lower() == 'n':
        print("Ok, idk why you input \'%s\' then, but whatev...") % (file_name)
        get_file()  # user indicated wrong file name, ask for new input
    else:
        print("Listen, bud, you gotta just type y or n.")
        get_file()  # invalid input, ask for new input


def process_file(file, newfile):
    print ("opening \'%s\'") % (file)
    info = []
    f = open(file, "r")
    n = open(newfile, "w")
    for line in f:  # iterate through lines
        info.append(line)
    headers = info[0]  # separate first line into headers
    keys = []  # blank list for parsed headers into keys
    sep = ','  # comma delimiter
    nl = '\r\n'  # new line delimiter

    for word in headers.split(sep,):  # separate first row as headers
        if nl in word:
            head = word.split(nl, 1)[0]  # remove \r\n newline indicators
            keys.append(head)
        else:
            keys.append(word)

    info.pop(0)  # take out the first line containing the headers
    values = []  # blank list for parsed values
    for line in info:  # iterate through lines
        for word in line.split(sep,):  # iterate through words using delimiter
            if nl in word:
                head = word.split(nl, 1)[0]  # separate new line delimiter
                values.append(head)  # append word without delimiter
            else:
                values.append(word)
    n.write('{ "table":\n' + '\t[\n')  # initialize json
    count = 0
    for word in values:  # combine keys and values accordingly
        if count == 0:  # if first item in a row add open curly bracket
            n.write('\t\t' + "{ " + ('"%s": "%s",') %
                    (keys[(values.index(word) % len(keys))],
                     values[values.index(word)])+"\n")
            count += 1
        elif (values.index(word) == (len(values)-1)) and count == (len(keys) - 1):
            n.write(('\t\t' + '"%s": "%s"') %
                    (keys[(values.index(word) % len(keys))],
                    values[values.index(word)]) + " }" + "\n" + "\n")
            n.write('\n\t]\n}')
        elif count == (len(keys) - 1):  # add closed curly for last item
            n.write(('\t\t' + '"%s": "%s"') %
                    (keys[(values.index(word) % len(keys))],
                    values[values.index(word)]) + " }," + "\n" + "\n")
            count = 0

        else:  # if in middle of a row no bracket
            n.write(('\t\t' + '"%s": "%s",') %
                    (keys[(values.index(word) % len(keys))],
                    values[values.index(word)]) + "\n")
            count += 1
    return
get_file()
print("Job completed")
