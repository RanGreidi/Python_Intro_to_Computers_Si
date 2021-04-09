import game_of_life_interface
import numpy as np
import matplotlib.pyplot as plt
import time

class GameOfLife(game_of_life_interface.GameOfLife):  # This is the way you construct a class that heritage properties
    
    def __init__(self, size_of_board, starting_position, rules):

        def initialize_board(starting_position,size_of_board):
            ''' This method returns initialized the board game. 
            Input size and position.
            Output a list that holds the board with a size of size_of_board*size_of_board.
                '''
            if starting_position <= 3   or starting_position > 6:    
                population = [0, 255] # 0 represents dead and 255 represents alive
                if starting_position == 1 or starting_position > 6 :
                    game_board = np.random.choice([0,255],(size_of_board,size_of_board))
                elif starting_position == 2:
                    game_board = np.random.choice([0,255],(size_of_board,size_of_board), p=[0.2, 0.8])
                elif starting_position == 3:
                    game_board = np.random.choice([0,255],(size_of_board,size_of_board), p=[0.8, 0.2])
                ones_board = np.ones(shape=(size_of_board+2,size_of_board+2))
                ones_board[1:size_of_board+1,1:size_of_board+1]=game_board
            if starting_position == 4:
                glider_gun =\
                [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,255,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,255,255],
                 [0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,255,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,255,255],
                 [255,255,0,0,0,0,0,0,0,0,255,0,0,0,0,0,255,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [255,255,0,0,0,0,0,0,0,0,255,0,0,0,255,0,255,255,0,0,0,0,255,0,255,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,255,0,0,0,0,0,255,0,0,0,0,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0,0,0,0,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

                ones_board = np.ones(shape=(size_of_board+2,size_of_board+2))
                ones_board[1:size_of_board+1,1:size_of_board+1] = np.zeros((size_of_board, size_of_board))
                ones_board[11:20,11:47] = glider_gun
            if starting_position == 5:
                pulsar = np.zeros((17, 17))
                pulsar[2, 4:7] = 255
                pulsar[4:7, 7] = 255
                pulsar += pulsar.T
                pulsar += pulsar[:, ::-1]
                pulsar += pulsar[::-1, :]
                ones_board = np.ones(shape=(size_of_board+2,size_of_board+2))
                ones_board[1:size_of_board+1,1:size_of_board+1] = np.zeros((size_of_board, size_of_board))
                #ones_board[10:27,10:27]=pulsar      ******fix the posiotin****
                ones_board[int((size_of_board +1)/2-8):int((size_of_board +1)/2 + 17-8),int((size_of_board +1)/2-8):int((size_of_board +1)/2 + 17-8)]=pulsar
            if starting_position == 6:
                ones_board = np.ones(shape=(size_of_board+2,size_of_board+2))
                ones_board[1:size_of_board+1,1:size_of_board+1] = np.zeros((size_of_board, size_of_board))
                ones_board[6:8,6:10] = [[255,0,0,255],[0,255,255,0]]                
            return ones_board
        self.size_of_board = size_of_board
        self.starting_position = starting_position
        self.rules = rules
        self.Board = initialize_board(starting_position,size_of_board)
         
    def update(self):
        
        born_list = self.rules.split('/')[0]   # making alist out of the input rules
        survive_list=self.rules.split('/')[1]
        survive_list=survive_list.split('S')[1]
        born_list=born_list.split('B')[1]
        born_list=[int(i) for i in str(born_list)] #born list is the list of all born rules aka B321=[3,2,1]
        survive_list=[int(i) for i in str(survive_list)] #survive list is a list of all survive rules aka S312=[3,1,2]


        ones_board = np.ones(shape=(self.size_of_board+2,self.size_of_board+2))

        for t in range(self.size_of_board):   #shora
            for r in range(self.size_of_board): #amoda
                x=self.Board[t+1][r+1]  # the element that we run on the matrix
                if x  == 0:  
                    counter =0
                    if self.Board[t+1][r+2] == 255:
                        counter = counter +1
                    if self.Board[t+2][r+2] == 255:
                        counter = counter +1
                    if self.Board[t+2][r+1] == 255:
                        counter = counter +1
                    if self.Board[t+2][r] == 255:
                        counter = counter +1
                    if self.Board[t+1][r] == 255:
                        counter = counter +1
                    if self.Board[t][r] == 255:
                        counter = counter +1
                    if self.Board[t][r+1] == 255:
                        counter = counter +1
                    if self.Board[t][r+2] == 255:
                        counter = counter +1  #counter is the number of alive cells near a dean one
                    

                    for i in born_list:
                        if counter == i:
                            ones_board[t+1,r+1]=255   # put the element in a new matrix as an 255
                            break    
                        else:
                            ones_board[t+1,r+1]= 0    #put the element in a new matrix as an 0     ********te of running timee!!

                else:
                    counter =0
                    if self.Board[t+1][r+2] == 255:
                        counter = counter +1
                    if self.Board[t+2][r+2] == 255:
                        counter = counter +1
                    if self.Board[t+2][r+1] == 255:
                        counter = counter +1
                    if self.Board[t+2][r] == 255:
                        counter = counter +1
                    if self.Board[t+1][r] == 255:
                        counter = counter +1
                    if self.Board[t][r] == 255:
                        counter = counter +1
                    if self.Board[t][r+1] == 255:
                        counter = counter +1
                    if self.Board[t][r+2] == 255:
                        counter = counter +1  #counter is the number of alive cells near a dean one
                    

                    for i in survive_list:
                        if counter == i:
                            ones_board[t+1,r+1]=255   # put the element in a new matrix as an 255
                            break    
                        else: 
                            ones_board[t+1,r+1]= 0    #put the element in a new matrix as an 0     
        self.Board=ones_board
        #updated_board=ones_board
        #return updated_board

    def save_board_to_file(self, file_name):
        board = self.Board
        board=np.delete(board,0, 1)
        board=np.delete(board,self.size_of_board, 1)
        board=np.delete(board,0, 0)
        board=np.delete(board,self.size_of_board, 0)
        plt.imsave(file_name,board)  # i put return_board, duble check it!!!!

    def display_board(self):
        board = self.Board
        board=np.delete(board,0, 1)
        board=np.delete(board,self.size_of_board, 1)
        board=np.delete(board,0, 0)
        board=np.delete(board,self.size_of_board, 0)        
        return plt.show(plt.matshow(board))

    def return_board(self):
        board = self.Board
        board=np.delete(board,0, 1)
        board=np.delete(board,self.size_of_board, 1)
        board=np.delete(board,0, 0)
        board=np.delete(board,self.size_of_board, 0)
        return board.tolist()








if __name__ == '__main__':  # You should keep this line for our auto-grading code.
	start_time = time.time()
	B=GameOfLife(17,5,'​​B2/S0')
	i=0
	while i < 0:
		i=i+1
		B.update()
		B.save_board_to_file(str(i)+'pipi.png')
	B.save_board_to_file(str(i)+'pipi.png')
	print("--- %s seconds ---" % (time.time() - start_time))
	B.display_board()
	board = B.return_board()
	print(board)