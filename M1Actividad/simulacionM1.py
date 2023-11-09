from actividadM1 import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    portrayal = {}
    if type(agent) is VacuumCleaner:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "purple",
                     "r": 0.7}
        
    if type(agent) is TrashAgent:
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 1,
                     "Color": "gray",
                     "r": 0.4}
        
        if agent.live == 0:
            portrayal["Color"] = "white"
    
    return portrayal

M = 28
N = 28
grid = CanvasGrid(agent_portrayal, M, N, 750, 750)
server = ModularServer(RoomModel, 
                       [grid],
                       "Room cleaning vacuums",
                       {"M":M, "N": N})
server.port = 8521
server.launch()