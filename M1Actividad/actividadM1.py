# Equipo 4
# Ares Ortiz Botello A01747848
# Rosa Itzel Figueroa Rosas A01748086

import mesa
from mesa import Model, Agent
import numpy as np
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.space import SingleGrid     

class RoomModel(Model):
    def __init__(self, M, N):
        self.num_agents = M * N
        self.grid = SingleGrid(M, N, True)
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True
        
        vacuum_agent = VacuumCleaner(1, self)
        self.grid.place_agent(vacuum_agent, (1,1))
        self.schedule.add(vacuum_agent)
        
        for i, (x,y) in self.grid.coord_iter():
            if (x,y) != (1,1):
                dirty_cell = TrashAgent((x,y), self)
                self.grid.place_agent(dirty_cell, (x,y))
                self.schedule.add(dirty_cell)
    
    def step(self):
        self.schedule.step()
        
class VacuumCleaner(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = np.random.choice([1,1])
        
    def step(self):
        x, y = self.pos
            
        if self.model.grid[x][y].live == 1:
            self.model.grid[x][y].live = 0
        else:
            possible_moves = self.model.grid.get_neighbors(
                self.pos,
                moore = True,
                include_center = False)
            
            move_positions = self.random.choice(possible_moves)
            self.model.grid.move_agent(self, move_positions)
        
        self.nex_state = None  

class TrashAgent(Agent):
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = np.random.choice([0,1])
        self.next_state = None

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