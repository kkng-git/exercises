def Solution(memory, queries):
    # memory is a binary array of 0s and 1s
    # queries is one of the following
        # [0, x]: Find leftmost free run of x cells whose start index is a multiple of 8
        # [1, ID]: release all cells owned by ID and return number of cells released
    
    id_counter = 0

    allocationIDs = dict()

    def allocate(memory, x):
        # base case
        if x > len(memory):
            return -1
        # Iterate by segments to see if theres a segment that fits x
        start = -1
        iterator = 0
        availableSize = 0
        while iterator < len(memory):
            # Chunk isn't allocated
            if memory[iterator] == 0:
                # New segment
                if availableSize == 0:
                    start = iterator
                availableSize+=8
            elif availableSize < x:
                availableSize = 0
                start = -1
                iterator+=1
                continue
            # we found enough chunks
            if availableSize >= x:
                break
            # Analyze next chunk
            iterator+=1

        # If no valid start, then data can't fit
        if start == -1:
            return -1
        # Allocate
        for i in range(start, start+x):
            memory[i] = 1

        allocationIDs[id_counter] = (start, x)
        id_counter += 1
        return start

    def deallocate(memory, id):
        # Given id, release the number of cells
        if id not in allocationIDs:
            return -1
        start, x = allocationIDs[id]
        # Deallocate
        for i in range(start, start+x):
            memory[i] = 0
        del allocationIDs[id]
        return x


    for query in queries:
        if query[0] == 0:
            # Allocate
            return allocate(memory, query[1])
        elif query[0] == 1:
            # Deallocate 
            return deallocate(memory, query[1])

