from .socket import Socket


class Task:
    def __init__(self, input=None, output=None):
        if isinstance(input, list):
            input = Socket(input)

        self.input = input or Socket()
        self.output = output or Socket()

    async def run(self):
        pass
