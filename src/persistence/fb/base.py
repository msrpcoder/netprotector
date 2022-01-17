import os
from elasticsearch import Elasticsearch
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..utils import get_pg_db_url

engine = create_engine(get_pg_db_url())
Base = declarative_base()
es_client = Elasticsearch(
    os.environ.get('ES_HOSTs', 'localhost').split(','),
    maxsize=25,
    sniff_on_start=True,
    sniffer_timeout=30,
    sniff_on_connection_fail=True
)
