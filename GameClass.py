class ChessPiece():
    unicodeCharBlack="\u25A0"
    unicodeCharWhite="\u25A1"
    def __init__(self,chessBoard,positionY,positionX,color) -> None:
        self.chessBoard=chessBoard
        self.color=color
        self.x=positionX
        self.y=positionY
    def possibleMove(self):
        pass
    def move(self,positionX,positionY):
        self.x=positionX
        self.y=positionY
    def moveChecker(self,x,y,movesList):
        stopMove=False
        #3 cas (1): Cases vides / (2) :pion allié / (3):pion ennemi
        if(type(self.chessBoard.board[y][x])==Cases):
            movesList.append((x,y))
        elif(self.chessBoard.board[y][x].color!=self.color):
            movesList.append((x,y))
            stopMove=True
        else:
            stopMove=True
        return stopMove
    def __str__(self):
        if(self.color=="Black"):
            return self.unicodeCharBlack
        else:
            return self.unicodeCharWhite
class Cases():
    unicodeCharBlack="\u25A0"
    unicodeCharWhite="\u25A1"
    def __init__(self,positionY,positionX):
        self.x=positionX
        self.y=positionY
        if((positionY+positionX)%2==0):
            self.color="White"
        else:
            self.color="Black"
    def __str__(self):
        if(self.color=="Black"):
            return self.unicodeCharBlack
        else:
            return self.unicodeCharWhite
class Rook(ChessPiece):
    unicodeCharBlack="\u265C"
    unicodeCharWhite="\u2656"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
        
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def possibleMove(self):
        movesList=[]
        #Déplacement verticale ascendant
        for j in range((self.y)+1,8):
            if(self.moveChecker(self.x,j,movesList)):
                break
        #Descendant
        for j in range(self.y,-1,-1):
            if(self.moveChecker(self.x,j,movesList)):
                break
        #Déplacement horizontale ascendant
        for i in range(self.x+1,8):
            if(self.moveChecker(i,self.y,movesList)):
                break
        #Déscendant
        for i in range(self.x,-1,-1):
            if(self.moveChecker(i,self.y,movesList)):
                break
        return movesList
    def __str__(self):
        return super().__str__()
class King(ChessPiece):
    unicodeCharBlack="\u265A"
    unicodeCharWhite="\u2654"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        
        return super().move(positionX, positionY)
    def possibleMove(self):
        movesList=[]
        #C'est toute les cases théoriques où le roi peut se déplacer
        theoryMoves=[]
        for i in range(self.x-1,self.x+2):
            for j in range(self.y-1,self.y+2):
                theoryMoves.append((i,j))
        theoryMoves=[i for i in theoryMoves if i[0]>=0 and i[0]<8 and i[1]>=0 and i[1]<8]
        for move in theoryMoves:
            self.moveChecker(move[0],move[1],movesList)
        return movesList
    def __str__(self):
        return super().__str__()
