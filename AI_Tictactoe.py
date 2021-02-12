import random
import copy

'''
    *** DESCIPTION ***
    Welcome to my TicTacToe AI using reinforcement learning ! 
    The experience of the AI is contained in a dictionary (dict type). To get experience, the AI plays thousands games in random-moves mode and saves all of them.
    Then, a value is associated with each move, as a reward. Higher the move's importance is, higher is the reward.
    To play, follow the instructions after running the program. You can setup parameters : the learning rate and the number of traning games, follow the #.
    
    Enjoy ! 
'''

class Board :

    def __init__(self):
        self.board = [["-","-","-"],["-","-","-"],["-","-","-"]]
    
    def Display_Board(self):
        for i in self.board :
            print(i)

    def Reset(self):
        self.board = [['-','-','-'],['-','-','-'],['-','-','-']]
        return board
    
    def Check_Full(self):
        for i in self.board :
            if '-' in i :
                return False
        return True
    
    def Check_Winner(self):
        #Check lines and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "-":
                return True
            elif self.board[0][i] == self.board[1][i] == self.board[2][i] != "-":
                return True
        #Check diagonals
        return (self.board[0][0] == self.board[1][1] == self.board[2][2] != "-") or (self.board[0][2] == self.board[1][1] == self.board[2][0] != "-")

    def Update_Board(self, symbol, coord):
        self.board[coord[0]][coord[1]] = symbol

class Player :
    
    def __init__(self, symbol, isHuman = False, isIntelligent = False, experience = {}, learningRate = 0.1):
        self.symbol = symbol
        self.isHuman = isHuman
        self.isIntelligent = isIntelligent
        self.experience = experience
        self.learningRate = learningRate
        self.gameHistory = []

    def Display_Experience(self):
        print('-------------------------- EXPERIENCE --------------------------')
        for state,value in self.experience.items():
            print('State : {}, Value : {}'.format(state,value))

    def reward(self):
        if self.symbol == 'X' :
            return 1
        else : return -1

    def Human_Turn(self, board):
        X = (int(input("Entrez la ligne à laquelle vous voulez jouer (1 à 3): ")) -1)%3
        Y = (int(input("Entrez la colonne à laquelle vous voulez jouer (1 à 3): ")) -1)%3
        if board[X][Y] != '-' :
            print("Cette case est déjà pleine, choisissez une autre case : ")
            X,Y = self.Human_Turn(board)
        return X,Y
    
    def Random_Turn(self,board) :
        X = random.randint(0,2)
        Y = random.randint(0,2)
        if board[X][Y] != "-" :
            X,Y = self.Random_Turn(board)
        return X,Y

    def Get_Possible_Moves(self,board):
        possibleMoves = []
        for i in range(3) :
            for j in range(3) :
                if board[i][j] == '-' :
                    possibleMoves.append((i,j))
        return possibleMoves

    def Best_Move(self, board):
        possibleMoves = self.Get_Possible_Moves(board)
        
        #------ Security if there is no move in experience ------# 
        bestMove = random.choice(possibleMoves)
        bestScore = -1
        #--------------------------------------------------------#  
        
        for move in possibleMoves :
            boardCopy = copy.deepcopy(board)
            boardCopy[move[0]][move[1]] = self.symbol
            if str(boardCopy) not in self.experience :
                continue
            if self.experience[str(boardCopy)] > bestScore :
                bestScore = self.experience[str(boardCopy)]
                bestMove = move
        return bestMove

    def Turn(self,board):
        if self.isHuman : 
            return self.Human_Turn(board)
        elif self.isIntelligent :
            return self.Best_Move(board)                 
        else : return self.Random_Turn(board)

    def Experience_Saving(self,reward):
        '''
            Here is the most important part of this program : save the experience and associate a reward to each move
            The last move is always important, the according reward is proportionnal to its importance.
            Then, the previous move will receive a less significant reward, because it is less decisive.
        '''
        actionValue = reward
        for state in reversed(self.gameHistory) :
            if state not in self.experience :
                self.experience[state] = 0
            actionValue = self.experience[state] + self.learningRate*(actionValue-self.experience[state])
            self.experience[state] = actionValue

def PlayTicTacToe(p1, p2, aiTraining = False):
    players = [p1,p2]
    random.shuffle(players)
    i = 0                                           # i symbolize the current player
    reward = 0
    board = Board()
                 
    while True :

        if players[i].isHuman or players[i].isHuman :
            print('--- {} is playing ---'.format(players[i].symbol))
            board.Display_Board()
          
        X,Y = (players[i]).Turn(board.board)
        board.Update_Board(players[i].symbol, (X,Y))
        players[i].gameHistory.append(str(board.board))
        
        if board.Check_Winner() :
            if players[i].isHuman or players[(i+1)%2].isHuman :
                print("- {} wins -".format(players[i].symbol))
                print('------ GAME OVER ------')
            reward = 1
            break
        
        elif board.Check_Full():
            if players[i].isHuman or players[(i+1)%2].isHuman :
                print("-------- DRAW ---------")
                print('------ GAME OVER ------')
            reward = 0
            break
        i = (i+1)%2

    if aiTraining :
        players[i].Experience_Saving(reward)
        players[(i+1)%2].Experience_Saving(-reward)
    p1.gameHistory = []
    p2.gameHistory = []

    return players[i]

def WinningRate(myExperience):
    nbWins = 0
    for i in range(1000) :
        role = [True, False]
        random.shuffle(role)
        p1 = Player('X', isIntelligent = role[0], experience = myExperience)
        p2 = Player('O', isIntelligent = role[1], experience = myExperience)
        winner = copy.deepcopy(PlayTicTacToe(p1,p2))
        if winner.isIntelligent :
            nbWins += 1
    print('The winning rate is : ', nbWins/10, '%')
    return nbWins



if __name__ == "__main__":
    print('----- WELCOME TO MY AI-TICTACTOE-PROGRAM -----', end='\n\n')

    mode = int(input("Entrez 0 pour jouer contre un humain, 1 contre une IA : "))%2

    if mode == 0 :
        p1 = Player('X', isHuman = True)
        p2 = Player('O', isHuman = True)
        PlayTicTacToe(p1,p2)
    else :
        p1 = Player('X', isIntelligent = False, learningRate = 0.1)         # You can change the learning rate of each symbol
        p2 = Player('O', isIntelligent = False, learningRate = 0.1)         # There will be consequences in the Winning Rate
        print('Start training ... (it can be long)')
        for i in range(10000) :                                             # You can change the nb of training games : the higher it is, the higher will be the Winning Rate
            PlayTicTacToe(p1,p2, aiTraining = True)
        p1.experience.update(p2.experience)
        aiExperience = copy.deepcopy(p1.experience)
        #p1.Display_Experience()                        # ---> it's is now p1 and p2 experience
        WinningRate(aiExperience)

        p1 = Player('X', isIntelligent = False)
        p2 = Player('O', isIntelligent = False)
        while True : 
            role = [True, False]
            random.shuffle([True, False])
            p1 = Player('X', isHuman = role[0], isIntelligent = True, experience = aiExperience)
            p2 = Player('O', isHuman = role[1], isIntelligent = True, experience = aiExperience)
            PlayTicTacToe(p1,p2)
            playAgain = input("Press 1 to play again : ")
            if playAgain != '1' :
                break
        print('Thanks for playing !')






