import tkinter as Tk
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from Faculty import *
from Faculty import Networks

def openDF(df):
    df_window = Tk()
    df_window.title("Findings")
    cols = list(df.columns)
    tree = ttk.Treeview(df_window)
    tree.pack()
    tree["columns"] = cols
    for i in cols:
        tree.column(i, anchor="w")
        tree.heading(i, text=i, anchor='w')

    for index, row in df.iterrows():
        tree.insert("",0,text=index,values=list(row))
    df_window.mainloop()

def drawNetworkx(figure):
    Netw = Tk()
    Netw.wm_title("Network")
    #f = plt.Figure(figsize=(5,4), dpi=100)
    #a = f.add_subplot(111)
    #a.plot([1,2,3,4,5],[3,2,1,3,4])
    #nx.draw_kamada_kawai(figure,with_labels=True, ax=a)
    canvas = FigureCanvasTkAgg(figure, master=Netw)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    #toolbar = NavigationToolbar2Tk(canvas, Netw)
    #toolbar.update()
    #canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    Netw.mainloop()


def openGUI():
    #Defining the Tkinter Window
    root = Tk()
    root.title("CZ4071 Faculty Visualiser")
    root.geometry("450x230")

    #to call from Science.py
    data = Networks()

    #to program "Show" button
    def show(btn):
        btn.config(state = 'disabled')
        isGraph = 1
        if option_network.get() == "SCSE":
                if option_graph.get() == "Degree Distribution":
                    graph,no,need = GetScseDegreeDistribution(data.GetScseNetwork())

                elif option_graph.get() == "Publication Distribution":
                    graph = GetScsePublicationDistribution(data.GetScseNetwork())

                elif option_graph.get() == "Reputation Distribution":
                    graph,no,need = GetScseReputationDistribution(data.GetScseNetwork())

                elif option_graph.get() == "Reputation Degree":
                    graph = GetAuthorReputationDegree(data.GetScseNetwork())

                elif option_graph.get() == "Maximum Degree Change":
                    graph = GetAuthorMaximumDegreeChange(data.GetScseNetwork())

        elif option_network.get() == "Coauthor":
                if option_graph.get() == "Degree Distribution":
                    graph ,no,need = GetScseDegreeDistribution(data.GetCoauthorNetwork())


        elif option_network.get() == "Faculty Comparisons":
            isGraph =0
            if option_factor.get() == "position":
                filter = 'position'
                if option_graph.get() == "Professor":
                    rank1 = "Professor"
                elif option_graph.get() == "Associate Professor":
                    rank1 = "Associate Professor"
                elif option_graph.get() == "Assistant Professor":
                    rank1 = "Assistant Professor"
                elif option_graph.get() == "Lecturer":
                    rank1 = "Lecturer"


            elif option_factor.get() == "management":
                filter = 'position'
            elif option_factor.get() == "area":
                filter = 'area'
            isGraph = 0
            graph = compareFiltered(data.GetScseNetwork(), filter,rank1)


        btn.config(state = 'normal')
        if isGraph:
            graph.show()
        else:
            drawNetworkx(graph)




    #to update the options based on previous options
    def update_next(*args):
        if option_network.get() == "SCSE":
            option_graph.set("Degree Distribution")
            dropdown_graph = OptionMenu(root, option_graph, *measures)
            dropdown_graph.place(x=100,y=95)

            if option_factor.get() != "Not Applicable":
                option_factor.set("Not Applicable")
                dropdown_factor = OptionMenu(root, option_factor,"Not Applicable")
                dropdown_factor.place(x=100,y=55)
        elif option_network.get() == "Coauthor":
            option_graph.set("Degree Distribution")
            dropdown_graph = OptionMenu(root, option_graph, *measures1)
            dropdown_graph.place(x=100,y=95)

            if option_factor.get() != "Not Applicable":
                option_factor.set("Not Applicable")
                dropdown_factor = OptionMenu(root, option_factor,"Not Applicable")
                dropdown_factor.place(x=100,y=55)
        elif option_network.get() == "Faculty Comparisons":
            option_factor.set("management")
            dropdown_factor = OptionMenu(root, option_factor, *factor,command = update)
            dropdown_factor.place(x=100,y=55)
            update()


    def update(*args):
        if option_factor.get() == "position":
            option_graph.set("Professor")
            dropdown_graph = OptionMenu(root, option_graph, *measures2)
            dropdown_graph.place(x=100,y=95)

        elif option_factor.get() == "Location":
            option_graph.set("Role in success of a Data Scientist")
            dropdown_graph = OptionMenu(root, option_graph, *measures3)
            dropdown_graph.place(x=100,y=95)


    #Labelling
    networkgraph_label = Label(root, text = "Network: ")
    networkgraph_label.place(x=10,y=20)

    measures_label = Label(root,text = "Graph/Findings: ")
    measures_label.place(x=10,y=100)

    factor_label = Label(root, text = "Factor: ")
    factor_label.place(x=10,y=60)


    #options
    option_network = StringVar()
    option_graph = StringVar()
    option_factor = StringVar()
    option_factor2 = StringVar

    #setting defaults
    option_network.set("SCSE")
    option_graph.set("Degree Distribution")
    option_factor.set("Not Applicable")

    #options for networkgraphs
    network = [
        "SCSE",
        "Coauthor",
        "Faculty Comparisons"
        ]

    #options for factors
    factor = [
        "position",
        "management",
        "area"
        ]

    #options for questions, will be changed accordingly
    measures = [
        "Degree Distribution",
        "Publication Distribution",
        "Reputation Distribution",
        "Reputation Degree",
        "Maximum Degree Change"
        ]
    measures1 = [
        "Degree Distribution"
        ]
    measures2 = [
        "Professor",
        "Associate Professor",
        "Assistant Professor",
        "Lecturer"
        ]
    measures3 = [
        "Role in success of a Data Scientist"
        ]

    #Displays network dropdown menu
    dropdown_network = OptionMenu(root, option_network, *network,command = update_next)
    dropdown_network.place(x=100,y=15)

    #Displayes question dropdown menu
    dropdown_graph = OptionMenu(root, option_graph, *measures)
    dropdown_graph.place(x=100,y=95)

    #Displays factor dropdown menu
    dropdown_factor = OptionMenu(root, option_factor,"Not Applicable")
    dropdown_factor.place(x=100,y=55)

    #Displays factor dropdown menu
    dropdown_factor2 = OptionMenu(root, option_factor2,"Not Applicable")
    dropdown_factor2.place(x=300,y=55)

    #Button to confirm and show, defined at the top
    btnConfirm = Button(root, text="Show Graph/Findings", command= lambda : show(btnConfirm))
    btnConfirm.place(x=180,y=180)



    root.mainloop()
