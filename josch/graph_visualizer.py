from graphviz import Digraph

class Visualizer:
    # A class to visualize dag graph
    def __init__(self, tmpjob):
        self._tmpjob = tmpjob
    
    def visualize(self):
        tmpjob = self._tmpjob
        
        dot = Digraph(comment=tmpjob._job_name)
        edge_nodes = set([ n for nt in tmpjob._edges for n in nt ])
        dag_nodes = edge_nodes | tmpjob._nodes
        dag_nodes = sorted(list(dag_nodes))
        
        # set different node types
        for node in dag_nodes:
            disp = '{}\n{}\n{}'.format(node._node_id, node._job_name, node._node_name)
            style = 'solid'
            shape = 'rectangle'
            color = 'black'
            if node._job_name != tmpjob._job_name:
                style = 'dashed'
            if node._node_type == 'S':
                shape = 'ellipse'
                disp = '[S] {}\n{}'.format(disp, node._signoff_time)
            elif node._node_type == 'R':
                shape = 'component'
                disp = '[R] {}'.format(disp)
                color = 'red'
            elif node._node_type == 'L':
                shape = 'note'
                disp = '[L] {}'.format(disp)

            if node._date == -1:
                disp = '{-1} ' + disp
            dot.node(str(node._node_id), disp, style=style, 
                     shape=shape, color=color)
        for p_node, c_node in tmpjob._edges:
            dot.edge(str(p_node._node_id), str(c_node._node_id))
        
        return dot