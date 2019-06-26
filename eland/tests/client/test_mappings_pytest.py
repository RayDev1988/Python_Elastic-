# File called _pytest for PyCharm compatability

from pandas.util.testing import (
    assert_series_equal, assert_frame_equal)

import eland as ed
from eland.tests import *
from eland.tests.common import TestData


class TestMapping(TestData):

    # Requires 'setup_tests.py' to be run prior to this
    def test_fields(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        assert TEST_MAPPING1_EXPECTED_DF.index.tolist() == mappings.all_fields()

        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))

        assert TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT == mappings.count_source_fields()

    def test_copy(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        assert TEST_MAPPING1_EXPECTED_DF.index.tolist() == mappings.all_fields()
        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))
        assert TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT == mappings.count_source_fields()

        # Pick 1 source field
        columns = ['dest_location']
        mappings_copy1 = ed.Mappings(mappings=mappings, columns=columns)

        assert columns == mappings_copy1.all_fields()
        assert len(columns) == mappings_copy1.count_source_fields()

        # Pick 3 source fields (out of order)
        columns = ['dest_location', 'city', 'user_name']
        mappings_copy2 = ed.Mappings(mappings=mappings, columns=columns)

        assert columns == mappings_copy2.all_fields()
        assert len(columns) == mappings_copy2.count_source_fields()

        # Check original is still ok
        assert TEST_MAPPING1_EXPECTED_DF.index.tolist() == mappings.all_fields()
        assert_frame_equal(TEST_MAPPING1_EXPECTED_DF, pd.DataFrame(mappings.mappings_capabilities['es_dtype']))
        assert TEST_MAPPING1_EXPECTED_SOURCE_FIELD_COUNT == mappings.count_source_fields()

    def test_dtypes(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        expected_dtypes = pd.Series(
            {'city': 'object', 'content': 'object', 'dest_location': 'object', 'email': 'object',
             'maps-telemetry.attributesPerMap.dataSourcesCount.avg': 'int64',
             'maps-telemetry.attributesPerMap.dataSourcesCount.max': 'int64',
             'maps-telemetry.attributesPerMap.dataSourcesCount.min': 'int64',
             'maps-telemetry.attributesPerMap.emsVectorLayersCount.france_departments.avg': 'float64',
             'maps-telemetry.attributesPerMap.emsVectorLayersCount.france_departments.max': 'int64',
             'maps-telemetry.attributesPerMap.emsVectorLayersCount.france_departments.min': 'int64',
             'my_join_field': 'object', 'name': 'object', 'origin_location.lat': 'object',
             'origin_location.lon': 'object', 'text': 'object', 'tweeted_at': 'datetime64[ns]',
             'type': 'object', 'user_name': 'object'})

        assert_series_equal(expected_dtypes, mappings.dtypes())

    def test_get_dtype_counts(self):
        mappings = ed.Mappings(ed.Client(ELASTICSEARCH_HOST), TEST_MAPPING1_INDEX_NAME)

        expected_get_dtype_counts = pd.Series({'datetime64[ns]': 1, 'float64': 1, 'int64': 5, 'object': 11})

        assert_series_equal(expected_get_dtype_counts, mappings.get_dtype_counts())
