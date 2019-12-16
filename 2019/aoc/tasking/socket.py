from .util import Interupt


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
