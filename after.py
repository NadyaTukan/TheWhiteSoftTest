import json
import requests


def get_data(link_data):
    data_text = requests.get(link_data)
    return json.loads(data_text.text)


def get_replacements(path_replacements):
    with open(path_replacements, "r") as read_file:
        replacements = json.load(read_file)
    return replacements


def writing_results(clean_data, path_results):
    with open(path_results, "w") as write_file:
        json.dump(clean_data, write_file, indent=2)


def cleaning_replacements_from_repetitions(replacements):
    replacements.reverse()
    replacement_without_repetitions = []
    [replacement_without_repetitions.append(x) for x in replacements if x not in replacement_without_repetitions]
    return replacement_without_repetitions


def cleaning_from_replacements(replacements, data):
    clean_data = data.copy()
    for replacement in replacements:
        if replacement['source'] == None:
            clean_data = [i for i in clean_data if i != replacement['replacement']]
        else:
            for message in clean_data:
                if message.find(replacement['replacement']) != -1:
                    clean_data.insert(clean_data.index(message), message.replace(replacement['replacement'],
                                                                                 replacement['source']))
                    clean_data.remove(message)
    return clean_data


if __name__ == "__main__":
    data = get_data("https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json")
    replacements = cleaning_replacements_from_repetitions(get_replacements("./Data/replacement.json"))
    clean_data = cleaning_from_replacements(replacements, data)
    writing_results(clean_data, "./Data/result.json")

