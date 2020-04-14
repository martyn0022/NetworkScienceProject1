from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from Science import GetConferenceInDegreeStrength, GetNetworkEffect
from Science import Networks

#Defining the Tkinter Window
root = Tk()
root.title("Interface")
root.geometry("300x230")

#to call from Science.py
test1= Networks()

#to program "Show" button
def show():
    if option_networkgraph.get() == "Conferences":
        test2= GetConferenceInDegreeStrength(test1.GetConferenceGraph())
    else:
        test2= GetNetworkEffect(test1.GetAuthorGraph())
    test2.show()
    
#to update the options based on previous options
def update_next(*args):
    if option_networkgraph.get() == "Authors":
        option_measure.set("Degree Distribution")
        dropdown_measure = OptionMenu(root, option_measure, *measures)
    elif option_networkgraph.get() == "Institutions":
        option_measure.set("Publication Distribution")
        dropdown_measure = OptionMenu(root, option_measure, *measures1)
    elif option_networkgraph.get() == "Conferences":
        option_measure.set("Degree Distribution")
        dropdown_measure = OptionMenu(root, option_measure, *measures2)
    dropdown_measure.place(x=100,y=55)
    
#Labelling
networkgraph_label = Label(root, text = "Network Graph: ")
networkgraph_label.place(x=10,y=20)

measures_label = Label(root,text = "Questions: ")
measures_label.place(x=10,y=60)

startyear_label = Label(root, text = "Start year: ")
startyear_label.place(x=10,y=100)

endyear_label = Label(root, text = "End year: ")
endyear_label.place(x=10, y=140)

#options
option_networkgraph = StringVar()
option_measure = StringVar()
option_startyear = StringVar()
option_endyear = StringVar()

#setting defaults
option_networkgraph.set("Authors")
option_measure.set("Degree Distribution")

#options for networkgraphs
networkgraphs = [
    "Authors",
    "Institutions",
    "Conferences"
    ]

#options for questions, will be changed accordingly
measures = [
    "Degree Distribution",
    "Publication Distribution"
    ]
measures1 = [
    "Publication Distribution",
    "Example"
    ]
measures2 = [
    "Degree Distribution",
    "Example"
    ]

#Displays network dropdown menu
dropdown_networkgraph = OptionMenu(root, option_networkgraph, *networkgraphs,command = update_next)
dropdown_networkgraph.place(x=100,y=15)

#Displayes question dropdown menu
dropdown_measure = OptionMenu(root, option_measure, *measures)
dropdown_measure.place(x=100,y=55)

#Displays entrybox for start year
entrybox_start = Entry(root, textvariable= option_startyear, width =10)
entrybox_start.place(x=102,y=102)

#Displays entrybox for end year
entrybox_end = Entry(root, textvariable= option_endyear, width =10)
entrybox_end.place(x=102,y=142)

#Button to confirm and show, defined at the top
btnConfirm = Button(root, text="Show Graph", command=show)
btnConfirm.place(x=110,y=180)



root.mainloop()


    
