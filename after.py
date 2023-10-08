import json
import requests


class ClearingData:

    def __int__(self):
        pass
    def get_data(self, link_data):
        data_text = requests.get(link_data)
        return json.loads(data_text.text)


    def get_replacements(self, path_replacements):
        with open(path_replacements, "r") as read_file:
            replacements = json.load(read_file)
        return replacements


    def writing_results(self, clean_data, path_results):
        with open(path_results, "w") as write_file:
            json.dump(clean_data, write_file, indent=2)

    def cleaning_replacements_from_repetitions(self, replacements):

        replacements.reverse()
        replacement_without_repetitions = {}
        for x in replacements:
            if x['replacement'] not in replacement_without_repetitions:
                replacement_without_repetitions[x['replacement']] = x['source']
        return replacement_without_repetitions

    def cleaning_from_replacements(self, replacements, data):
        clean_data = data.copy()
        for replacement, sourse in replacements.items():
            if replacements[replacement] == None:
                clean_data = [i for i in clean_data if i != replacement]
            else:
                for message in clean_data:
                    if message.find(replacement) != -1:
                        index = clean_data.index(message)
                        clean_data.insert(index, message.replace(replacement, sourse))
                        clean_data.remove(message)
        return clean_data


if __name__ == "__main__":
    clearing_data = ClearingData()
    data = clearing_data.get_data("https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json")
    replacements = clearing_data.get_replacements("./Data/replacement.json")
    replacements_without_repetitions = clearing_data.cleaning_replacements_from_repetitions(replacements)
    clean_data = clearing_data.cleaning_from_replacements(replacements_without_repetitions, data)
    clearing_data.writing_results(clean_data, "./Data/result.json")

