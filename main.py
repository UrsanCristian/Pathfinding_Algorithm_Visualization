import pygame
import sys
from tkinter import Tk, messagebox

width = 700
height = 700
rows = 35
columns = 35
cell_w = width // columns
cell_h = height // rows
grid = []
djikstra_queue = []
solved_line = []

pygame.display.set_caption("The best path finder! (Djikstra Algorithm)")
interface = pygame.display.set_mode((width, height))

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 170, 0)
grey = (130, 130, 130)
plum = (255, 187, 255)

all_elements_added = False
start_searching = False
start_point_set = False
end_point_set = False
running_algorithm = True


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_cell = False
        self.end_cell = False
        self.block_cell = False
        self.next_cells = []
        self.queued_cell = False
        self.checked_cell = False
        self.prior = None

    def fill_color(self, graph_interface, color):
        pygame.draw.rect(graph_interface, color, (self.x * cell_w, self.y * cell_h, cell_w - 3, cell_h - 3))

    def search_next_cells(self):
        if self.x > 0:
            self.next_cells.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.next_cells.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.next_cells.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.next_cells.append(grid[self.x][self.y + 1])


def create_grid():
    for i in range(columns):
        coordinates = []
        for j in range(rows):
            coordinates.append(Cell(i, j))
        grid.append(coordinates)


def set_next_cells():
    for i in range(columns):
        for j in range(rows):
            grid[i][j].search_next_cells()


def final_game():
    global all_elements_added, start_searching, start_point_set, end_point_set, running_algorithm
    create_grid()
    set_next_cells()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.mouse.get_pressed()[0]:
                coord_x = pygame.mouse.get_pos()[0]
                coord_y = pygame.mouse.get_pos()[1]
                pos_x = coord_x // cell_w
                pos_y = coord_y // cell_h
                cell = grid[pos_x][pos_y]

                if cell.block_cell is False and start_point_set is True and end_point_set is True:
                    if not cell.start_cell and not cell.end_cell:
                        cell.block_cell = True
                        all_elements_added = True

                elif start_point_set is False:
                    start_point = grid[pos_x][pos_y]
                    cell.start_cell = True
                    start_point_set = True
                    start_point.checked_cell = True
                    djikstra_queue.append(start_point)

                elif start_point_set is True and end_point_set is False:
                    end_point = grid[pos_x][pos_y]
                    cell.end_cell = True
                    end_point_set = True

            if event.type == pygame.KEYDOWN and all_elements_added is True:
                start_searching = True

        if start_searching:
            if len(djikstra_queue) > 0 and running_algorithm is True:
                current_cell = djikstra_queue.pop(0)
                current_cell.checked_cell = True
                if current_cell == end_point:
                    running_algorithm = False
                    while current_cell.prior != start_point:
                        solved_line.append(current_cell.prior)
                        current_cell = current_cell.prior
                else:
                    for near_cell in current_cell.next_cells:
                        if near_cell.queued_cell is False and near_cell.block_cell is False:
                            near_cell.queued_cell = True
                            near_cell.prior = current_cell
                            djikstra_queue.append(near_cell)
            else:
                if running_algorithm:
                    Tk().wm_withdraw()
                    messagebox.showinfo('Error: Solution Not Found',
                                        'There is no a path to reach the final point in this case')
                    pygame.quit()
                    sys.exit()

        interface.fill(grey)

        for i in range(columns):
            for j in range(rows):
                cell = grid[i][j]
                cell.fill_color(interface, white)
                if cell.queued_cell is True:
                    cell.fill_color(interface, plum)
                if cell.checked_cell is True:
                    cell.fill_color(interface, green)
                if cell in solved_line:
                    cell.fill_color(interface, red)
                if cell.start_cell is True:
                    cell.fill_color(interface, blue)
                if cell.end_cell is True:
                    cell.fill_color(interface, orange)
                if cell.block_cell is True:
                    cell.fill_color(interface, black)

        pygame.display.flip()


final_game()
