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
        if(x>7 or x<0 or y<0 or y>7):
            return True
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
    def __eq__(self, other):
        return self.x==other.x and self.y==other.y and self.__class__.__name__==other.__class__.__name__
class Cases():
    unicodeCharBlack="\u25A0"
    unicodeCharWhite="\u25A1"
    def __init__(self,positionY,positionX,passantCase=[False,1]):
        self.x=positionX
        self.y=positionY
        self.passantCase=passantCase
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
        self.moved=False
        
    def move(self, positionX, positionY):
        self.moved=True
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
    def __eq__(self, other):
        return super().__eq__(other)
class King(ChessPiece):
    unicodeCharBlack="\u265A"
    unicodeCharWhite="\u2654"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
        self.moved=False
    def move(self, positionX, positionY):
        self.moved=True
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
        piecesList=[]
        if(self.chessBoard.state==-1):
            piecesList.extend(self.chessBoard.whitePiecesList)
        else:
            piecesList.extend(self.chessBoard.blackPiecesList)
        for piece in piecesList:
            if(type(piece)==King):
                piecesList.remove(piece)
        for piece in piecesList:
            opposingMovesList.extend(piece.possibleMove())
        movesList2=[]
        movesList2.extend(movesList)
        for kingMove in movesList:
            for attackerMove in opposingMovesList:
                if(kingMove[0]==attackerMove[0] and kingMove[1]==attackerMove[1]):
                    movesList2.remove(kingMove)
                    break

        #Castling
        if(not self.moved):
            #Check small castling
            smallVide=True
            controlled=False
            for i in range(self.x+1,7):
                if(type(self.chessBoard.board[self.y][i])!=Cases):
                    smallVide=False
                    break
            if(type(self.chessBoard.board[self.y][7])==Rook and not(self.chessBoard.board[self.y][7].moved) and smallVide):
                #Verifier que les ennemis de controle pas la zone
                for i in range(self.x,7):
                    for attackerMove in opposingMovesList:
                        if(attackerMove[0]==i and attackerMove[1]==self.y):
                            controlled=True
                            break
                if(not controlled):
                    movesList2.append((self.x+2,self.y,self))
            #Check big castling
            bigVide=True
            controlled=False
            for i in range(self.x-1,0,-1):
                print(i)
                if(type(self.chessBoard.board[self.y][i])!=Cases):
                    bigVide=False
                    break
            if(type(self.chessBoard.board[self.y][0])==Rook and not(self.chessBoard.board[self.y][0].moved) and bigVide):
                #Verifier que les ennemis de controle pas la zone
                for i in range(self.x,0,-1):
                    for attackerMove in opposingMovesList:
                        if(attackerMove[0]==i and attackerMove[1]==self.y):
                            controlled=True
                            break
                if(not controlled):
                    movesList2.append((self.x-2,self.y,self))
            
        return movesList2
    def __str__(self):
        return super().__str__()
    def __eq__(self, other):
        return super().__eq__(other)
class Queen(ChessPiece):
    unicodeCharBlack="\u265B"
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
    def __eq__(self, other):
        return super().__eq__(other)
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
    def __eq__(self, other):
        return super().__eq__(other)
class Pawn(ChessPiece):
    unicodeCharBlack="\u265F"
    unicodeCharWhite="\u2659"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
        self.moved=False
        self.passant=[False,1]
    def move(self, positionX, positionY):
        self.moved=True
        if(abs(self.y-positionY)==2):
            self.passant=[True,self.chessBoard.turn]
        else:
            self.passant=[False,self.chessBoard.turn]
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
        if(self.y==7 or self.y==0):
            numberMoveCase=0
        for i in range(start,end+1):
            for j in range(1,numberMoveCase+1):
                if(self.x!=i and type(self.chessBoard.board[self.y+(j*avance)][i])==Cases):#Ne pas inclure les moves diagonales sans ennemis
                    break
                elif(self.x==i and type(self.chessBoard.board[self.y+(j*avance)][i])!=Cases):
                    break
                else:
                    self.moveChecker(i,(self.y+(j*avance)),movesList)
       #Coup en passant
        if(self.x-1>=0):
            leftPawn=self.chessBoard.board[self.y][self.x-1]
            if(type(leftPawn)==Pawn):
                if(leftPawn.passant[0] and (leftPawn.passant[1]+1)==self.chessBoard.turn):
                    movesList.append((self.x-1,self.y+avance,self))
        if(self.x+1<8):
            rightPawn=self.chessBoard.board[self.y][self.x+1]
            if(type(rightPawn)==Pawn):
                if(rightPawn.passant[0] and (rightPawn.passant[1]+1)==self.chessBoard.turn):
                    movesList.append((self.x+1,self.y+avance,self))
        return movesList
    def __str__(self):
        return super().__str__()
    def __eq__(self, other):
        return super().__eq__(other)
class Knight(ChessPiece):
    unicodeCharBlack="\u265E"
    unicodeCharWhite="\u2658"
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def possibleMove(self):
        movesList=[]
        theoryMoves=[]
        adjustList=[1,-1]
        adjustList2=[2,-2]
        for i in adjustList:
            for j in adjustList2:
                theoryMoves.append((self.x+i,self.y+j))
                theoryMoves.append((self.x+j,self.y+i))
        for move in theoryMoves:
            self.moveChecker(move[0],move[1],movesList)
        
        return movesList
    def __str__(self):
        return super().__str__()
    def __eq__(self, other):
        return super().__eq__(other)