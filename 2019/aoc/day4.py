# Range 158126-624574
# Gonna brute force it cuz fuck it. I forsee this biting me in the ass in part 2

# Assuming always 6 digit input
def check_it(x):
    adj = False
    f = 100000
    d = x // f
    x = x % f
    f = f // 10
    while f != 0:
        t = x // f
        if d > t:
            return False
        elif d == t:
            adj = True
        d = t
        x = x % f
        f = f // 10

    return adj


# Part 1
# count = 0 
# for x in range(158126, 624574):
# 	count += int(check_it(x))
# print(count)

# Part 2

# so dumb so ugly
def check_it_again(x):
    adj = bang = False
    f = 100000
    d = x // f
    x = x % f
    f = f // 10
    while f != 0:
        t = x // f
        if d > t:
            return False
        elif d == t:
            if bang and not adj:
                pass
            elif adj:
                bang = False
            elif not adj:
                adj = True
                bang = True
        else:
            adj = False
        d = t
        x = x % f
        f = f // 10

    return bang


count = 0
for x in range(158126, 624574):
    count += int(check_it_again(x))

print(count)
