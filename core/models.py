from random import randint

from django.db import models
from django.db import transaction
from django.utils import timezone
from django.core.validators import MaxValueValidator


NEIGHBORS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


class Game(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    won = models.BooleanField(default=False)
    width = models.PositiveIntegerField(validators=[MaxValueValidator(128)])
    height = models.PositiveIntegerField(validators=[MaxValueValidator(128)])
    mines = models.PositiveIntegerField(validators=[MaxValueValidator(8192)])

    def __str__(self):
        return "{}: {}".format(self.user, self.start_date)

    def new_board(self):
        """
            Create all cells with bombs
        """
        self.too_much_mines(raise_except=True)
        mines = []
        for i in range(0, self.mines):
            while True:
                mine = (randint(0, self.width - 1), randint(0, self.height - 1))
                if mine in mines:
                    continue
                cell = Cell(game=self, x=mine[0], y=mine[1], is_mine=True, neighbors_mines=0)
                mines.append(cell)
                break

        Cell.objects.bulk_create(mines)

    def too_much_mines(self, raise_except=False):
        mines_avg = self.mines / (self.width * self.height)
        if mines_avg > 0.4:
            if raise_except:
                raise Exception('The amount of mines is grater than 40%% of cells')
            return True
        return False

    def finish_game(self, won):
        self.end_date = timezone.now()
        self.won = won
        self.save()

    def reveal(self, x, y):
        if self.end_date:
            raise Exception('Game finished')

        if x > self.width or y > self.height:
            raise Exception('Cell index error')

        cell = self.cells.filter(x=x, y=y).first()
        if cell is None:
            matrix = self.get_matrix()
            queue = [(x, y)]
            while len(queue) > 0:
                next_field = queue.pop(0)
                with transaction.atomic():
                    self._reveal(next_field[0], next_field[1], matrix, queue)
        else:
            if cell.is_mine:
                self.finish_game(False)
            return

        if self.cells.count() == self.width * self.height:
            self.finish_game(True)

        return

    def _reveal(self, x, y, matrix, queue):
        """ Reveals the fields
            If the field has no mines around, it will reveals its neighbors fields too.
            Its using a queue to process the reveals fields to avoid
            "maximum recursion depth exceeded" error.

        """

        cell_value = matrix[y][x]
        if cell_value is None:
            is_mine = False
            neighbors_mines = self.count_neighbors_mines(x, y, matrix)
            matrix[y][x] = self.get_cell_value(is_mine, neighbors_mines)
            Cell.objects.create(game=self,
                                x=x,
                                y=y,
                                revealed=True,
                                neighbors_mines=neighbors_mines)

            if neighbors_mines == 0:
                for nb_x, nb_y in self.get_neighboors(x, y, matrix):
                    if 0 <= nb_x < self.width and 0 <= nb_x < self.height:
                        queue.append((nb_x, nb_y))

        elif cell_value == -1:
            return True

        return False

    def get_neighboors(self, x, y, matrix):
        nb_list = []
        for mv_x, mv_y in NEIGHBORS:
            if x + mv_x < 0 or y + mv_y < 0:
                continue
            if x + mv_x >= self.width or y + mv_y >= self.height:
                continue

            nb_list.append((x + mv_x, y + mv_y))

        return nb_list

    def count_neighbors_mines(self, x, y, matrix):
        mines_count = 0
        for nb_x, nb_y in self.get_neighboors(x, y, matrix):
            if nb_x < 0 or nb_y < 0:
                continue
            try:
                if matrix[nb_y][nb_x] and matrix[nb_y][nb_x] < 0:
                    mines_count += 1
            except IndexError:
                continue
        return mines_count

    def get_matrix(self):
        matrix = [[None] * self.width for iy in range(0, self.height)]
        cells = self.cells.values_list('x', 'y', 'is_mine', 'neighbors_mines')
        for x, y, is_mine, neighbors_mines in cells:
            if x < 0 or y < 0:
                continue
            try:
                matrix[y][x] = self.get_cell_value(is_mine, neighbors_mines)
            except IndexError:
                continue
        return matrix

    def get_cell_value(self, is_mine, neighbors_mines):
        return -1 if is_mine else neighbors_mines

    @property
    def status(self):
        if self.end_date is None:
            return "In Game"

        if self.won:
            return "Won"
        else:
            return "Lost"

    def time(self):
        if self.end_date is None:
            return ''
        delta = self.end_date - self.start_date
        return int(delta.total_seconds() / 60)


class Cell(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='cells')
    x = models.PositiveIntegerField(validators=[MaxValueValidator(128)], db_index=True)
    y = models.PositiveIntegerField(validators=[MaxValueValidator(128)], db_index=True)
    is_mine = models.BooleanField(default=False, db_index=True)
    revealed = models.BooleanField(default=False)
    neighbors_mines = models.PositiveIntegerField()
