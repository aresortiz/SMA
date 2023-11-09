# Equipo 4
# Ares Ortiz Botello A01747848
# Rosa Itzel Figueroa Rosas A01748086

import random
import mesa
from mesa import Model, Agent
import numpy as np
from mesa.time import SimultaneousActivation
from time import time
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.space import MultiGrid


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
        possible_moves = [(x, y) for (x, y) in next_moves if (x - self.pos[0]) <= 1 and (y - self.pos[1]) <= 1]
        if possible_moves:
            new_position = self.random.choice(possible_moves)
            self.model.grid.move_agent(self, new_position)
                
        cell = self.model.grid.get_cell_list_contents(new_position)
        for value in cell:
            if type(value) is TrashAgent:
                print("Pise basura")
                self.model.grid.remove_agent(value)

    def step(self):
        self.random_move()


class TrashAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = np.random.choice([0, 1])
        self.state = "Dirty"


class RoomModel(Model):
    def __init__(self, M, N, agentes):
        self.num_agents = agentes
        self.grid = MultiGrid(M, N, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.start_time = time()
        self.end_time = 0


        for i in range(agentes):
            agent = VacuumCleaner(i, self)
            self.grid.place_agent(agent, (0, 0))
            self.schedule.add(agent)

        for i, (x, y) in self.grid.coord_iter():
            if (x, y) != (0, 0):
                dirty_cell = TrashAgent((x, y), self)
                self.grid.place_agent(dirty_cell, (x, y))
                self.schedule.add(dirty_cell)

    def step(self):
        self.schedule.step()
