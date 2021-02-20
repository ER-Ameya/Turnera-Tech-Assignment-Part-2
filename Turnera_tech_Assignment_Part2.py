import sys
import seaborn as sns
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from sqlalchemy import create_engine
import mysql.connector as msql
from mysql.connector import Error

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDialog, QDialogButtonBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets


import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import matplotlib.pyplot as plt

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=15, height=14, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Graphs !")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("TO generate graph click ok")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        
    def accept(self):
        window().generate_graph()
        print("cool")

class window(QMainWindow):

    def __init__(self):
        super(window, self).__init__()
        self.setWindowTitle('Generate Graph')
        
        button = QPushButton("Press me for graphs")
        button.clicked.connect(self.button_clicked)
        
        self.setCentralWidget(button)
        
    def button_clicked(self, s):
        print("click", s)

        dlg = CustomDialog()  
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")


    def generate_graph(self):

        
        sc = MplCanvas(self, width=15, height=14, dpi=100)
        st = MplCanvas(self, width=15, height=14, dpi=100)
        dataframe = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/college-majors/recent-grads.csv")
        engine = create_engine('mysql://root:Apple@123@localhost/turnera') # format: mysql://user:pass@host/db
        dataframe.to_sql('college',chunksize=20,index = False, con=engine,if_exists='replace')

        #To retrive data from MySql
        dbConnection = engine.connect()
        dfs = pd.read_sql("select * from turnera.college", dbConnection)

        # print(frame.head())
        dbConnection.close()
        

        #Extracting 20 rows
        df = dfs.iloc[0:20]

        # Line Graph Rank Vs Full time year round
        fig, ax = plt.subplots(figsize =(16, 9)) 
        plt.plot(df['Rank'], df['Full_time_year_round'], color='red', marker='o')
        plt.title('Rank Vs Full_time_year_round', fontsize=14)
        plt.xlabel('Rank', fontsize=14)
        plt.ylabel('Full_time_year_round', fontsize=14)
        plt.grid(True)
        plt.show()

        # Line Graph Part_time Vs Unemployment_rate
        fig, ax = plt.subplots(figsize =(16, 9)) 
        plt.plot(df['Part_time'], df['Unemployment_rate'], color='Blue', marker='o')
        plt.title('Part_time Vs Unemployment_rate', fontsize=14)
        plt.xlabel('Part_time', fontsize=14)
        plt.ylabel('Unemployment_rate', fontsize=14)
        plt.grid(True)
        plt.show()

        df[['Rank','Full_time_year_round']].plot(ax=sc.axes)
        df[['Part_time','Unemployment_rate']].plot(ax=st.axes)

        # bar graph between college rank and College jobs and Non College jobs.
        y = np.random.rand(10,3)
        y[:,0]= np.arange(10)

        ax = df.plot(x="Rank", y="College_jobs", kind="bar")
        df.plot(x="Rank", y="Non_college_jobs", kind="bar", ax=ax, color="C2",figsize =(16, 9))


        plt.xticks(rotation=90)
        plt.title('Bar Plot', fontsize=14)
        plt.xlabel('Rank', fontsize=14)
        plt.ylabel('College Jobs vs Non College Jobs', fontsize=14)
        plt.grid(True) 

        toolbar = NavigationToolbar(sc,st, self)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)
        layout.addWidget(st)
        
         # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()
        plt.show()


app = QApplication(sys.argv)
Gui = window()
Gui.show()
sys.exit(app.exec_())

