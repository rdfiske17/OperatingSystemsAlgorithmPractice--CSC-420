# Write a program (in your choice of programming language) to simulate a contiguous memory allocation algorithm.
# You may choose to implement any of the three common contiguous allocation schemes (first fit, best fit, or worst fit).
# Assume a fixed memory, and an input consisting of a sequence of incoming processes each with a required memory space mixed with completing processes.
# The job of your program is to allocate space to incoming processes and reclaim space used by completing processes.

# To simplify the program implementation, make the memory size and all requests a multiple of some fixed size (say 1k).
# Whenever there is no “hole” large enough to accommodate an incoming process, your program should determine if the total available space
# is sufficient to accommodate the incoming process, and if that is the case, then the memory should be compacted and the space allocated.
# If a process cannot be allocated space, it should be placed on a queue that should be checked whenever space is reclaimed.

# Each time a process is allocated, your program should display a “picture” of how memory space is currently allocated. This display can be in any format you choose (i.e. a textual description is fine).

# The program should also keep track of the number of times it has to compact the memory and the number of times it has to queue a process and display these values as a percentage of the total number of processes.

# You will need to design your own data, but it should be large enough to demonstrate the fragmentation, compaction and queuing of the different processes.

##################################################

# Implementing a First-Fit Algorithm

# Create a Memory Class



############# START MEMORY CLASS DECLARATION #############

class Memory:
    # Constuctor
    def __init__(self, total_blocks):
        self.total_blocks = total_blocks
        self.blocks = [None] * total_blocks  # None represents a free block
        self.process_queue = [] # processes waiting for memory allocation
        self.total_processes = 0
        self.compaction_count = 0 # increment this whenever we compact the memory
        self.queuing_count = 0 # increment this whenever we queue a process

    # Allocating a Process involves checking if the process already exists in memory, finding the first block with enough space to fit the process,
    # allocating the process to that block if one exists, otherwise check if there is enough memory noncontiguously available to fulfill the request (compact and retry)
    # or claim the process unallocatable and add it to the process queue. Also, increment the total_processes counter and the queuing_counter (if applicable).
    def allocate_process(self, process_id, size):
        # Start by checking if process exists in memory already
        if process_id in self.blocks:
            print("Process ", process_id, " already exists in memory.")
            return

        # Look for first block that has enough space for the size of the requesting process
        start_index = None
        block_count = 0
        for i, block in enumerate(self.blocks):
            if block is None: # if block is free
                if start_index is None: # if starting index has not been set yet
                    start_index = i
                block_count += 1 # increment block count further
            else: # block is not free
                start_index = None # reset the starting index
                block_count = 0 # reset the block count
            
            if block_count == size:
                break # we've found our match!
        
        # either say there's not enough space
        if block_count < size:
            total_available_space = sum(1 for block in self.blocks if block is None)
            if total_available_space >= size:
                print("Not enough contiguous memory for Process ", process_id, ". Compacting Memory to create contiguous space for Process", process_id, ".")
                self.compact_memory()
                self.allocate_process(process_id, size)
            else:
                print("Insufficient Total Memory. Process", process_id, " added to the Waiting Queue for later allocation.")
                self.process_queue.append((process_id, size)) # add process to queue
                self.queuing_count += 1 # increment queue count
                self.total_processes += 1 # also increment this for calculating statistics
            return

        # or allocate memory to process
        for i in range(start_index, start_index + size):
            self.blocks[i] = process_id
        
        print("Proces ", process_id, " has been allocated memory from ", start_index, " to ", start_index + size - 1)
        self.total_processes += 1
        self.print_memory_map()

        self.process_queue = [(p_id, p_size) for p_id, p_size in self.process_queue if p_id != process_id]

        return

    # Deallocating a Process is much simpler than allocating one. One must find where the process exists in memory, then free up that space.
    def deallocate_process(self, process_id):
        start_index = None
        process_size = 0
        for i in range(len(self.blocks)):
            if self.blocks[i] == process_id:
                if start_index is None:
                    start_index = i
                self.blocks[i] = None
                process_size += 1
        print("Deallocating Process ", process_id, " from ", start_index, " to ", start_index + process_size - 1)
        self.print_memory_map()

        # run through queue and allocate where possible
        for process_id, process_size in self.process_queue:
            self.allocate_process(process_id, process_size)
        return

    # Compact Memory involves moving the process memory units as far forward as possible to free up gaps left by deallocation.
    # The procedure walks through memory sequentially fetching the allocated process indices and moving the process data to the first available
    # free memory space. Then increment compaction count and print the memory map.
    def compact_memory(self):
        # Initialize indices for tracking the next available slot and the next slot to check for compaction
        next_free_index = 0
        next_process_index = 0

        # Iterate through memory
        while next_process_index < self.total_blocks:
            # If the current block is allocated
            if self.blocks[next_process_index] is not None:
                # If the current block is not already in the correct position
                if next_process_index != next_free_index:
                    # Move the process to the next available free slot
                    self.blocks[next_free_index] = self.blocks[next_process_index]
                    # Clear the original slot
                    self.blocks[next_process_index] = None
                # Move to the next free slot
                next_free_index += 1
            # Move to the next block
            next_process_index += 1

        # Update the compaction count
        self.compaction_count += 1

        # Print the memory map after compaction
        self.print_memory_map()

        return

    # To print memory, simply loop through each block and report if it is free or allocated
    def print_memory_map(self):
        print("Memory Map:")
        for i, block in enumerate(self.blocks):
            if block is None:
                print("Block ", i, ": Free")
            else:
                print("Block ", i, ": Allocated to Process ", block)
        print()

    # Printing Statistics reports the Compacting Rate and the Queuing Rate of the Memory Management Unit, as collected through allocate_process and compact_memory
    def print_statistics(self):
        compaction_percentage = (self.compaction_count / self.total_processes) * 100
        queueing_percentage = (self.queuing_count / self.total_processes) * 100
        print("Memory Compaction Percentage: ", compaction_percentage, "%")
        print("Process Queueing Percentage: ", queueing_percentage, "%")

############# END MEMORY CLASS DECLARATION #############



# Now create a memory object and start doing things with it

memory = Memory(50)

memory.print_memory_map()

memory.allocate_process("001", 10)
memory.allocate_process("002",15)
memory.allocate_process("003",20) # 45/50 full
memory.allocate_process("004", 12) # not enough space, add to queue
memory.deallocate_process("001") # deallocate 1, then compact and allocate 4

memory.allocate_process("005",19) # not enough space, add to queue
memory.deallocate_process("003") # deallocate 3, then allocate 5

memory.allocate_process("006",4) # not enough contiguous space, compact and allocate 6

memory.print_statistics() # print final statistics