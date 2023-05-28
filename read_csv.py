import csv

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def reload_csv(listing):
    res_arr = []
    for i in listing:
        res_arr.append(i[0].replace('https://vk.com/',''))
    return res_arr

# print(reload_csv(read_csv_file('aims.csv')))