import csv

def csvToDic(file):
    reader = csv.reader(open(file, newline=''),delimiter=';', quotechar='|')

    result = {}
    for row in reader:
        key = row[0]
        result[key] = row[1:]
        print (key + str(result[key]))

    return result



def dicToCsv(file, my_dict):
    with open(file, 'w', newline='') as f:  # Just use 'w' mode in 3.x
        csv_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for k, v in my_dict.items():
            csv_writer.writerow([k] + v)

        return True

def appendDicToCsv(file, my_dict):
    with open(file, 'a', newline='') as f:  # Just use 'w' mode in 3.x
        csv_writer = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for k, v in my_dict.items():
            csv_writer.writerow([k] + v)

        return True

def inCsv(file,target):
    data = csvToDic(file)
    if target in data:
        return target, data[target]
    return False