import pytest

import eland as ed

import pandas as pd

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create pandas and eland data frames
from eland.tests import ELASTICSEARCH_HOST
from eland.tests import FLIGHTS_DF_FILE_NAME, FLIGHTS_INDEX_NAME,\
    ECOMMERCE_DF_FILE_NAME, ECOMMERCE_INDEX_NAME

_pd_flights = pd.read_json(FLIGHTS_DF_FILE_NAME).sort_index()
_pd_flights['timestamp'] = \
    pd.to_datetime(_pd_flights['timestamp'])
_ed_flights = ed.read_es(ELASTICSEARCH_HOST, FLIGHTS_INDEX_NAME)

_pd_ecommerce = pd.read_json(ECOMMERCE_DF_FILE_NAME).sort_index()
_pd_ecommerce['order_date'] = \
    pd.to_datetime(_pd_ecommerce['order_date'])
_pd_ecommerce['products.created_on'] = \
    _pd_ecommerce['products.created_on'].apply(lambda x: pd.to_datetime(x))
_ed_ecommerce = ed.read_es(ELASTICSEARCH_HOST, ECOMMERCE_INDEX_NAME)

class TestData:

    def pd_flights(self):
        return _pd_flights

    def ed_flights(self):
        return _ed_flights

    def pd_ecommerce(self):
        return _pd_ecommerce

    def ed_ecommerce(self):
        return _ed_ecommerce