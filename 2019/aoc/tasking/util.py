class Interupt:
    def __await__(self):
        return iter([1])
