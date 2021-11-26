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
            movesList.append((x,y,self))
        elif(self.chessBoard.board[y][x].color!=self.color):
            movesList.append((x,y,self))
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

        #Removes cases that are attacked
        opposingMovesList=[]
        if(self.chessBoard.state==1):
            piecesList=self.chessBoard.whitePiecesList
        else:
            piecesList=self.chessBoard.blackPiecesList
        piecesList.remove(self)
        for piece in self.chessBoard.whitePiecesList:
            opposingMovesList.extend(piece.possibleMove())
        for kingMove in movesList:
            for attackerMove in opposingMovesList:
                if((kingMove[0],kingMove[1])==(attackerMove[0],attackerMove[1])):
                    movesList.remove(kingMove)
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
                    #movesList.remove((i,self.y+(j*avance),self))
                    pass

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