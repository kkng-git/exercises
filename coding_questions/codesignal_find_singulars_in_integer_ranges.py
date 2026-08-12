def Solution(ranges):
    # range in ranges = [start, end]
    # start = +1
    # end = -1

    # Store result
    res = 0
    # Keep track of actors on the number line
    directory = dict()
    for start, end in ranges:
        # print(start, end)
        if start not in directory:
            directory[start] = 0
        directory[start]+=1
        if end+1 not in directory:
            directory[end+1] = 0
        directory[end+1]-=1
    points = sorted(directory.keys())
    freq = 0
    for i in range(len(points)-1):
        point = points[i]
        next = points[i+1]

        freq += directory[point]
        if freq == 1:
            # freq is 1 up until next point
            res += next - point
    return res


example = [[10, 15], [12, 20], [14, 18]]
print(Solution(example))