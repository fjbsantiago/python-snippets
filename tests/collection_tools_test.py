import os
import unittest
import json

import pandas as pd
import pandas.util.testing as pdt

from utils import collection_tools


class TestBase(unittest.TestCase):

    def test_build_hierarchy(self):
        artists = [
            {
                "genre": "blues",
                "decade": "50",
                "name": "muddy waters"
            },
            {
                "genre": "hip hop",
                "decade": "90",
                "name": "kriss kross"
            },
            {
                "genre": "blues",
                "decade": "90",
                "name": "buddy guy"
            },
            {
                "genre": "rock",
                "decade": "80",
                "name": "rolling stones"
            },
            {
                "genre": "rock",
                "decade": "90",
                "name": "rolling stones"
            }
        ]

        with self.assertRaises(collection_tools.NoFieldsError):
            collection_tools.build_hierarchy(artists, fields=[])

        with self.assertRaises(collection_tools.FormatError):
            collection_tools.build_hierarchy(artists, fields='sala')

        decades = collection_tools.build_hierarchy(artists, fields=['decade'])
        self.assertEquals(len(decades), 3)
        for node in decades:
            self.assertTrue(node['title'] in ('50', '80', '90'))

        artist_nodes = collection_tools.build_hierarchy(
            artists, fields=['name', 'decade'])
        self.assertEquals(len(artist_nodes), 4)
        for node in artist_nodes:
            # Check that all names are in the first level
            self.assertTrue(node['title'] in (
                'kriss kross', 'buddy guy', 'muddy waters', 'rolling stones'))
            for sub_node in node['nodes']:
                # Check that decades are in the second level
                self.assertTrue(sub_node['title'] in ('50', '80', '90'))
