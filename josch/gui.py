import tkinter as tk 
from tkinter import *
import datetime

class GUI:
    """
    job to create a client GUI
    """

    def __init__(self, dataloader_class):
        self._loader = dataloader_class()
        self._win = Tk()
        #to specify size of window. 
        self._win.geometry("250x170")

    def node_view(self, r):
        """

        :param r: specific job
        :return: the graphical view of the job
        """
        # To Create a text widget and specify size. 
        # TO Create label 
        win = self._win
        dt = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        date = r.loc['date']
        node_id = r.loc['node_id']
        job_name = r.loc['job_name']
        node_name = r.loc['node_name']
        state = r.loc['state']
        node_type = r.loc['node_type']
        
        if state == 'failed':
            color = 'red'
        else:
            color = 'black'

        message = '\n{} {}\n'.format(node_id, node_name)
        message += 'State: {}\n\n'.format(state)
        message += '{} {}\n'.format(date, job_name)
        message += '{}\n'.format(dt)
        l = Label(win, text = message, fg=color) 

        l.config(font =("Courier", 14)) 
        l.pack() 

        # Create a button for the next text. 
        if node_type == 'S':
            b1 = Button(win, text = "Signoff", command=self.handle_signoff) 
            b1.pack()
        else:
            b1 = Button(win, text = "Mark Success", command=self.handle_success) 
            b2 = Button(win, text = "Retry", command=self.handle_retry) 

            b1.pack() 
            b2.pack() 
            
        tk.mainloop()

    
    def handle_signoff(self):
        self._loader.handle_signoff()
        
    def handle_retry(self):
        self._loader.handle_retry()
        
    def handle_success(self):
        self._loader.handle_success()
    