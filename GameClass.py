class ChessPiece():
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
    def __str__(self):
        return self.color+" "+self.__class__.__name__
class Rook(ChessPiece):
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class King(ChessPiece):
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class Queen(ChessPiece):
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class Bishop(ChessPiece):
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class Pawn(ChessPiece):
    def __init__(self, chessBoard, positionY, positionX, color) -> None:
        super().__init__(chessBoard, positionY, positionX, color)
    def move(self, positionX, positionY):
        return super().move(positionX, positionY)
    def __str__(self):
        return super().__str__()
class Knight(ChessPiece):
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
        self.board=[[0 for _ in range(8)] for _ in range(8)]
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
        
    def terminal_test():
        pass
    def showBoard(self):
        for rows in self.board:
            print([str(i) for i in rows])

chess=ChessBoard()
chess.showBoard()
print(chess.board[0][0].y)