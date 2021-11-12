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
        for i in range((self.y)+1,8):
            if(self.moveChecker(self.x,i,movesList)):
                break
        #Descendant
        for i in range(0,self.y):
            if(self.moveChecker(self.x,i,movesList)):
                break
        #Déplacement horizontale ascendant
        for j in range(self.x+1,8):
            if(self.moveChecker(j,self.y,movesList)):
                break
        #Déscendant
        for j in range(0,self.x):
            if(self.moveChecker(j,self.y,movesList)):
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
        
        return super().possibleMove()
    def __str__(self):
        return super().__str__()
class Pawn(ChessPiece):
    unicodeCharBlack="\u265F"
    unicodeCharWhite="\u2659"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class Knight(ChessPiece):
    unicodeCharBlack="\u265E"
    unicodeCharWhite="\u2658"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
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
        
    def terminal_test(self):
        pass
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
chess.board[1][0]=Cases(1,0)
chess.board[5][3]=King(chess,5,3,"Black")
chess.board[6][3]=Pawn(chess,6,3,"Black")
print("*"*20)
chess.showBoard()

print(chess.board[5][3].possibleMove())
