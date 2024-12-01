# Create a class which is something like 'InstructionRecord' with all of the relevant members such as opcode, source_reg, etc. and a basic constructor
class InstructionRecord:
    def __init__(self, opcode, destination, source1, source2):
        self.opcode = opcode
        self.destination = destination
        self.source1 = source1
        self.source2 = source2

class IntegerUnits:
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
    add_sub_reservations = [IntegerUnits(f"RS{i + 1}") for i in range(3)] #Declare RS for add/sub
    mul_div_reservations = [IntegerUnits(f"RS{i + 4}") for i in range(2)] #Declare RS for mul/div
    reservation_stations = add_sub_reservations + mul_div_reservations
    RAT = [None] * 8
    num_instructions, num_cycles, instruction_queue, RF = read_text_file()
    for instruction in range(num_instructions):
        issue_instructions(instruction_queue, reservation_stations, RAT, RF)
        dispatch_instructions(reservation_stations)
        broadcast_instructions(reservation_stations, RAT, RF)

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

#Makes sure an RS is open and assigns variables to the RS
def issue_instructions(instruction_queue, reservation_stations, RAT, RF):
    if not instruction_queue:
        return
    instruction = instruction_queue[0]
    
    # Find an available reservation station
    rs = None
    for station in reservation_stations:
        if station.busy==False and (
            (instruction.opcode in ADD_SUB_OPCODES and "RS1" <= station.name <= "RS3")
            or (instruction.opcode in MUL_DIV_OPCODES and "RS4" <= station.name <= "RS5")):
            rs = station
            break

    #If RS is found, update the rs
    if rs:
        rs.busy = True
        rs.op = instruction.opcode
        rs.vj, rs.qj = (
            (RF[instruction.source1], None) if RAT[instruction.source1] is None 
            else (None, RAT[instruction.source1]))
        rs.vk, rs.qk = (
            (RF[instruction.source2], None) if RAT[instruction.source2] is None 
            else (None, RAT[instruction.source2]))

         # Update the RAT to point to the reservation station
        RAT[instruction.destination] = rs.name

        # Remove the instruction from the instruction queue
        instruction_queue.pop(0)

#Makes sure all conditions are met, marks insturction as dispatched and sets the run time
def dispatch_instructions(reservation_stations):
    for rs in reservation_stations:
        if rs.busy and rs.dispatched==False and rs.qj is None and rs.qk is None:
            rs.dispatched = True
            rs.time_remaining = (
                ADD_TIME if rs.op in ADD_SUB_OPCODES 
                else MUL_TIME if rs.op == 2 
                else DIV_TIME
            )

def broadcast_instructions(reservation_stations, RAT, RF):
    #Loops through RS's
    for rs in reservation_stations:
        #If RS is taken, and dispatched and the runtime is still going
        if rs.busy and rs.dispatched and rs.time_remaining >0:
           #Deincrement time by 1
            rs.time_remaining -=1
            #If no time is remaining
            if rs.time_remaining ==0:
                #Do calculations based on the opcode
                if rs.op == 0:
                    result=rs.vj + rs.vk
                elif rs.op == 1:
                    result = rs.vj - rs.vk
                elif rs.op == 2:
                    result = rs.vj * rs.vk
                elif rs.op == 3:
                    result = rs.vj // rs.vk

                # Update the RAT and RF after instruction completes execution
                for reg, tag in enumerate(RAT):
                    #RS is destination, update RF with results and clear RAT
                    if tag == rs.name:
                        RAT[reg] = None
                        RF[reg] = result  

                # Update other reservation stations waiting on this result
                for other_rs in reservation_stations:
                    #If other RS's are waiting on the result of the RS for the first operand 
                    if other_rs.qj == rs.name:
                        other_rs.vj = result
                        other_rs.qj = None
                    #If other RS's are waiting on the result of the RS for the second operand 
                    if other_rs.qk == rs.name:
                        other_rs.vk = result
                        other_rs.qk = None
                #RS is now available to be used again
                rs.busy=False
                rs.dispatched=False
                

# Create output file assuming we have all the data we need
def output_simulation_result():
    pass


if __name__ == "__main__":
    main()
