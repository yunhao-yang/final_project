import sqlalchemy as sql
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import insert, select, update
import pandas as pd

class DataLoader:
    # Abstract class for reading data
    def read_table(self, table_name):
        raise NotImplementedError()
        
class DB_DataLoader(DataLoader):
    # sub-class of DataLoader, which uses database to store data
    def __init__(self, **kwargs):
        metadata = MetaData()
        self._metadata = metadata
        
        # environment variables
        self._environs = Table('environs', metadata,
                        Column('var', String(100), primary_key=True),
                        Column('value', String(200)))
        
        # template jobs
        self._tpl_jobs = Table('tpl_jobs', metadata,
                        Column('job_name', String(20), primary_key=True),
                        Column('job_desc', String(60)))
        
        # template nodes
        self._tpl_nodes = Table('tpl_nodes', metadata,
                        Column('node_id', Integer, primary_key=True),
                        Column('node_type', String(5)),
                        Column('job_name', String(20), ForeignKey('tpl_jobs.job_name')))
        
        # template node dependencies
        self._tpl_node_deps = Table('tpl_node_deps', metadata,
                        Column('p_node_id', Integer, ForeignKey('tpl_nodes.node_id')),
                        Column('c_node_id', Integer, ForeignKey('tpl_nodes.node_id')),
                        Column('p_date', Integer),
                        Column('c_date', Integer))
        
        self._engine = create_engine(kwargs['engine'])
                               
                    
    def read_table(self, table_name):
        
        stmt = select(['{}.*'.format(table_name)])
        connection = self._engine.connect()
        results = connection.execute(stmt).fetchall()
        
        return pd.DataFrame(results)
    
    
class CSV_DataLoader(DataLoader):
    # sub-class of DataLoader, which uses CSV to store data
    
    def __init__(self, **kwargs):
        table_dict = {}
        
        table_dict['tpl_nodes'] = pd.read_csv('tables/tpl_nodes.csv')[['node_id','node_type','job_name',
                                                           'node_name', 'exec_command','signoff_time']]
        table_dict['tpl_jobs'] = pd.read_csv('tables/tpl_jobs.csv')[['job_name', 'job_desc']]
        table_dict['tpl_node_deps'] = pd.read_csv('tables/tpl_node_deps.csv')[['p_node_id','p_date','c_node_id','c_date']]
        table_dict['environs'] = pd.read_csv('tables/environs.csv')[['var', 'value']]
        
        self._table_dict = table_dict
    
    def read_table(self, table_name):
        return self._table_dict[table_name]