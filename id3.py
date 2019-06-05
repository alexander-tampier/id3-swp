import csv

# Check the cardinality and count the existing ones
# and return the entropy E(S)
import math


class Node:
    def __init__(self, name):
        self.name = name
        self.node_list = {}

    def add_node(self, node):
        self.node_list[node.name] = node

    def __repr__(self):
        return str(self.__dict__)


class AttributeQuality:
    def __init__(self, name, cardinalities, entropy_dict, count_dict, information=0, gain=0):
        self.name = name
        self.cardinalities = cardinalities
        self.entropy_dict = entropy_dict
        self.count_dict = count_dict
        self.information = information
        self.gain = gain

    def calc_gain(self, entropy):
        self.gain = round(entropy - self.information, 3)
        print(self.name, self.gain)

    def calc_information(self):
        n = 0
        sum = 0
        for x in self.count_dict.values():
            for y in x:
                n+=y[1]



        for key in self.entropy_dict:
            counter = 0
            for count in self.count_dict[key]:
                counter += count[1]
            sum +=  counter * 1 / n * self.entropy_dict[key]

        self.information = round(sum, 3)

    def __repr__(self):
        return str(self.__dict__)


def filter_quality(data_S_F, value):
    da_filtered_array = []

    for x in data_S_F:
        if x[0] == value:
            da_filtered_array.append(x[1])

    return da_filtered_array


def count_cardinality_result(cardinality):
    unique_values = set(cardinality)

    count_cardinality = []
    for x in unique_values:
        counter = 0
        for value in cardinality:
            if x == value:
                counter += 1;
        count_cardinality.append([x, counter])

    return count_cardinality


# E(S,F)
# i.e - E(Outlook, Sunny); E(Outlook, Overcast); E(Outlook, Rainy)
def entropy_sub_information(matrix, attribute_F=0):
    line_count = 0
    data_S_F = []
    data_S = []
    name = ""
    entropy = {}
    count = {}

    for row in matrix:
        if line_count == 0:
            name = row[attribute_F]
            line_count += 1
        else:
            data_S_F.append([row[attribute_F], row[-1]])
            data_S.append(row[attribute_F])

    cardinalities = set(data_S)

    for value in cardinalities:
        new_filtered_quality = filter_quality(data_S_F, value)
        card_res = count_cardinality_result(new_filtered_quality)
        count[value] = card_res
        entropy[value] = get_entropy(card_res)

    return AttributeQuality(name, cardinalities, entropy, count)


def get_overall_entropy(matrix):
    cardinality = []
    line_count = 0;

    for row in matrix:
        if line_count == 0:
            line_count += 1
        else:
            cardinality.append(row[-1])

    count_cardinality = count_cardinality_result(cardinality)
    return get_entropy(count_cardinality)


# For instance: [['yes', 9], ['no', 5]]
# Parameter: Count cardinality in columns
# Return: Entropy of E(S) ie sunny,windy,cloudy
def get_entropy(count_cardinality):
    entropy_s = 0;
    n = 0

    for entry in count_cardinality:
        n += entry[1]

    for entry in count_cardinality:
        p = entry[1] / n
        entropy_s = entropy_s - p * math.log2(p)
    return round(entropy_s, 3)


def load_csv(file):
    with open(file) as csv_file:
        data = []
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if (line_count == 0):
                row[0] = row[0][1:]
                line_count += 1
            data.append(row)

    return data


def get_max_gain(objects):
    max_gain = 0
    max_gain_object = None
    for object in objects:
        if max_gain < object.gain:
            max_gain = object.gain
            max_gain_object = object
    return max_gain_object


def modify_data(data, quality):
    fette_data_like_filtered_and_stuff = []
    counter = 0
    for row in data:
        if counter == 0:
            fette_data_like_filtered_and_stuff.append(row)
            counter+=1
        for entry in row:
            if entry == quality:
                fette_data_like_filtered_and_stuff.append(row)

    return fette_data_like_filtered_and_stuff


def id3_recursive(data):

    node = {}

    objects = []
    index = 0

    e_s = get_overall_entropy(data)
    for row in data[0]:
        if index == len(data[0]) - 1:
            break
        column_obj = entropy_sub_information(data, index)

        column_obj.calc_information()
        column_obj.calc_gain(e_s)
        objects.append(column_obj)
        index += 1

    obj = get_max_gain(objects)
    node[obj.name] = {}
    node[obj.name]['children'] = []

    print(obj)


    for quality in obj.cardinalities:
        if len(obj.count_dict[quality]) == 1:
            node[obj.name]['children'].append(obj.count_dict[quality][0][0])
            #print(obj.count_dict[quality])
            return node;
        else:
            new_data = modify_data(data,quality)
            node[obj.name]['children'].append(id3_recursive(new_data))

    return node

    # id3_recursive(new_matrix)


def main():
    matrix = load_csv('./06_machinelearning_id3_table_weather.csv')
    root = id3_recursive(matrix)
    print(root)


if __name__ == "__main__": main()
