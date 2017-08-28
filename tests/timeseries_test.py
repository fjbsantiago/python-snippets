import os
import unittest
import json

import pandas as pd
import pandas.util.testing as pdt

from utils import timeseries


class TestBase(unittest.TestCase):

    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

        self.json_path = os.path.join(self.fixtures_dir, 'timeseries.json')
        self.csv_path = os.path.join(self.fixtures_dir, 'timeseries.csv')

    def test_json_timeseries_to_df(self):
        expected_result = pd.read_csv(self.csv_path)

        input_data = None
        with open(self.json_path) as json_file:
            input_data = json.load(json_file)

        # Run method to be tested
        actual_result = timeseries.json_timeseries_to_df(input_data)

        pdt.assert_frame_equal(expected_result, actual_result)

    def test_df_to_json_timeseries(self):

        expected_result = None
        with open(self.json_path) as json_file:
            expected_result = json.load(json_file)

        df = pd.read_csv(self.csv_path)
        actual_result = timeseries.df_to_json_timeseries(df)

        self.assertEqual(len(expected_result), len(actual_result))

        # Assert that all columns from data frame are there
        for node in actual_result:
            self.assertTrue(node['name'] in df)
            # Assert that all values for each column were transported to node
            self.assertEquals(len(node['data']), len(df[node['name']]))
