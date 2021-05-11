
class Job:
    # class to represent a template job
    def __init__(self, job_name):
        self._job_name = job_name
        self._edges = []
        self._nodes = set()
        self._node_children = dict()
    
    def add_node(self, node):
        if node in self._nodes:
            raise ValueError('node {} already in job {}'.format(node._node_id, self._job_name))
        self._nodes.add(node)
    
    def add_edge(self, p_node, c_node):
        edge = (p_node, c_node)
        if edge in self._edges:
            raise ValueError('Duplicated edge from {} to {}'.format(p_node._node_id, c_node._node_id))
            
        children = self._node_children.get(p_node, None)
        if not children:
            children = []
        children.append(c_node)
        self._node_children[p_node] = children
        self._edges.append(edge)
    
    def get_nodes(self):
        pass
    
    def __repr__(self):
        s = 'Job {} ({})'.format(self._job_name, len(self._nodes))
        return s
    
    def __eq__(self, other):
        return self._job_name == other._job_name

    
class Node:
    # class to represent a template node
    def __init__(self, node_id, node_type, job_name, 
                 node_name, exec_command, signoff_time, date):
        self._job_name = job_name
        self._node_name = node_name
        self._node_id = node_id
        self._node_type = node_type
        self._exec_command = exec_command
        self._signoff_time = signoff_time
        self._date = date
        
    def __repr__(self):
        s = 'Node {} {} {} {}'.format(self._node_type, self._node_id, self._node_name, self._date)
        return s
    
    def __eq__(self, other):
        return ((self._node_id == other._node_id)
                & (self._date == other._date))
    
    def __lt__(self, other):
        if self._date < other._date:
            return True
        elif self._date > other._date:
            return False
        else:
            if self._node_id < other._node_id:
                return True
            else:
                return False
        return False
    
    
    def __hash__(self):
        return hash('{} {}'.format(self._node_id, self._date))
