def do_thing():
    print(1)
    a = yield
    print(a)


def do_t():
    while True:
        yield None
