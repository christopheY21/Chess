import ChessPieces
import time
import datetime
class ChessBoard(): 
    def __init__(self,loadpgnFile="noLoad",boardConfig=False,unicodeText=True):
        self.state=1# -1 Black : 1 White -> state white have to play
        self.turn=1
        self.board=[[ChessPieces.Cases(j,i) for i in range(8)] for j in range(8)]
        self.blackPiecesList=[]
        self.whitePiecesList=[]
        self.history=[]
        self.result=0
        self.unicodeText=unicodeText
        if(not boardConfig):
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

            #complete black list pieces
            for i in range(8):
                for j in range(2):
                    self.blackPiecesList.append(self.board[j][i])
            #complete white list pieces
            for i in range(8):
                for j in range(6,8):
                    self.whitePiecesList.append(self.board[j][i])
        else:
            self.boardConfiguration()
        if(loadpgnFile[-4:]==".pgn"):
            self.loadPgnGame(loadpgnFile)
        #self.showBoard()

    def loadPgnGame(self,loadpgnFile):
        try:
            with open(loadpgnFile,"r") as game:
                l=game.read().split("1.")
                movesHistory=("1."+l[1]).strip()
                movesList=movesHistory.split(" ")
                
                for i in range(0,len(movesList),2):
                    movesList[i]=movesList[i].split(".")[1]
                #print(movesList)
                #TRADUCTION PGN TO CLASS FORMAT

                for move in movesList:
                    print(move)
                    if(self.state==-1):#Black play
                        colorPlay="Black"
                    else:
                        colorPlay="White"
                    boardMoves=self.boardPossibleMoves(colorPlay)
                    self.movePieces(self.pgnToMove(move,boardMoves),boardMoves)
                
                
        except IOError as e:
            print(e)
    def pgnToMove(self,move,boardMoves):

        algebricNotation={
            "B":ChessPieces.Bishop,
            "R":ChessPieces.Rook,
            "Q":ChessPieces.Queen,
            "K":ChessPieces.King,
            "N":ChessPieces.Knight,
            "O-O":"SmallCastle",
            "O-O-O":"BigCastle"
        }
        
        pieceType=algebricNotation.get(move[0],ChessPieces.Pawn)
        if(len(move)<=3):
            #Normal moves
            indexX=1
            indexY=2
            if(pieceType==ChessPieces.Pawn):
                indexX-=1
                indexY-=1
            moveX=int(ord(move[indexX]))-97
            moveY=(int(move[indexY])-8)*(-1)
        elif(len(move)==4):#Mange
            moveX=int(ord(move[2]))-97
            moveY=(int(move[3])-8)*(-1)
        for moveBoard in boardMoves:
            if(moveBoard[0]==moveX and moveBoard[1]==moveY and type(moveBoard[2])==pieceType):
                return moveBoard
        self.showBoard()
        return None
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
            possibleMovesList.extend(movesList)
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
        promotedPawn=(False,None)
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
            if(movedPiece.passantCase[0] and (movedPiece.passantCase[1]+1)==self.turn):
                eatingMove=True
                if(self.state==-1):
                    passedPiece=self.board[moves[1]-1][moves[0]]
                    self.whitePiecesList.remove(passedPiece)
                else:
                    passedPiece=self.board[moves[1]+1][moves[0]]
                    self.blackPiecesList.remove(passedPiece)
                self.board[passedPiece.y][passedPiece.x]=ChessPieces.Cases(passedPiece.y,passedPiece.x)
        #Rendre vide la case de depart
        self.board[moves[2].y][moves[2].x]=ChessPieces.Cases(moves[2].y,moves[2].x)
        #Promotion move
        listOfPromotion=[ChessPieces.Queen,ChessPieces.Bishop,ChessPieces.Rook,ChessPieces.Knight]
        promotionResponse=0
        if(moves[1]==0 and moves[2].color=="White" and type(moves[2])==ChessPieces.Pawn):
            print("PROMOTION!")
            self.whitePiecesList.remove(moves[2])
            print("Choose a promotion :{}".format([str(i.__name__) for i in listOfPromotion]))
            promotionResponse=int(input("Choose a number:"))
            newPiece=listOfPromotion[promotionResponse](self,moves[1],moves[0],"White")
            self.whitePiecesList.append(newPiece)
            self.board[moves[1]][moves[0]]=newPiece
            print("Vous avez choisi {}.".format(str(newPiece)))
            promotedPawn=(True,listOfPromotion[promotionResponse])
        elif(moves[1]==7 and moves[2].color=="Black" and type(moves[2])==ChessPieces.Pawn):
            self.blackPiecesList.remove(moves[2])
            print("Choose a promotion :{}".format([str(i.__name__) for i in listOfPromotion]))
            promotionResponse=int(input("Choose a number:"))
            newPiece=listOfPromotion[promotionResponse](self,moves[1],moves[0],"Black")
            self.whitePiecesList.append(newPiece)
            self.board[moves[1]][moves[0]]=newPiece
            promotedPawn=(True,listOfPromotion[promotionResponse])
            print("Vous avez choisi {}.".format(str(newPiece)))
        #Rook
        elif(type(moves[2])==ChessPieces.King and abs(moves[0]-moves[2].x)==2):
            moves[2].move(moves[0],moves[1])
            self.board[moves[1]][moves[0]]=moves[2]
            rookY=0
            if(moves[2].color=="Black"):
                rookY=0
            else:
                rookY=7
            if(moves[1]>4):#small castle

                self.board[rookY][5]=self.board[rookY][7]
                self.board[rookY][5].x=5
                self.board[rookY][5].y=rookY
                self.board[rookY][7]=ChessPieces.Cases(7,rookY)
            else:#big castle
                self.board[rookY][3]=self.board[rookY][0]
                self.board[rookY][3].x=3
                self.board[rookY][3].y=rookY
                self.board[rookY][0]=ChessPieces.Cases(0,rookY)
        #acting move
        else:
            moves[2].move(moves[0],moves[1])
            self.board[moves[1]][moves[0]]=moves[2]
            if(type(moves[2])==ChessPieces.Pawn):
                if(moves[2].passant[0]):
                    self.board[moves[2].y+(self.state)][moves[2].x].passantCase=[True,self.turn]
        #Checking moves
        self.state=self.state*(-1)
        self.turn+=1
        if(self.echec()!=[]):
            checkingMove=True

        self.history.append((startingMove,endingMove,checkingMove,eatingMove,promotedPawn))
        
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
            self.result=self.state*(-1)
            print(self.echec()[0].color)
            return True
        return False
    def boardConfiguration(self):
        algebricNotation={
            "B":ChessPieces.Bishop,
            "R":ChessPieces.Rook,
            "Q":ChessPieces.Queen,
            "K":ChessPieces.King,
            "N":ChessPieces.Knight,
            "P":ChessPieces.Pawn
        }
        print("Vous avez choisi la configuration manuelle!")
        
        #APPEND PIECE  ON BOARD
        reponse='c'
        self.showBoard()
        while(reponse!="q"):
            print("Entrez (x,y,P,color) P version algébrique pour ajouter une piece: ")
            pieceX=int(input("Entrez x:"))
            pieceY=int(input("Entrez y:"))
            pieceType=input("Entrez le type B/R/Q/J/B/P:")
            pieceColor=input("Entrez la couleur Black/White:")
            pieceType=algebricNotation[pieceType]
            self.board[pieceY][pieceX]=pieceType(self,pieceY,pieceX,pieceColor)
            if(pieceColor=="Black"):
                self.blackPiecesList.append(self.board[pieceY][pieceX])
            else:
                self.whitePiecesList.append(self.board[pieceY][pieceX])
            self.showBoard()
            reponse=input("Entre 'q' pour quittez / c pour continuez:")
    def printMovesList(self,movesList):
        i=0
        for move in movesList:
            print((move[0],move[1],str(move[2])), end=" ")
            print(i)
            i+=1
    def startTheGame(self):
        whiteTime=0
        blackTime=0
        while(not self.terminal_test()):
            
            if(self.state==-1):
                blackStart=time.time()

                colorPlay="Black"
                print("Le temps de jeu des noirs est :{}".format(datetime.timedelta(seconds=blackTime)))
                print("C'est au tour des Noirs de jouer!")
            else:
            
                whiteStart=time.time()
                
                colorPlay="White"
                print("Le temps de jeu des blancs est :{}".format(datetime.timedelta(seconds=whiteTime)))
                print("C'est au tour des blanc de jouer!")
            self.showBoard()
            movesList=self.boardPossibleMoves(colorPlay)
            self.printMovesList(movesList)
            print("You can resign if you input 'resign' you can propose a draw with 'draw':")
            chooseMove=input("Which move do you chose ?:")
            #chooseMove=0
            if(chooseMove=="resign"):
                if(self.state==-1):
                    print("Black resign")
                else:
                    print("White resign")
                self.result=self.state*(-1)
                break
            elif(chooseMove=="draw"):
                if(self.state==-1):
                    print("Black want to draw do you want too?")
                else:
                    print("White want to draw do you want too?")
                draw=input("you can reply with  y/n:")
                if(draw=="y"):
                    print("it's a draw !")
                    self.result=1/2
                    break
                else:
                    print("Keep playing the draw is refused")
                    continue
            if(self.state==1):##White have to play
                self.movePieces(movesList[int(chooseMove)],movesList)
                whiteTime+=time.time()-whiteStart
            elif(self.state==-1):##Black have to play
                self.movePieces(movesList[int(chooseMove)],movesList)
                blackTime+=time.time()-blackStart
            
            #self.writeHistory()
    def showBoard(self):
        unicodeToText={
            ChessPieces.Bishop.__name__:"B",
            ChessPieces.Rook.__name__:"R",
            ChessPieces.Queen.__name__:"Q",
            ChessPieces.King.__name__:"K",
            ChessPieces.Knight.__name__:"N",
            ChessPieces.Pawn.__name__:"P"
        }
        
        
        if(self.unicodeText):
            print([str(i) for i in range(8)])
            i=0
            for rows in self.board:
                print([str(i) for i in rows],end=" ")
                print(i)
                i+=1
        else:
            print([(str(i)+' ') for i in range(8)])
            i=0
            for rows in self.board:
                pieceList=[]
                textRep=""
                for piece in rows:
                    if(type(piece)==ChessPieces.Cases):
                        textRep="__"
                    elif(piece.color=="Black"):
                        textRep="b"+unicodeToText[piece.__class__.__name__]
                    else:
                        textRep="w"+unicodeToText[piece.__class__.__name__]
                    pieceList.append(textRep)
                print(pieceList,end=" ")
                print(i)
                i+=1


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
                    historyFile.write("{}.".format(turn))
                    turn+=1
                if(move[3]):#EATING MOVE
                    if(type(move[1][2])==ChessPieces.Pawn):
                        historyFile.write("{}x ".format(chr(move[0][0]+97)))
                    else:
                        historyFile.write("{}x".format(algebricNotation[move[1][2].__class__.__name__]))
                    historyFile.write("{}{}".format(chr(move[1][0]+97),move[1][1]*(-1)+8))
                else:
                    historyFile.write("{}".format(algebricNotation[move[1][2].__class__.__name__]))
                    historyFile.write("{}{}".format(chr(move[1][0]+97),move[1][1]*(-1)+8))
                if(move[4][0]):#PROMOTING PAWN
                    historyFile.write("={}".format(algebricNotation[move[4].__name__]))
                if(move[2]):#Checking move
                    historyFile.write("+")

                historyFile.write(" ")
                moveNumber+=1


                
                
        print(self.history)
