import ChessPieces
class ChessBoard(): 
    def __init__(self):
        self.state=1# -1 Black : 1 White -> state white have to play
        self.turn=1
        self.board=[[ChessPieces.Cases(j,i) for i in range(8)] for j in range(8)]
        #Filling the board
        for i in range(8):
            self.board[1][i]=ChessPieces.Pawn(self,1,i,"Black")
            self.board[6][i]=ChessPieces.Pawn(self,6,i,"White")
        l=[ChessPieces.Rook,ChessPieces.Knight,ChessPieces.Bishop]
        for i in range(3):
            self.board[0][i]=l[i](self,0,i,"Black")
            self.board[0][-(i+1)]=l[i](self,0,8-(i+1),"Black")
            self.board[-1][-(i+1)]=l[i](self,8-1,8-(i+1),"White")
            self.board[-1][i]=l[i](self,8-1,i,"White")
        self.board[0][3]=ChessPieces.Queen(self,0,3,"Black")
        self.board[0][4]=ChessPieces.King(self,0,4,"Black")
        self.board[-1][3]=ChessPieces.Queen(self,8-1,3,"White")
        self.board[-1][4]=ChessPieces.King(self,8-1,4,"White")
        self.blackPiecesList=[]
        self.whitePiecesList=[]
        #complete black list pieces
        for i in range(8):
            for j in range(2):
                self.blackPiecesList.append(self.board[j][i])
        #complete white list pieces
        for i in range(8):
            for j in range(6,8):
                self.whitePiecesList.append(self.board[j][i])
        
    def theoryPossibleMove(self,color):
        movesList=[]
        if(color=="Black"):
            for piece in self.blackPiecesList:
                movesList.extend(piece.possibleMove())
        else:
            for piece in self.whitePiecesList:
                movesList.extend(piece.possibleMove())
        return movesList
    def echec(self):
       # ECHEC
        kingPosition=(0,0)
        attackingPiecesList=[]
        piecesList=[]
        movesList=[]
        if(self.state==-1):#Black
            piecesList=self.blackPiecesList
            movesList=self.theoryPossibleMove("Black")
        else:
            piecesList=self.whitePiecesList
            movesList=self.theoryPossibleMove("White")
        for piece in piecesList:
            if(piece==ChessPieces.King):
                kingPosition=(piece.x,piece.y)
                break
        for moves in movesList:
            if(kingPosition==(moves[0],moves[1])):
                    attackingPiecesList.append(moves[2])
        return attackingPiecesList
    def possibleMove(self):
        if(self.state==-1):
            colorPlay="Black"
        else:
            colorPlay="White"
        movesList=self.theoryPossibleMove(colorPlay)
        possibleMovesList=[]
        attackerList=self.echec()
        piecesList=[]
        if(self.state==1):#White have to play
            piecesList=self.whitePiecesList
        else:
            piecesList=self.blackPiecesList
        if(attackerList!=[]):
            for piece in piecesList:
                if(piece==ChessPieces.King):
                    kingPosition=(piece.x,piece.y)
            #add only the moves that defend the king
            for attacker in attackerList:
                horizontalAdvance=0
                verticalAdvance=0
                if((kingPosition[0]-attacker.x)<0):
                    horizontalAdvance=1
                else:
                    horizontalAdvance=-1
                if((kingPosition[1]-attacker.y)<0):
                    verticalAdvance=1
                else:
                    verticalAdvance=-1
                if(kingPosition[0]==attacker.x):#attacker attack on line vertical
                    verticalDangerZone=[]
                    for move in movesList:
                        if(move[0]==attacker.x and (move[0]-attacker.x)*horizontalAdvance<=0):
                            possibleMovesList.append(move)
                elif(kingPosition[1]==attacker.y):#attacker attack on line horizontal
                    for move in movesList:
                        if(move[1]==attacker.y and (move[1]-attacker.y)*verticalAdvance<=0):
                            possibleMovesList.append(move)
            
                else:#attack on diagonal
                    diagonalDangerZone=[]
                    
                    for i,j in zip(range(kingPosition[0]+1,attacker.x,horizontalAdvance),
                                    range(kingPosition[1]+1,attacker.y,verticalAdvance)):
                        if(self.moveChecker(i,j,diagonalDangerZone)):
                            break
                    for move in movesList:
                        for dangerMove in diagonalDangerZone:
                            if(move[0]==dangerMove[0 and move[1]==dangerMove[1]]):
                                possibleMovesList.append(move)
        else:
            return movesList
        return possibleMovesList
    def movePieces(self,moves):#moves is the a tuple from movesList
        self.board[moves[2].y][moves[2].x]=ChessPieces.Cases()
        moves[2].move(moves[0],moves[1])
        self.board[moves[1]][moves[0]]=moves[2]
    def terminal_test(self):
        if(self.possibleMove()==[]):
            print("Partie terminé")
            return True
        return False
    def startTheGame(self):
        while(not self.terminal_test()):
            movesList=self.possibleMove()
            print(movesList)
            #chooseMove=int(input("Which move do you chose ?"))
            chooseMove=0
            if(self.state==1):##White have to play
                self.movePieces(movesList[chooseMove])
            elif(self.state==-1):##Black have to play
                self.movePieces(movesList[chooseMove])
            self.state*=-1
    def showBoard(self):
        print([str(i) for i in range(8)])
        i=0
        for rows in self.board:
            print([str(i) for i in rows],end=" ")
            print(i)
            i+=1
chess=ChessBoard()

chess.startTheGame()