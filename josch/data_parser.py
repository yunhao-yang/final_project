import pandas as pd
import copy
from template_container import *


class DataParser:
    # class to parse job/node to internal data structures
    def __init__(self, data_loader_class, date):
        self._data_loader_class = data_loader_class
        self._date = date
        self.parse_data()

    def parse_data(self):
        date = self._date
        loader = self._data_loader_class()
        
        tlp_nodes_table = loader.read_table('tpl_nodes')
        tlp_jobs_table = loader.read_table('tpl_jobs')
        environ_table = loader.read_table('environs')
        tlp_node_deps_table = loader.read_table('tpl_node_deps')
        
        # read in environment variables
        environ_map = {}
        environ_map['$DATE'] = date
        for i in environ_table.iterrows():
            _, (var, value) = i
            environ_map['${}'.format(var)] = value
        
        # read in template jobs
        tpljob_map = {}
        for i in tlp_jobs_table.iterrows():
            _, (job_name, job_desc) = i
            tpl_job = Job(job_name=job_name)
            tpljob_map[job_name] = tpl_job

        # read in template nodes
        tplnode_map = {}
        for i in tlp_nodes_table.iterrows():
            _, (node_id, node_type, job_name, 
                node_name, exec_command, signoff_time) = i
            if pd.isna(exec_command):
                exec_command = ''
            date = 0
            tpl_node = Node(node_id=node_id,
                            node_type=node_type, 
                            job_name=job_name, 
                            node_name=node_name, 
                            exec_command=exec_command, 
                            signoff_time=signoff_time,
                            date=date)
            tplnode_map[(node_id, date)] = tpl_node
            # add node into jobs
            if job_name not in tpljob_map:
                raise ValueError('Job {} not in template_jobs'.format(job_name))
            tpl_job = tpljob_map[job_name]
            tpl_job.add_node(tpl_node)
    
        tplnodedep_map = {}
        for i in tlp_node_deps_table.iterrows():
            _, (p_node_id, p_date, c_node_id, c_date) = i
            p_tpl_node = self.get_or_insert_node(tplnode_map, p_node_id, p_date) 
            c_tpl_node = self.get_or_insert_node(tplnode_map, c_node_id, c_date) 
            p_tpl_job = tpljob_map[p_tpl_node._job_name]
            p_tpl_job.add_edge(p_tpl_node, c_tpl_node)
            # in case the child and parent node are not in the same job
            if c_tpl_node._job_name != p_tpl_node._job_name:
                c_tpl_job = tpljob_map[c_tpl_node._job_name]
                c_tpl_job.add_edge(p_tpl_node, c_tpl_node)

        self._tpljob_map = tpljob_map
        self._environ_map = environ_map
        self._c_tpl_job = c_tpl_job
        self._p_tpl_job = p_tpl_job
        
        
    # read in dependency table
    def get_or_insert_node(self, tplnode_map, node_id, date):
        tpl_node = tplnode_map.get((node_id, date), None)
        if tpl_node is None:
            tpl_node = tplnode_map.get((node_id, 0), None)
            if tpl_node is None:
                raise ValueError('node_id {} not in template_nodes_table'.format(node_id))
            tpl_node = copy.deepcopy(tpl_node)
            tpl_node._date = date
            tplnode_map[(node_id, date)] = tpl_node
        return tpl_node
    
    def get_tpl_jobs(self):
        return list(self._tpljob_map.values())