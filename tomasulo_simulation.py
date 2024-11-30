# Create a class which is something like 'InstructionRecord' with all of the relevant members such as opcode, source_reg, etc. and a basic constructor
class InstructionRecord:
    def __init__(self, opcode, destination, source1, source2):
        self.opcode = opcode
        self.destination = destination
        self.source1 = source1
        self.source2 = source2

class ReservationStation:
    def __init__(self, name):
        self.name = name
        self.busy = False
        self.op = None
        self.vj = None
        self.vk = None
        self.qj = None
        self.qk = None
        self.dispatched = False
        self.time_remaining = 0

# Configuration
ADD_TIME = 2
SUB_TIME = 2
MUL_TIME = 10
DIV_TIME = 40

ADD_SUB_OPCODES = {0, 1}  
MUL_DIV_OPCODES = {2, 3} 

# Make the logic for the simulation
# Initialize each instruction record and put them in the queue
# Initialize all containers that we need such as reservation stations and execution units (probably can just be lists)
# Then issue, dispatch, broadcast etc.
# Make sure we are keeping track of all the data we need for the output file
def main():
    reservation_stations = [None] * 5
    RAT = [None] * 8
    num_instructions, num_cycles, instruction_queue, RF = read_text_file()
    for instruction in instruction_queue:
        pass  # start simulator logic with issuing


# Read in relevant data from the text file and use the data to populate variables, lists, etc to be used in the simulation
def read_text_file():
    instruction_queue = []
    RF = []
    line_index = 0
    with open("instruction_file.txt", "r") as file:
        file_lines = file.readlines()
        num_instructions = int(file_lines[line_index])
        line_index += 1
        num_cycles = int(file_lines[line_index])
        line_index += 1
        while line_index < (2 + num_instructions):
            split_line = file_lines[line_index].split(" ")
            opcode = int(split_line[0])
            destination = int(split_line[1])
            source1 = int(split_line[2])
            source2 = int(split_line[3])
            instruction = InstructionRecord(opcode, destination, source1, source2)
            instruction_queue.append(instruction)
            line_index += 1
        while line_index < (10 + num_instructions):
            RF.append(int(file_lines[line_index]))
            line_index += 1
    return num_instructions, num_cycles, instruction_queue, RF


# Create output file assuming we have all the data we need
def output_simulation_result():
    pass


if __name__ == "__main__":
    main()
