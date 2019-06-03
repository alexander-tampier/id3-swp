import csv

# Check the cardinality and count the existing ones
# and return the entropy E(S)
import math


def calculate_gain(entropy_s, matrix, attribute_F=0):
    line_count = 0
    cardinality_S_F = []

    for row in matrix:
        if line_count == 0:
            line_count += 1
        else:
            cardinality_S_F.append([row[attribute_F], row[-1]])

    print(cardinality_S_F)


def get_overall_entropy(matrix):
    cardinality = []
    line_count = 0;
    count_cardinality = []
    n = 0

    for row in matrix:
        if line_count == 0:
            line_count += 1
        else:
            cardinality.append(row[-1])

    unique_values = set(cardinality)
    n = len(cardinality)

    for x in unique_values:
        counter = 0
        for value in cardinality:
            if x == value:
                counter += 1;
        count_cardinality.append([x, counter])

    print(count_cardinality)
    print(cardinality)
    return get_entropy(count_cardinality, n)


# For instance: [['yes', 9], ['no', 5]]
# Parameter: Count cardinality in columns
# Return: Entropy of E(S) ie sunny,windy,cloudy
def get_entropy(count_cardinality, n):
    entropy_s = 0;
    for entry in count_cardinality:
        p = entry[1] / n
        entropy_s = entropy_s - p * math.log2(p)
    print(f'Entropy S: {entropy_s}')
    return entropy_s


def load_csv(file):
    with open(file) as csv_file:
        data = []
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if (line_count == 0):
                row[0] = row[0][1:]
                line_count+=1
            data.append(row)

    return data


def main():
    csv_matrix = load_csv('./06_machinelearning_id3_table_weather.csv')
    e_s = get_overall_entropy(csv_matrix)
    calculate_gain(e_s,csv_matrix)


if __name__ == "__main__": main()