class Queen(ChessPiece):
    unicodeCharBlack="\u265A"
    unicodeCharWhite="\u2655"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)

    def possibleMove(self):
        movesList=[]
        #Déplacement verticale ascendant
        for j in range((self.y)+1,8):
            if(self.moveChecker(self.x,j,movesList)):
                break
        #Descendant
        for j in range(self.y,-1,-1):
            if(self.moveChecker(self.x,j,movesList)):
                break
        #Déplacement horizontale ascendant
        for i in range(self.x+1,8):
            if(self.moveChecker(i,self.y,movesList)):
                break
        #Déscendant
        for i in range(self.x,-1,-1):
            if(self.moveChecker(i,self.y,movesList)):
                break
        #diagonale haut droite
        for i,j in zip(range(self.x+1,8),range(self.y+1,8)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal bas gauche
        for i,j in zip(range(self.x-1,-1,-1),range(self.y-1,-1,-1)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal bas droite
        for i,j in zip(range(self.x-1,-1,-1),range(self.y+1,8)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal haut gauche
        for i,j in zip(range(self.x+1,8),range(self.y-1,-1,-1)):
            if(self.moveChecker(i,j,movesList)):
                break
        return movesList
        
    def __str__(self):
        return super().__str__()
class Bishop(ChessPiece):
    unicodeCharBlack="\u265D"
    unicodeCharWhite="\u2657"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)

    def possibleMove(self):
        movesList=[]
        #diagonale haut droite
        for i,j in zip(range(self.x+1,8),range(self.y+1,8)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal bas gauche
        for i,j in zip(range(self.x-1,-1,-1),range(self.y-1,-1,-1)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal bas droite
        for i,j in zip(range(self.x-1,-1,-1),range(self.y+1,8)):
            if(self.moveChecker(i,j,movesList)):
                break
        #diagonal haut gauche
        for i,j in zip(range(self.x+1,8),range(self.y-1,-1,-1)):
            if(self.moveChecker(i,j,movesList)):
                break
        return movesList
    def __str__(self):
        return super().__str__()
class Pawn(ChessPiece):
    unicodeCharBlack="\u265F"
    unicodeCharWhite="\u2659"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
        self.moved=False
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def possibleMove(self):
        movesList=[]
        avance=1
        numberMoveCase=1
        if(not self.moved):
            numberMoveCase=2
        if(self.color=="White"):
            avance=-1
        start=self.x-1
        end=self.x+1
        if(start<0):
            start=self.x
        if(end>8-1):
            end=self.x
        for i in range(start,end+1):
            for j in range(1,numberMoveCase+1):
                self.moveChecker(i,self.y+(j*avance),movesList)
                if(self.x!=i and type(self.chessBoard.board[self.y+(j*avance)][i])==Cases):
                    movesList.remove((i,self.y+(j*avance)))

        return movesList
    def __str__(self):
        return super().__str__()
class Knight(ChessPiece):
    unicodeCharBlack="\u265E"
    unicodeCharWhite="\u2658"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def possibleMove(self):
        movesList=[]
        theoryMoves=[
            (self.x+1,self.y+2),
            (self.x-1,self.y+2),
            (self.x+2,self.y+1),
            (self.x+2,self.y-1)
        ]
        theoryMoves=[i for i in theoryMoves if i[0]>=0 and i[0]<8 and i[1]>=0 and i[1]<8]
        for move in theoryMoves:
            self.moveChecker(move[0],move[1],movesList)
        return movesList
    def __str__(self):
        return super().__str__()
class ChessBoard(): 
    def __init__(self):
        self.state=1# 0 Black : 1 White -> state white have to play
        self.turn=1
        self.board=[[Cases(j,i) for i in range(8)] for j in range(8)]
        #Filling the board
        for i in range(8):
            self.board[1][i]=Pawn(self,1,i,"Black")
            self.board[6][i]=Pawn(self,6,i,"White")
        l=[Rook,Knight,Bishop]
        for i in range(3):
            self.board[0][i]=l[i](self,0,i,"Black")
            self.board[0][-(i+1)]=l[i](self,0,8-(i+1),"Black")
            self.board[-1][-(i+1)]=l[i](self,8-1,8-(i+1),"White")
            self.board[-1][i]=l[i](self,8-1,i,"White")
        self.board[0][3]=Queen(self,0,3,"Black")
        self.board[0][4]=King(self,0,4,"Black")
        self.board[-1][3]=Queen(self,8-1,3,"White")
        self.board[-1][4]=King(self,8-1,4,"White")
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
        print(self.blackPiecesList)
    def theoryPossibleMove(self,color):
        movesList=[]
        if(color=="Black"):
            for piece in self.blackPiecesList:
                movesList.extend(piece.possibleMove())
        else:
            for piece in self.whitePiecesList:
                movesList.extend(piece.possibleMove())
        if(self.echec()):
            pass
        return movesList
    def echec(self):
       # ECHEC
        kingPosition=(0,0)
        if(self.state==0):#Black
            for piece in self.blackPiecesList:
                if(piece==King):
                    kingPosition=(piece.x,piece.y)
            movesList=self.theoryPossibleMove("White")
            if(kingPosition in movesList):
                return True
        else:
            movesList=self.theoryPossibleMove("Black")
            for piece in self.whitePiecesList:
                if(piece==King):
                    kingPosition=(piece.x,piece.y)
            if(kingPosition in movesList):
                return True
        return False
    def possibleMove(self):
        movesList=self.theoryPossibleMove()
        if(self.echec()):
            #remove all the actiions that don't defend the king
            pass
        return movesList
    def startTheGame(self):
        while(not self.terminal_test()):
            if(self.state==1):##White have to play
                pass
            elif(self.state==0):##Black have to play
                pass
    def showBoard(self):
        print([str(i) for i in range(8)])
        i=0
        for rows in self.board:
            print([str(i) for i in rows],end=" ")
            print(i)
            i+=1
chess=ChessBoard()
chess.showBoard()
print(len(chess.possibleMove("Black")))
print(chess.possibleMove("Black"))