import pytest
import Faculty
import networkx
import gui
import matplotlib.pyplot as plt


data = Faculty.Networks()

def test_getScseNetwork():
    network = data.GetScseNetwork()
    assert type(network) == networkx.classes.graph.Graph

def test_compareFiltered_valid():
    plot = Faculty.compareFiltered(data.GetScseNetwork(), "management", "Y", "N")
    assert plot is not None
