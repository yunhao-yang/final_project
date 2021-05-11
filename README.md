# Documentation for JOSCH

### Project Proposal

In this project, I will develop from scratch a light-weight interactive job scheduler (JOSCH for short). Similar to Airflow, JOSCH is a workflow management platform, which enables users and programs to schedule, monitor, and edit routine tasks. The advantage of JOSCH compared to Airflow is that it’s more light-weighted and user customizable. We also have complete control over the system since it’s developed from scratch, which makes it easier to add additional functionality or change the underlying logic in the future. The project will cover the following major topics.

1. Workflows. (These are typical workflows and I will not elaborate on them)
1.1. Version Control (Git)
1.2. Cookiecutter
1.3. Reproducable Environment (pipenv)

2. Data Structures and Algorithms
2.1. Model-View-Controller Design Pattern. The project will incorporate the MVC design pattern: Model being the underlying graph nodes stored in the database, View being the user GUI, Controller being the scheduling and editing of the workflow. 

2.2. Inheritance and Encapsulation. The MVC design pattern explicitly utilizes inheritance and encapsulation to segregate the program into three parts. Besides that, I plan to use OOPS through out the project.

2.3. Graph (DAG) Construction, Algorithms and Visualization. A Directed Acyclic Graph is an excellent choice for modeling the tasks and their dependencies. The vertices of the graph will be the tasks, and edges will be the dependencies among the tasks. I will implement various graph algorithms as well, including cycle detection, topological sort, graph traversal, etc.

2.4. Finite State Machine. There will be different states associated with each task, including Pending, Running, Succeeded, Failed, Review, Signoff, etc. The collection and the relationships of the states form a finite state machine, and I will model them as such.

2.5. Parallel Computing. Considering the node status may be changed simultaneously by different users and programs, it’s crucial to solve the race conditions and dead locks in the project. I plan to implement a semaphore to deal with this issue. 

3. Database (PostgreSQL)
3.1. Design. There will be Node tables and Node-dependency tables in the database. The Node table contains the information about each task, including task_id, task_name, exec_command, status, etc. The node dependency table contains the dependencies among tasks, i.e. parent_task_id, child_task_id. 

3.2. Auditing. I will have an auditing table for each database table, containing the sequence of logs of the changes to each table.

3.3. Python Interface. I will develop (or use 3rd party lib) to connect python code to database.

4. GUI
4.1. Interactive GUI using Tkinter. I will implement a GUI to let user interactively monitor and control the nodes. Each task has its own window, and the window will pop up if the node status is Failed, Review or Signoff (nodes that needs human intervention). There will be a text-box and click-bar in the window to let user change the status of the corresponding node. 

4.2. Graphic Representations of Graphs. I will also draw the graphs to show the tasks and task dependencies to be more human-friendly. 

4.3. Remote Control through Network and X11. In case there are multiple users located on different client machines, each client machine which runs the monitor GUI will listen to a central server though network and display the GUI via X11.

### Implementation Details:

Here are some visualizations associated with the project, which will be explained in detail.

Example Node dependencies in a Job:

![image](https://user-images.githubusercontent.com/78084449/117831031-c9823100-b2a6-11eb-9b68-05e1db269d43.png)

Clients' GUI to change the node states: 

![image](https://user-images.githubusercontent.com/78084449/117830968-b8d1bb00-b2a6-11eb-83df-fe9353eae7df.png)


File descriptions:

#### data_loader.py
DataLoader is an abstract class to load template jobs/nodes/dependencies from file system.

There are 4 main tables for the users to pre-occupy:

environs: table that contains environment variables

tpl_jobs: template jobs which is a collection of template nodes. Columns include job_name (Primary Key) and job_desc.

tpl_nodes: template nodes which represent a 'task' to run. Columns include 

- node_id: primary id of node
- node_name: descriptive name of node
- node_type: types of node, including SignOff(S), LongRunning(L), Normal(N), Review(R)
- exec_command: the execution command associated with the node. e.g. /usr/bin/python script.py --date 2019-04-04 --arg test
- signoff_time: time for signing off the node
- job_name: job that contains the node

tpl_node_deps: template node dependencies to keep track of ancestors and predecessors

DB_DataLoader is an implementation of DataLoader, which uses sqlalchemy as the ORM to connect to database.

CSV_DataLoader is an implementation, which stores the data in csv form. Example of tables are shown in tables/ folder:

environs.csv:

|var|value|
| ----------- | ----------- |
|PYTHON|/Users/yunhaoyang/opt/anaconda3/bin/python

tpl_jobs.csv:

|job_name|job_desc|
| ----------- | ----------- |
|Eod|Eod Jobs
|Sod|Sod Jobs
|SodServer|Sod Server Jobs

tpl_nodes.csv:

|node_id|node_type|job_name|node_name|exec_command|signoff_time|
| ----- | ------- | ------ | ------- | ---------- | -----------|
900000|S|Eod|Eod_Signoff| |15:30:00
100000|S|Sod|Sod_Signoff| |06:30:00
100100|L|SodServer|SodServer_RtPrice|$PYTHON rt_price_server.py --date $DATE|
100110|L|SodServer|SodServer_EodPrice|$PYTHON eod_price_server.py --date $DATE|
100120|N|SodServer|SodServer_ProdFeature|$PYTHON prod_feature.py --date $DATE|
100130|R|SodServer|SodServer_CheckStatus|$PYTHON check_status.py --date $DATE|

tpl_node_deps.csv:

|p_node_id|p_date|c_node_id|c_date
| ----- | ------- | ------ | ---- |
900000|-1|100000|0
900000|-1|100100|0
100000|0|100100|0
100000|0|100110|0
100110|0|100120|0
100120|0|100130|0

#### template_container.py

Job: a class to represent a template job. It contains attributes of the job, as well as the nodes and 
dependencies contained in the job. Nodes are represented as (nodes), dependencies are represented as (edges).

Node: a class to represent a template node. It contains attributes of the node.


#### data_parser.py

DataParser: a class to parse data from DB or CSV to internal data structures (Job/Node/NodeDep). 

#### dag.py

DAG: a representation of a Directed Acyclical Graph, and a function topological_sort to sort the nodes 
based on the dependency graph.

#### scheduler.py

Scheduler: a class to schedule template jobs/nodes/deps to daily scheduled jobs/nodes/deps. For each day,
the scheduled containers are independent of those from different days.


#### graph_visualizer.py

Visualizer: A class that uses graphviz package to visualize nodes and their dependencies in a job. 
Different types of nodes are associated with different styles in the graph view. For example, [S], [L], or [R] 
represents type of the node. Dashed circle represents nodes outside of the job, but has dependencies with the nodes
within the job. Red means the node is a review node, which needs close attention. Each node also includes
job_name, node_id, node_type, node_name, which is informative to human.

![image](https://user-images.githubusercontent.com/78084449/117831031-c9823100-b2a6-11eb-9b68-05e1db269d43.png)


#### gui.py

GUI: a class that uses tkinter to implement a client's GUI to interact with the server.
When a node is in Signoff, Fail or Review state, the GUI will pop up on client side to get attention.
The client can either push the node to success or retry(pending) state, depends on what she wants to do.

There are three types of windows that are slightly different. The left GUI is a Signoff node, where the only
button is to signoff the node. The middle GUI is a failed node (colored red to get user attention), and the 
buttons are "Mark Success" and "Retry". The right GUI is a review node.

In this case, users can either directly change the 'state' column in the database, or use the GUI to
quickly change the state of nodes.

![image](https://user-images.githubusercontent.com/78084449/117830968-b8d1bb00-b2a6-11eb-83df-fe9353eae7df.png)

