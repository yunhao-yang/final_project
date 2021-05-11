import datetime as dt
import copy
import pandas as pd


def prev_day(date, days):
    adate = dt.datetime.strptime(date, '%Y-%m-%d')
    adate += dt.timedelta(days=days)
    return dt.datetime.strftime(adate, '%Y-%m-%d')


def schedule_node(tpl_node, date):
    sch_node = copy.deepcopy(tpl_node)
    sch_node._date = prev_day(date, int(sch_node._date))
    return sch_node


def schedule_job(tmp_job, date):
    sch_job = copy.deepcopy(tmp_job)
    sch_job._nodes = {schedule_node(x, date) for x in sch_job._nodes}
    sch_job._edges = [(schedule_node(x[0], date), schedule_node(x[1], date)) for x in sch_job._edges]
    sch_job._node_children = dict([[schedule_node(k, date), [schedule_node(v, date) for v in vs]]
                                   for k, vs in sch_job._node_children.items()])
    return sch_job


def sch_exec_command(exec_command, environ_map):
    exec_command = ' '.join([environ_map.get(x, x) for x in exec_command.split()])
    if '$' in exec_command:
        raise ValueError('Unknown environment variable in {}'.format(exec_command))
    return exec_command


class Scheduler:
    # class to schedule template jobs/nodes
    def __init__(self, data_parser):
        self._date = data_parser._date
        self._tpljob_map = data_parser._tpljob_map
        self._environ_map = data_parser._environ_map

    def schedule(self):
        tpljob_map = self._tpljob_map
        date = self._date
        environ_map = self._environ_map

        # create scheduled jobs
        schjob_map = {}
        for tmp_job in tpljob_map.values():
            sch_job = schedule_job(tmp_job, date)
            schjob_map[sch_job._job_name] = sch_job

        # create scheduled nodes
        edge_nodes = set([n for nt in sch_job._edges for n in nt])
        all_nodes = edge_nodes | sch_job._nodes
        sch_nodes_table = []
        for sch_node in all_nodes:
            attr_list = ['date', 'node_id', 'node_type', 'job_name', 'node_name', 'exec_command', 'signoff_time']
            node_row = pd.DataFrame([(attr, getattr(sch_node, '_{}'.format(attr))) for attr in attr_list])
            node_row = node_row.set_index(0)
            node_row.loc['state'] = 'Pending'
            node_row.loc['exec_command'] = sch_exec_command(node_row.loc['exec_command'].values[0], environ_map)
            sch_nodes_table.append(node_row)
        sch_nodes_table = pd.concat(sch_nodes_table, axis=1).T

        # create scheduled node dependencies
        sch_node_deps_table = []
        for p_sch_node, c_sch_node in sch_job._edges:
            sch_node_dep = pd.Series([p_sch_node._node_id, p_sch_node._date,
                                      c_sch_node._node_id, c_sch_node._date],
                                     index=['p_node_id', 'p_date', 'c_node_id', 'c_date'])
            sch_node_deps_table.append(sch_node_dep)
        sch_node_deps_table = pd.concat(sch_node_deps_table, axis=1).T

        self._sch_nodes_table = sch_nodes_table
        self._sch_node_deps_table = sch_node_deps_table

    def get_sch_node_table(self):
        return self._sch_nodes_table

    def get_sch_node_deps_table(self):
        return self._sch_node_deps_table
