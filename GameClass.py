import ChessPieces
import copy
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
        self.history=[]
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
        if(self.state==-1):#if black play check white move
            piecesList=self.blackPiecesList
            movesList.extend(self.theoryPossibleMove("White"))
        else:
            piecesList=self.whitePiecesList
            movesList.extend(self.theoryPossibleMove("Black"))
        for piece in piecesList:
            if(piece.__class__.__name__=="King"):
                kingPosition=(piece.x,piece.y)
                break
        for moves in movesList:
            if(kingPosition==(moves[0],moves[1])):
                    attackingPiecesList.append(moves[2])
        return attackingPiecesList
    def boardPossibleMoves(self,colorPlay):
        movesList=self.theoryPossibleMove(colorPlay)
        possibleMovesList=[]
        attackerList=self.echec()
        piecesList=[]
        if(colorPlay=="White"):#White have to play
            piecesList=self.whitePiecesList
        else:
            piecesList=self.blackPiecesList
        if(attackerList!=[]):
            kingPosition=(-1,-1)
            for piece in piecesList:
                if(type(piece)==ChessPieces.King):
                    kingPosition=(piece.x,piece.y)
                    break
            #add only the moves that defend the king
           
            for move in movesList:
                for attacker in attackerList:
                    if(move[0]==attacker.x and move[1]==attacker.y):
                        possibleMovesList.append(move)
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
                    for move in movesList:
                        if(move[0]==attacker.x and (move[0]-attacker.x)*horizontalAdvance<0):
                            possibleMovesList.append(move)
                elif(kingPosition[1]==attacker.y):#attacker attack on line horizontal
                    for move in movesList:
                        if(move[1]==attacker.y and (move[1]-attacker.y)*verticalAdvance<0):
                            possibleMovesList.append(move)
            
                else:#attack on diagonal
                    DangerZone=[]
                    #Diagonal
                    for i,j in zip(range(kingPosition[0]+1,attacker.x,horizontalAdvance),
                                    range(kingPosition[1]+1,attacker.y,verticalAdvance)):

                        if(piecesList[0].moveChecker(i,j,DangerZone)):
                            break
                    for move in movesList:
                        for dangerMove in DangerZone:
                            if(move[0]==dangerMove[0] and move[1]==dangerMove[1]):
                                possibleMovesList.append(move)
        else:
            possibleMovesList=movesList
        #Verifier que les mouvements ne créer pas d'échec
        #for move in possibleMovesList:
         #   predictionBoard=self
          #  predictionBoard.movePieces(move,possibleMovesList)
          #  if(predictionBoard.echec()!=[]):
           #     print(move)
             #   print(self.state)
                #possibleMovesList.remove(move)
        return possibleMovesList
    def movePieces(self,moves,movesList):#moves is the a tuple from movesList
        endingMove=moves
        startingMove=(moves[2].x,moves[2].y,moves[2])
        checkingMove=False
        #numberOfMoves=0
        eatingMove=False
        #Checking unique moves
        #for move in movesList:
         #   if(moves[0]==move[0] and moves[1]==move[1]):
          #      numberOfMoves+=1
        #uniqueMove=numberOfMoves==1

        movedPiece=self.board[moves[1]][moves[0]]
        #Checking eating move
        if(type(movedPiece)!=ChessPieces.Cases):
            eatingMove=True
            if(self.state==-1):
                self.whitePiecesList.remove(movedPiece)
            else:
                self.blackPiecesList.remove(movedPiece)
        else:
            if(movedPiece.passantCase):
                eatingMove=True
                if(self.state==-1):
                    passedPiece=self.board[movedPiece.y-1][movedPiece.x]
                    self.whitePiecesList.remove(passedPiece)
                else:
                    passedPiece=self.board[movedPiece.y+1][movedPiece.x]
                    self.blackPiecesList.remove(passedPiece)
                self.board[passedPiece.y][passedPiece.x]=ChessPieces.Cases(passedPiece.y,passedPiece.x)
        #Rendre vide la case de depart
        self.board[moves[2].y][moves[2].x]=ChessPieces.Cases(moves[2].y,moves[2].x)
        #Promotion move
        listOfPromotion=[ChessPieces.Queen,ChessPieces.Bishop,ChessPieces.Rook,ChessPieces.Knight]
        promotionResponse=0
        if(moves[2].y==0 and moves[2].color=="White" and type(moves[2])==ChessPieces.Pawn):
            self.whitePiecesList.remove(moves[2])
            print("Choose a promotion :{}",[str(i) for i in listOfPromotion])
            promotionResponse=int(input("Choose a number:"))
            newPiece=listOfPromotion[promotionResponse](self,moves[2].x,moves[2].y,"White")
            self.whitePiecesList.append(newPiece)
            self.board[moves[2].y][moves[2].x]=newPiece
        elif(moves[2].y==7 and moves[2].color=="Black" and type(moves[2])==ChessPieces.Pawn):
            self.blackPiecesList.remove(moves[2])
            print("Choose a promotion :{}",[str(i) for i in listOfPromotion])
            promotionResponse=int(input("Choose a number:"))
            newPiece=listOfPromotion[promotionResponse](self,moves[2].x,moves[2].y,"Black")
            self.whitePiecesList.append(newPiece)
            self.board[moves[2].y][moves[2].x]=newPiece
        #acting move
        moves[2].move(moves[0],moves[1])
        self.board[moves[1]][moves[0]]=moves[2]
        if(type(moves[2])==ChessPieces.Pawn):
            if(moves[2].passant[0]):
                self.board[moves[2].y][moves[2].x].passantCase=True
        #Checking moves
        if(self.echec()!=[]):
            checkingMove=True
        self.history.append((startingMove,endingMove,checkingMove,eatingMove))
    def terminal_test(self):
        if(self.state==-1):
            colorPlay="Black"
        else:
            colorPlay="White"
        boardMoves=self.boardPossibleMoves(colorPlay)
        if(boardMoves==[]):
            print("Partie terminé")
            print("Nombres de tours :{}".format(self.turn))
            print("Victoire de {}".format(self.state*(-1)))
            print(self.echec()[0].color)
            return True
        return False
    def startTheGame(self):
        while(not self.terminal_test()):
            self.showBoard()
            if(self.state==-1):
                colorPlay="Black"
            else:
                colorPlay="White"
            movesList=self.boardPossibleMoves(colorPlay)
            movesListStr=[(i[0],i[1],str(i[2])) for i in movesList]
            print(movesListStr)
            print(len(movesListStr))
            chooseMove=int(input("Which move do you chose ?"))
            #chooseMove=0
            if(self.state==1):##White have to play
                self.movePieces(movesList[chooseMove],movesList)
            elif(self.state==-1):##Black have to play
                self.movePieces(movesList[chooseMove],movesList)
            self.state=self.state*(-1)
            self.turn+=1
            self.writeHistory()
    def showBoard(self):
        print([str(i) for i in range(8)])
        i=0
        for rows in self.board:
            print([str(i) for i in rows],end=" ")
            print(i)
            i+=1
    def loadHistory(self,history):
        pass
    def writeHistory(self):
        event=""
        site=""
        date=""
        round=self.turn
        white=""
        black=""
        result="*"
        turn=1
        moveNumber=1
        algebricNotation={
            ChessPieces.Bishop.__name__:"B",
            ChessPieces.Rook.__name__:"R",
            ChessPieces.Queen.__name__:"Q",
            ChessPieces.King.__name__:"K",
            ChessPieces.Knight.__name__:"N",
            ChessPieces.Pawn.__name__:""
        }
        with open("history.pgn","w") as historyFile:
            #HEAD
            historyFile.write("[Event {}]\n".format(event))
            historyFile.write("[Site {}]\n".format(site))
            historyFile.write("[Date {}]\n".format(date))
            historyFile.write("[Round {}]\n".format(round))
            historyFile.write("[White {}]\n".format(white))
            historyFile.write("[Black {}]\n".format(black))
            historyFile.write("[Result {}]\n".format(result))
            #BODY
            for move in self.history:
                #move form(startingMove,endingMove,checkingMove,eatingMove)
                if(moveNumber%2!=0):
                    historyFile.write("{}. ".format(turn))
                    turn+=1
                if(move[3]):
                    if(type(move[1][2])==ChessPieces.Pawn):
                        historyFile.write("{}x ".format(chr(move[0][0]+97)))
                    else:
                        historyFile.write("{}x".format(algebricNotation[move[1][2].__class__.__name__]))
                    historyFile.write("{}{} ".format(chr(move[1][0]+97),move[1][1]+1))
                else:
                    historyFile.write("{}".format(algebricNotation[move[1][2].__class__.__name__]))
                    historyFile.write("{}{} ".format(chr(move[1][0]+97),move[1][1]+1))
                if(move[2]):#Checking move
                    historyFile.write("+")
                moveNumber+=1
                
                
        print(self.history)
chess=ChessBoard()

chess.startTheGame()
chess.showBoard()