# Pareja 4
# Actividad 1 - Agentes de limpieza reactivos 
# Ares Ortiz Botello A01747848
# Rosa Itzel Figueroa Rosas A01748086

import random
import mesa
from mesa import Model, Agent
import numpy as np
from mesa.time import SimultaneousActivation
from time import time
#from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.space import MultiGrid

# global clean_cells 
# clean_cells = 0

class VacuumCleaner(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = 1
        # self.moore = True
        self.pos = (1, 1)

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,
                include_center=False
                )
        possible_moves = [(x, y) for (x, y) in next_moves if abs(x - self.pos[0]) <= 1 and abs(y - self.pos[1]) <= 1]
        if possible_moves:
            new_position = self.random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)
                
        cell = self.model.grid.get_cell_list_contents(new_position)
        for value in cell:
            if type(value) is TrashAgent:
                if value.live == 1:
                    self.model.grid.remove_agent(value)
                    self.model.clean_cells += 1
                

    def step(self):
        self.random_move()


class TrashAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = np.random.choice([0, 1])
        self.state = "Dirty"


class RoomModel(Model):
    def __init__(self, M, N, agents, max_time):
        self.M = M
        self.N = N
        self.max_time = max_time
        self.num_agents = agents
        self.grid = MultiGrid(M, N, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.start_time = time()
        self.end_time = 0
        self.clean_cells = 0
        self.dirty_cells = 0

        for i in range(agents):
            agent = VacuumCleaner(i, self)
            self.grid.place_agent(agent, (1, 1))
            self.schedule.add(agent)

        for i, (x, y) in self.grid.coord_iter():
            if (x, y) != (1, 1):
                dirty_cell = TrashAgent((x, y), self)
                self.grid.place_agent(dirty_cell, (x, y))
                self.schedule.add(dirty_cell)
                if dirty_cell.live == 1:
                    self.dirty_cells += 1
        
                
        print("SUCIAS: ", self.dirty_cells)
        print("M:", self.M)
        print("N: ", self.N)

    def step(self):
        self.schedule.step()
        self.end_time = time()
        elapsed_time = self.end_time - self.start_time
        
        if elapsed_time >= self.max_time:
            print(f'Total elapsed time {elapsed_time}')
            print(f'Porcentage cleaned: {(self.clean_cells*100) / self.dirty_cells}%')
            print(f'Porcentage initially dirty: {(self.dirty_cells*100) / (self.M * self.N)}%')
            self.running = False