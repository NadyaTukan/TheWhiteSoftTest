import unittest
import json
import requests

from after import ClearingData


class TestClearingData(unittest.TestCase):
    def setUp(self):
        self.clearing_data = ClearingData()
        self.data_link = "https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json"
        self.replacements_path = "../Data/replacement.json"
        self.results_path = "./results.json"


    def test_get_data(self):
        correct_data = "../Data/data.json"
        data_text = requests.get(self.data_link)
        correct_data = json.loads(data_text.text)
        geting_data = self.clearing_data.get_data(self.data_link)

        self.assertEqual(geting_data, correct_data)

    def test_get_replacements(self):
        with open(self.replacements_path, "r") as read_file:
            correct_replacements = json.load(read_file)
        geting_replacements = self.clearing_data.get_replacements(self.replacements_path)

        self.assertEqual(geting_replacements, correct_replacements)

    def test_writing_results(self):
        test_text = "test_writing_results"
        self.clearing_data.writing_results(test_text, self.results_path)

        with open(self.results_path, "r") as read_file:
            test_results = json.load(read_file)

        self.assertEqual(test_results, test_text)

    def test_cleaning_replacements_from_repetitions_without_repetitions(self):

        test_replacements = [{"replacement": "Test1 Test1", "source": "data1"},
                             {"replacement": "Test2 Test2", "source": "data2"}]

        correct_replacements = {"Test1 Test1": "data1", "Test2 Test2": "data2"}

        clean_replacements = self.clearing_data.cleaning_replacements_from_repetitions(test_replacements)

        self.assertEqual(clean_replacements, correct_replacements)

    def test_cleaning_replacements_from_repetitions_with_repetitions(self):
        test_replacements = [{"replacement": "Test", "source": "data1"},
                             {"replacement": "Test", "source": "data2"}]
        correct_replacements = {"Test": "data2"}

        clean_replacements = self.clearing_data.cleaning_replacements_from_repetitions(test_replacements)

        self.assertEqual(clean_replacements, correct_replacements)

    def test_cleaning_from_replacements_without_change(self):
        test_data = ["Test1 Test1 Test1", "Test2 Test2 Test1"]
        test_replacements = {"Test Test": "data"}
        correct_data = ["Test1 Test1 Test1", "Test2 Test2 Test1"]

        clean_data = self.clearing_data.cleaning_from_replacements(test_replacements, test_data)

        self.assertEqual(clean_data, correct_data)

    def test_cleaning_from_replacements_with_change(self):
        test_data = ["Test1 Test1 Test1", "Test2 Test2 Test1"]
        test_replacements = {"Test1": "data1", "Test2": "data2"}
        correct_data = ["data1 data1 data1", "data2 data2 data1"]

        clean_data = self.clearing_data.cleaning_from_replacements(test_replacements, test_data)

        self.assertEqual(clean_data, correct_data)

    def test_cleaning_from_replacements_with_none(self):
        test_data = ["Test1 Test1 Test1", "Test2 Test2 Test1"]
        test_replacements = {"Test1 Test1 Test1": None}
        correct_data = ["Test2 Test2 Test1"]

        clean_data = self.clearing_data.cleaning_from_replacements(test_replacements, test_data)

        self.assertEqual(clean_data, correct_data)

if __name__ == '__main__':
    unittest.main()
