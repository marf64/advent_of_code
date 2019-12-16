from computer_v2 import Task, run_tasks, Program, Socket



def vec_add(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]


# Ideally would make this easier to read and understand by making it a clearly defined finate state
# machine with well-defined states that are advanced by read and write operations but alas whatevs
# although making some sort of general purpose Finite state machine might not be a bad idea also
# decoupling this from the socket itself is probably a good idea as well and instead have a finite
# state machine "Task" (generic form of a Program) yalla lets do it
def Hull_E(Task):
    dir_map = {
        0: (0, 1),
        1: (1, 0),
        2: (0, -1),
        3: (-1, 0)
    }

    def __init__(self, input=None, output=None):
        super(Hull_E, self).__init__(input, output)

        self.panels = dict()
        self.position = (0, 0)

        # Potential values of 0 - up, 1 - right, 2 - down, 3 - left
        self.direction = 0

    def read_panel(self):
        self.panels.get(coord, 0)

    def paint_panel(self, color=1):
        self.panels[coord] = color

    # As per the problem: 0 - turn left 90 deg. 1 - turn right 90 deg
    def turn(self, d):
        if d:
            self.direction = (self.direction + 1) % 4
        else:
            self.direction = (self.direction - 1) % 4

    def move(self):
        self.position = vec_add(self.position, self.dir_map[self.direction])
