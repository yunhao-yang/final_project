
class DAG:
    """
    class to determine node dependencies
    """
    def __init__(self, dag):
        self._dag = dag
    
    def topological_sort(self):
        """

        :return: the topologically sorted dag
        """
        dag = self._dag
        
        dfs_nodes = []
        visited_nodes = set()
        child_edges = []
        parent_edges = []
        nodes = []
        name_dict = {}
        # Inner function to perform Depth-First-Search
        def dfs(node, level):
            if node in visited_nodes:
                for i, l in enumerate(dfs_nodes):
                    if l[0] == node:
                        if l[1] < level:
                            dfs_nodes[i] = (node, level)
                        break
                return
            visited_nodes.add(node)
            children = child_edges.get(node, [])
            for child in children:
                dfs(child, level+1)
            dfs_nodes.append((node, level))
        
        # Find isolated nodes
        root_nodes = [ node for node in nodes if len(parent_edges.get(node,[])) == 0]
        for node in root_nodes:
            if node in visited_nodes:
                continue
            dfs(node, 0)
        
        # calculate dependencies and put into list
        depth_dict = {}
        for group_name, depth in dfs_nodes:
            if depth not in depth_dict:
                depth_dict[depth] = []
            depth_dict[depth].append(group_name)

        depth_res = []
        for depth in range(len(depth_dict)):
            group_names = depth_dict[depth]
            dag_exp_list = [ name_dict[d][0] for d in group_names]
            dag_opt_dict_list = [ name_dict[d][1] for d in group_names]
            depth_res.append([group_names, dag_exp_list, dag_opt_dict_list])

        return depth_res