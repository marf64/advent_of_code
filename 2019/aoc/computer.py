class Computer:
    # Need to buff up input and output so that they act as signals and slots
    # Currently have a primitive version of this with set_input and on_output
    # I feel like this is eventually gonna need to be parrallelizable
    # I think I can create a ThreadSafeComputer that wraps this Computer
    # For ease of use need to fix input and output though
    # Maybe some form of connect function and a generalized Node object that
    # This inherits from that handles input output operations (Similar to Web Audio Api)
    def __init__(self, intcodes, input=[], ptr=0):
        self.ptr = ptr
        self.intcodes = intcodes.copy()
        self.input = input.copy()
        self.output = []

        self.running = 0
        self.wait4input = 0

        self.output_callbacks = []

    # Sets input. If wait4input True then resumes do_work at current ptr
    def set_input(self, inp):
        self.input = inp.copy()
        if self.wait4input:
            self.wait4input = 0
            self.do_work(self.ptr)

    # Append values to input
    def add_input(self, inp):
        self.set_input(self.input + inp)

    # Code to call on new output value
    def on_output(self, callback):
        self.output_callbacks.append(callback)

    # Clears output list
    def clear_output(self):
        self.output = []

    # Gets data from pos - mode == 0 then gets data from position stored at pos
    def get_data(self, pos, mode=1):
        p = self.intcodes[pos]
        return p if mode else self.intcodes[p]

    # Sets data at pos to value
    def set_data(self, pos, value):
        self.intcodes[pos] = value

    # (function, parameter_length, total_length)
    @property
    def ins_map(self):
        return {
            1: (self.add, 2, 4),
            2: (self.mul, 2, 4),
            3: (self.do_input, 1, 2),
            4: (self.do_output, 1, 2),
            5: (self.jump_if_true, 2, 3),
            6: (self.jump_if_false, 2, 3),
            7: (self.less_than, 2, 4),
            8: (self.equals, 2, 4),
            99: (self.halt, 0, 1)
        }

    # Adds leading 0s to modes - Big assumption that len(modes) <= length
    def format_modes(self, modes, length):
        return [0] * (length - len(modes)) + modes

    # Opcode 1 - length 4
    def add(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        p3 = self.get_data(pos + 3)
        self.set_data(p3, p1 + p2)
        return pos + 4

    # Opcode 2 - length 4
    def mul(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        p3 = self.get_data(pos + 3)
        self.set_data(p3, p1 * p2)
        return pos + 4

    # Opcode 3 - length 2
    def do_input(self, pos, modes):
        if not len(self.input):
            self.wait4input = 1
            return pos

        val = self.input.pop(0)
        p = self.get_data(pos + 1)
        self.set_data(p, val)
        return pos + 2

    # Opcode 4 - length 2
    def do_output(self, pos, modes):
        p = self.get_data(pos + 1, modes[0])
        self.output.append(p)

        for cb in self.output_callbacks:
            cb(self.output)

        return pos + 2

    # Opcode 5 - length 3
    def jump_if_true(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        if p1 != 0:
            return p2
        return pos + 3

    # Opcode 6 - length 3
    def jump_if_false(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        if p1 == 0:
            return p2
        return pos + 3

    # Opcode 7 - length 4
    def less_than(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        p3 = self.get_data(pos + 3)
        val = 1 if p1 < p2 else 0
        self.set_data(p3, val)
        return pos + 4

    # Opcode 8 - length 4
    def equals(self, pos, modes):
        p1 = self.get_data(pos + 1, modes[1])
        p2 = self.get_data(pos + 2, modes[0])
        p3 = self.get_data(pos + 3)
        val = 1 if p1 == p2 else 0
        self.set_data(p3, val)
        return pos + 4

    # Opcode 99 - Returns -1 which is the halt code 
    def halt(self, pos, modes=[]):
        return -1

    def parse_opcode(self, opcode):
        op = opcode % 100
        modes = self.format_modes([int(m) for m in str(opcode // 100)], self.ins_map[op][1])
        return (op, modes)

    def read_ins(self, pos):
        opcode, modes = self.parse_opcode(self.intcodes[pos])
        return self.ins_map[opcode][0](pos, modes)

    def do_work(self, ptr=0):
        self.running = 1

        self.ptr = self.read_ins(ptr)

        while self.ptr != -1 and not self.wait4input:
            self.ptr = self.read_ins(self.ptr)

        if self.ptr == -1:
            self.running = 0
