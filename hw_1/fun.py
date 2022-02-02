def fib_num(n):
    curr_num, next_num = 0, 1
    for _ in range(n):
        tmp = curr_num
        curr_num = next_num
        next_num = tmp + next_num
    return curr_num
