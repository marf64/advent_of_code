class Memory(list):
    def __setitem__(self, index, value):
        missing = index - len(self) + 1
        if missing > 0:
            self.extend([0] * missing)
        super(Memory, self).__setitem__(index, value)
    def __getitem__(self, index):
        try:
            return super(Memory, self).__getitem__(index)
        except IndexError:
            return 0

class Interupt:
    def __await__(self):
        return iter([1])

class Socket:
    def __init__(self, content=[]):
        self.content = content

    def __repr__(self):
        return str(self.content)

    # This definitely does not need to be a coroutine but keeping it as one for now just in case
    async def write(self, data):
        self.content.append(data)

    async def read(self):
        while not len(self.content):
            await Interupt()
        return self.content.pop(0)

class Task:
    def __init__(self, input=None, output=None):
        if isinstance(input, list):
            input = Socket(input)

        self.input = input or Socket()
        self.output = output or Socket()

    async def run(self):
        pass

class FSM(Task):
    def __init__(self, input=None, output=None):
        super(FSM, self).__init__(input, output)

class Program(Task):
    def __init__(self, memory, input=None, output=None):
        super(Program, self).__init__(input, output)

        self.memory = Memory(memory.copy())

        # Relative base
        self.relative = 0

    # Gets data from pos - if mode == 0 then gets data from position stored at pos
    def get_data(self, pos, mode=1):
        p = self.memory[pos]
        return (
            p if mode == 1 
            else self.memory[p] if mode == 0 
            else self.memory[self.relative + p]
        )

    # Sets data at pos to value
    def set_data(self, pos, value, mode=1):
        p = self.relative + pos if mode == 2 else pos
        self.memory[p] = value

    # (function, number of parameters, total_length)
    # [Wasn't always the case but num_parameters is now always total_length - 1 but whatevs]
    @property
    def ins_map(self):
        return {
            1: (self.add, 3, 4),
            2: (self.mul, 3, 4),
            3: (self.do_input, 1, 2),
            4: (self.do_output, 1, 2),
            5: (self.jump_if_true, 2, 3),
            6: (self.jump_if_false, 2, 3),
            7: (self.less_than, 3, 4),
            8: (self.equals, 3, 4),
            9: (self.adjust_relative, 1, 2),
            99: (self.halt, 0, 1)
        }

    
    # Opcode 1 - length 4
    async def add(self, pos, modes):
        p1 = self.get_data(pos+1, modes[2])
        p2 = self.get_data(pos+2, modes[1])
        p3 = self.get_data(pos+3)
        self.set_data(p3, p1 + p2, modes[0])
        return pos + 4

    # Opcode 2 - length 4
    async def mul(self, pos, modes):
        p1 = self.get_data(pos+1, modes[2])
        p2 = self.get_data(pos+2, modes[1])
        p3 = self.get_data(pos+3)
        self.set_data(p3, p1 * p2, modes[0])
        return pos + 4

    # Opcode 3 - length 2
    async def do_input(self, pos, modes):
        val = await self.input.read()

        p = self.get_data(pos+1)
        self.set_data(p, val, modes[0])
        return pos+2

    # Opcode 4 - length 2
    async def do_output(self, pos, modes):
        p = self.get_data(pos+1, modes[0])
        
        await self.output.write(p)

        return pos+2

    # Opcode 5 - length 3
    async def jump_if_true(self, pos, modes):
        p1 = self.get_data(pos+1, modes[1])
        p2 = self.get_data(pos+2, modes[0])
        if p1 != 0:
            return p2
        return pos+3

    # Opcode 6 - length 3
    async def jump_if_false(self, pos, modes):
        p1 = self.get_data(pos+1, modes[1])
        p2 = self.get_data(pos+2, modes[0])
        if p1 == 0:
            return p2
        return pos+3

    # Opcode 7 - length 4
    async def less_than(self, pos, modes):
        p1 = self.get_data(pos+1, modes[2])
        p2 = self.get_data(pos+2, modes[1])
        p3 = self.get_data(pos+3)
        val = 1 if p1 < p2 else 0
        self.set_data(p3, val, modes[0])
        return pos+4

    # Opcode 8 - length 4
    async def equals(self, pos, modes):
        p1 = self.get_data(pos+1, modes[2])
        p2 = self.get_data(pos+2, modes[1])
        p3 = self.get_data(pos+3)
        val = 1 if p1 == p2 else 0
        self.set_data(p3, val, modes[0])
        return pos+4

    # Opcode 9 - length 2
    async def adjust_relative(self, pos, modes):
        p = self.get_data(pos+1, modes[0])
        self.relative += p
        return pos+2

    # Opcode 99 - Returns -1 which is the halt code 
    async def halt(self, pos, modes=[]):
        return -1

    async def execute_ins(self, pos):
        opcode, modes = self.parse_opcode(self.memory[pos])
        return await self.ins_map[opcode][0](pos, modes)

    async def run(self, ptr=0):
        while ptr != -1:
            ptr = await self.execute_ins(ptr)

    # Adds leading 0s to modes - Big assumption that len(modes) <= length
    def format_modes(self, opcode, length):
        modes = [int(m) for m in str(opcode // 100)]
        return [0]*(length - len(modes)) + modes

    def parse_opcode(self, opcode):
        op = opcode % 100
        modes = self.format_modes(opcode, self.ins_map[op][1])
        return (op, modes)


def run_tasks(tasks):
        running = [task.run() for task in tasks]
    while len(running):
        for i, task in enumerate(running):
            try:
                task.send(None)
            except StopIteration:
                running.pop(i)

# For backwards compatibility
run_programs = run_tasks


