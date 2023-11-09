# Equipo 4
# Ares Ortiz Botello A01747848
# Rosa Itzel Figueroa Rosas A01748086

import random
import mesa
from mesa import Model, Agent
import numpy as np
from mesa.time import SimultaneousActivation
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
            self.pos, moore=True, include_center=True)
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0),
                          (1, 0), (1, -1), (-1, -1), (1, 1)]
        x, y = self.pos
        x2, y2 = random.choice(possible_moves)
        newX = x + x2
        newY = y + y2
        newPosition = (newX, newY)
        print(newPosition)
        cell = self.model.grid.get_cell_list_contents(newPosition)
        self.pos = newPosition
        self.model.grid.move_agent(self, newPosition)

    def step(self):
        self.random_move()


class TrashAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.live = np.random.choice([0, 1])
        self.next_state = None


class RoomModel(Model):
    def __init__(self, M, N):
        self.num_agents = M * N
        self.grid = MultiGrid(M, N, True)
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.running = True

        for i in range(15):
            agent = VacuumCleaner(i, self)
            self.grid.place_agent(agent, (1, 1))
            self.schedule.add(agent)

        for i, (x, y) in self.grid.coord_iter():
            if (x, y) != (1, 1):
                dirty_cell = TrashAgent((x, y), self)
                self.grid.place_agent(dirty_cell, (x, y))
                self.schedule.add(dirty_cell)

    def step(self):
        self.schedule.step()

        # possible_moves = []

        # for i in next_moves:
        #     possible_moves.append(i)
        #     moves

        # next_move = self.random.choice(next_moves)
        # # Now move:
        # self.model.grid.move_agent(self, next_move)

    # def step(self):
    #     x, y = self.pos

    #     # Si esta en inicio
    #     if self.model.grid[x][y].live == 1:
    #         self.pos = [2, 2]

    #     #     # self.model.grid[x][y].live = 0
    #     #      for neighbor in possible_moves:

    #     # else:
    #         possible_moves = self.model.grid.get_neighbors(
    #             self.pos,
    #             moore = True,
    #             include_center = False)

    #         print(possible_moves)

    #         move_positions = self.random.choice(possible_moves)
    #         self.model.grid.move_agent(self, move_positions)

    #     self.nex_state = None
