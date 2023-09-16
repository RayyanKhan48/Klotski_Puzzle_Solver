#Imports the pre-conditioned module of queue from Python  
from queue import PriorityQueue  
  
#sys module allows us to read and write to the given txt files  
import sys  
  
#Output values of the horizontal and vertical pieces   
horizontal_output_piece = 2  
vertical_output_piece = 3  
  
#The initial input values of the board  
large_piece = 1  
small_piece = 7  
one_by_two_piece = [2, 3, 4, 5, 6]  
  
#The height and width of the board   
board_height = 5  
board_width = 4  
  
#The index of our goal state (used for A*)  
goal_index = 13  
  
  
#Converts the index value from the list of integers to x and y coordinates where x represents the columns and y represents the rows  
def convert_to_coordinates(index):  
    return (index % board_width, index//board_width)  
  
#Converts the x and y coordinates to the index value  
def convert_to_index(board, x, y):  
    if x < 0 or x >= board_width or y < 0 or y >= board_height:  
        return -1  
    return board[y*board_width + x]  
  
#Assigns whether a piece is a vertical or horizontal piece  
def get_piece_type(board, index):  
    (x, y) = convert_to_coordinates(index)  
    board_number = board[index]  
    #Checks for left value on board  
    if convert_to_index(board, x-1, y) == board_number:  
        return horizontal_output_piece  
    #Checks for right value on board  
    if convert_to_index(board, x+1, y) == board_number:  
        return horizontal_output_piece  
    #Checks for the bottom value on board  
    if convert_to_index(board, x, y-1) == board_number:  
        return vertical_output_piece  
    #Checks for the above value on board  
    if convert_to_index(board, x, y+1) == board_number:  
        return vertical_output_piece  
  
  
class State:  
    def __init__(self, init=False, board=[], zeros=[], piece_one_by_two={}):  
        #Initialization for the starting state   
        self.initialized = init  
  
        #List of integers of length 20, consisting the whole board  
        self.board_list = board  
  
        #Initially setting the cost to inifinity  
        self.cost_a_star = 9999999999  
  
        #The number of moves until the goal state  
        self.distance = 0  
  
        #Keeps track of the previous node for back tracking  
        self.previous = None  
  
        #Keeps track of where the empty positions are  
        self.zeros = zeros  
  
        #Dictionary of pieces  
        self.piece_one_by_two = piece_one_by_two  
  
  
    #Comapres the copied list with the saved list, used for putting the State object into a dictionary  
    def __eq__(self, other):  
        if not isinstance(other, State):  
            return NotImplemented  
        copy_list = self.board_list.copy()  
        for i in range(len(copy_list)):  
            if copy_list[i] in self.piece_one_by_two:  
                copy_list[i] = self.piece_one_by_two[copy_list[i]]  
        hash_string = ''.join([str(x) for x in copy_list])  
        copy_list_other = other.board_list.copy()  
        for i in range(len(copy_list_other)):  
            if copy_list_other[i] in other.piece_one_by_two:  
                copy_list_other[i] = other.piece_one_by_two[copy_list_other[i]]  
        hash_string_other = ''.join([str(x) for x in copy_list_other])  
        return isinstance(other, State) and hash_string_other == hash_string  
  
    #Once again simply used to store the State object into a dictionary  
    def __lt__(self, other):  
        return isinstance(other, State) and ''.join([str(x) for x in self.board_list]) < ''.join([str(x)for (x) in other.board_list])  
  
    #Need to include hash as __eq__ was incorporated otherwise it'll be set to None (State into dictionary)  
    def __hash__(self):  
        copy_list = self.board_list.copy()  
        for i in range(len(copy_list)):  
            if copy_list[i] in self.piece_one_by_two:  
                copy_list[i] = self.piece_one_by_two[copy_list[i]]  
        hash_string = ''.join([str(x) for x in copy_list])  
        return hash(hash_string)  
  
    #Called to intialize the starting state (remaining states are initialized by generate_neighbours())  
    def init_start_state(self):  
        if self.initialized:  
            sys.exit()  
        for current_piece in one_by_two_piece:  
            for i in range(board_width*board_height):  
                if self.board_list[i] == current_piece:  
                    self.piece_one_by_two[current_piece] = get_piece_type(self.board_list, i)  
                    break  
        for i in range(board_width * board_height):  
            if self.board_list[i] == 0:  
                self.zeros.append(i)  
        self.initialized = True  
  
    #Checks whether the board has a valid layout  
    def check_valid_board(self):  
        board_list = self.board_list  
        large_piece_check = False  
        pieces_map = self.piece_one_by_two  
        for y in range(board_height):  
            for x in range(board_width):  
                current_value = convert_to_index(board_list, x, y)  
                if current_value in pieces_map and pieces_map[current_value] == horizontal_output_piece:  
                    if convert_to_index(board_list, x-1, y) != current_value and convert_to_index(board_list, x+1, y) != current_value:  
                        return False  
                if current_value in pieces_map and pieces_map[current_value] == vertical_output_piece:  
                    if convert_to_index(board_list, x, y-1) != current_value and convert_to_index(board_list, x, y+1) != current_value:  
                        return False  
                if not large_piece_check and convert_to_index(board_list, x, y) == large_piece:  
                    if not(convert_to_index(board_list, x+1, y) == large_piece and convert_to_index(board_list, x, y+1) == large_piece and convert_to_index(board_list, x+1, y+1) == large_piece):  
                        return False  
                    large_piece_check = True  
        return True  
  
    #Swaps the coordinate values with the empty spaces  
    def swap(self, zerox, zeroy, targetx, targety):  
        board_list = list(self.board_list)  
        i1, i2 = zeroy*board_width + zerox,  targety*board_width + targetx  
        board_list[i1], board_list[i2] = board_list[i2], board_list[i1]  
        newZeros = self.zeros.copy()  
        for i in range(len(newZeros)):  
            if convert_to_coordinates(newZeros[i]) == (zerox, zeroy):  
                newZeros[i] = targety*board_width + targetx  
                break  
        return State(init=True, board=board_list, zeros=newZeros, piece_one_by_two=self.piece_one_by_two)  
  
    #Generates the surrounding neighbours using the coordinate values  
    def generate_neighbours(self):  
        if not self.check_valid_board():  
            sys.exit()  
        if not self.initialized:  
            sys.exit()  
        neighbours = []  
        (x1, y1) = convert_to_coordinates(self.zeros[0])  
        (x2, y2) = convert_to_coordinates(self.zeros[1])  
        for (x, y) in (x1, y1), (x2, y2):  
            neighbours.extend(self.single_available_space(x, y))  
        if (x1 == x2) and abs(y1 - y2) == 1:  
            neighbours.extend(self.vertical_available_space(x1, y1, x2, y2))  
        if (y1 == y2) and abs(x1 - x2) == 1:  
            neighbours.extend(self.horizontal_available_space(x1, y1, x2, y2))  
        return neighbours  
  
    #Allows for the horizontal piece to be swapped  
    def horizontal_available_space(self, x1, y1, x2, y2):  
        neighbour = []  
        up_1 = convert_to_index(self.board_list, x1, y1-1)  
        up_2 = convert_to_index(self.board_list, x2, y1-1)  
        down1 = convert_to_index(self.board_list, x1, y1+1)  
        down2 = convert_to_index(self.board_list, x2, y1+1)  
        if(up_1 == up_2):  
            if up_1 in self.piece_one_by_two and self.piece_one_by_two[up_1] == horizontal_output_piece:  
                tempState = self.swap(x1, y1, x1, y1-1)  
                neighbour.append(tempState.swap(x2, y2, x2, y2-1))  
            if up_1 == large_piece:  
                tempState = self.swap(x1, y1, x1, y1-2)  
                neighbour.append(tempState.swap(x2, y2, x2, y2-2))  
        if(down1 == down2):  
            if down1 in self.piece_one_by_two and self.piece_one_by_two[down1] == horizontal_output_piece:  
                tempState = self.swap(x1, y1, x1, y1+1)  
                neighbour.append(tempState.swap(x2, y2, x2, y2+1))  
            if down1 == large_piece:  
                tempState = self.swap(x1, y1, x1, y1+2)  
                neighbour.append(tempState.swap(x2, y2, x2, y2+2))  
        return neighbour  
  
    #Allows for the vertical piece to be swapped  
    def vertical_available_space(self, x1, y1, x2, y2):  
        neighbour = []  
        left1 = convert_to_index(self.board_list, x1-1, y1)  
        left2 = convert_to_index(self.board_list, x1-1, y2)  
        right1 = convert_to_index(self.board_list, x1+1, y1)  
        right2 = convert_to_index(self.board_list, x1+1, y2)  
        if(left1 == left2):  
            if left1 in self.piece_one_by_two and self.piece_one_by_two[left1] == vertical_output_piece:  
                tempState = self.swap(x1, y1, x1-1, y1)  
                neighbour.append(tempState.swap(x2, y2, x2-1, y2))  
            if left1 == large_piece:  
                tempState = self.swap(x1, y1, x1-2, y1)  
                neighbour.append(tempState.swap(x2, y2, x2-2, y2))  
        if(right1 == right2):  
            if right1 in self.piece_one_by_two and self.piece_one_by_two[right1] == vertical_output_piece:  
                tempState = self.swap(x1, y1, x1+1, y1)  
                neighbour.append(tempState.swap(x2, y2, x2+1, y2))  
            if right1 == large_piece:  
                tempState = self.swap(x1, y1, x1+2, y1)  
                neighbour.append(tempState.swap(x2, y2, x2+2, y2))  
        return neighbour  
  
    #Allows for the single piece to be swapped  
    def single_available_space(self, x, y):  
        neighbour = []  
        left = convert_to_index(self.board_list, x-1, y)  
        right = convert_to_index(self.board_list, x+1, y)  
        down = convert_to_index(self.board_list, x, y+1)  
        up = convert_to_index(self.board_list, x, y-1)  
        if left in self.piece_one_by_two and self.piece_one_by_two[left] == horizontal_output_piece:  
            neighbour.append(self.swap(x, y, x-2, y))  
        if right in self.piece_one_by_two and self.piece_one_by_two[right] == horizontal_output_piece:  
            neighbour.append(self.swap(x, y, x+2, y))  
        if down in self.piece_one_by_two and self.piece_one_by_two[down] == vertical_output_piece:  
            neighbour.append(self.swap(x, y, x, y+2))  
        if up in self.piece_one_by_two and self.piece_one_by_two[up] == vertical_output_piece:  
            neighbour.append(self.swap(x, y, x, y-2))  
        if left == small_piece:  
            neighbour.append(self.swap(x, y, x-1, y))  
        if right == small_piece:  
            neighbour.append(self.swap(x, y, x+1, y))  
        if up == small_piece:  
            neighbour.append(self.swap(x, y, x, y-1))  
        if down == small_piece:  
            neighbour.append(self.swap(x, y, x, y+1))  
        return neighbour  
  
    #Checks to see whether the the large piece has reached the goal position  
    def goal_state(self):  
        board = self.board_list  
        return convert_to_index(board, 1, 4) == large_piece and convert_to_index(board, 2, 4) == large_piece  
  
  
    #Converts the string into the desired board format of 4x5  
    def board_output(self):  
        copy_list = self.board_list.copy()  
        self.piece_one_by_two[small_piece]=4  
        for i in range(len(copy_list)):  
            if copy_list[i] in self.piece_one_by_two:  
                copy_list[i] = self.piece_one_by_two[copy_list[i]]  
        output_string = ''.join([str(x) for x in copy_list])  
        output_string_formatted = ''  
        for y in range(board_height):  
            output_string_formatted += output_string[y*board_width:(y+1)*board_width]  
            output_string_formatted += "\n"  
        return output_string_formatted  
  
    #Writes to the fle at the end and outputs all over the states  
    def output_to_file(self, fileName, isAstar):  
        current_state = self  
        with open(fileName, 'w') as the_file:  
            if isAstar:  
                the_file.write("Cost of the solution: " + str(current_state.cost_a_star))  
            else:  
                the_file.write("Cost of the solution: " + str(current_state.distance))  
            the_file.write("\n")  
            correct_list = []  
            while current_state != None:  
                correct_list.append(current_state)  
                current_state = current_state.previous  
            for state in correct_list[::-1]:  
                the_file.write(state.board_output())  
                the_file.write("\n")  
  
  
#Advanced heuristic  
def advanced_heuristic(neibourState):  
    #Setting a random value which will be changed as per the heuristic  
    left_index = 20  
    additional_distance = 0  
    board_list = neibourState.board_list  
    for i in range(len(board_list)):  
        if board_list[i] == large_piece:  
            left_index = i  
            break  
    left_index_x = left_index % board_width  
    left_index_y = left_index // board_width  
    goal_x = goal_index % board_width  
    goal_y = goal_index // board_width  
    #Differnce between the x and y coordinates  
    manhattan_distance = abs(left_index_x - goal_x) + abs(left_index_y - goal_y)  
    #Checks for direct adjacency for reversal  
    if abs(left_index_x - goal_x) == 1 or abs(left_index_y - goal_y) == 1:  
        additional_distance += 1  
    final_distance = manhattan_distance + (2*additional_distance)  
    return final_distance  
  
  
#Manhattan distance heuristic  
def heuristic(neibourState):  
    #Setting a random value which will be changed as per the heuristic  
    left_index = 20  
    board_list = neibourState.board_list  
    for i in range(len(board_list)):  
        if board_list[i] == large_piece:  
            left_index = i  
            break  
    left_index_x = left_index % board_width  
    left_index_y = left_index // board_width  
    goal_x = goal_index % board_width  
    goal_y = goal_index // board_width  
    #Differnce between the x and y coordinates  
    manhattan_distance = abs(left_index_x - goal_x) + abs(left_index_y - goal_y)  
    return manhattan_distance  
  
#A* Search  
def a_star(startState: State):  
    current_state = startState  
    #From infinity the cost is set to 0  
    current_state.cost_a_star = 0  
    pQ = PriorityQueue()  
    pQ.put((heuristic(current_state), current_state))  
    #pQ.put((advanced_heuristic(current_state), current_state))  
    visited = set()  
    createdState = {}  
    createdState[current_state] = createdState  
    while not pQ.empty():  
        item = pQ.get()  
        current_state = item[1]  
        del createdState[current_state]  
        if current_state.goal_state():  
            break  
        #Updates the visited pieces  
        visited.add(current_state)  
        #Unvisited neighbours are pushed to the stack  
        possibleStates = current_state.generate_neighbours()  
        for neighbour in possibleStates:  
            if neighbour not in createdState and neighbour not in visited:  
                neighbour.cost_a_star = current_state.cost_a_star + 1  
                neighbour.previous = current_state  
                createdState[neighbour] = neighbour  
                pQ.put((heuristic(neighbour) + neighbour.cost_a_star, neighbour))  
                #pQ.put((advanced_heuristic(neighbour) + neighbour.cost_a_star, neighbour))  
    return current_state  
  
#DFS Search  
def dfs(startState: State):  
    current_state = startState  
    stack = [current_state]  
    visited = set()  
    while len(stack) != 0 and not current_state.goal_state():  
        current_state = stack.pop()  
        visited.add(current_state)  
        possibleStates = current_state.generate_neighbours()  
        for state in possibleStates:  
            if state not in visited:  
                state.distance = current_state.distance + 1  
                state.previous = current_state  
                stack.append(state)  
    return current_state  
  
  
def main(argv):  
    inputfile = ''  
    outputfileDfs = ''  
    outputfileAstar = ''  
    #Checks the argument number of the input  
    if len(argv) != 3:  
        sys.exit()  
    else:  
        inputfile = argv[0]  
        outputfileDfs = argv[1]  
        outputfileAstar = argv[2]  
    inputString = ''  
    #Reads from the input file  
    with open(inputfile) as f:  
        for line in f:  
            inputString += line.strip()  
  
    #Creates the starting state from the input  
    startState = State(board=[int(x) for x in list(inputString)])  
    #Initializes the starting state  
    startState.init_start_state()  
  
    #Runs A* on the starting state  
    endState = a_star(startState)  
    #Outputs the result to the respective file  
    endState.output_to_file(outputfileAstar, isAstar=True)  
  
    #Need to run this line again for Dfs   
    startState = State(board=[int(x) for x in list(inputString)])  
    #Initializes the starting state  
    startState.init_start_state()  
  
    #Runs Dfs on the starting state  
    endState = dfs(startState)  
    #Outputs the result to the respective file  
    endState.output_to_file(outputfileDfs, isAstar=False)  
  
  
if __name__ == "__main__":  
    main(sys.argv[1:])  