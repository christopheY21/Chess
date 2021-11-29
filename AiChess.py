import math
import copy
class AiChess():
    #IA
    def __init__(self):
        self.game=""
    def initializeGame(self,chessGame):
        self.game=chessGame
    def successors(self):
        """
        Returns a list of the successors resulting from all the possibles actions from the current state of the game
        """
        if(self.game.state==-1):
            colorPlay="Black"
        else:
            colorPlay="White"
        gameActions=self.game.boardPossibleMoves()
        gameSuccessors=[(i,copy.deepcopy(self.game)) for i in gameActions]
        for actions,successor in gameSuccessors:
            successor.movePieces(actions,gameActions)
        return gameSuccessors
    def eval(self,colorPlay):
        evaluation=0
        piecesDictValue={
            "King":666,
            "Queen":9,
            "Rook":5,
            "Bishop":3,
            "Knight":3,
            "Pawn":1
        }
        if(colorPlay=="Black"):
            for piece in self.game.blackPiecesList:
                evaluation+=piecesDictValue[piece.__class__.__name__]
        else:
            for piece in self.game.whitePiecesList:
                evaluation+=piecesDictValue[piece.__class__.__name__]
        return evaluation
    def utility(self):
        if(self.game.result=="1-0"):
            gameIssue=1
        elif(self.game.result=="0-1"):
            gameIssue=-1
        else:
            gameIssue=1/2
        return gameIssue

    #ALPHABETA
    def alpha_beta_decision(self,maxPlayer):
        maximum=-math.inf
        for a,s in self.successors():
            smin=s.ai.min_valueAB(-math.inf,math.inf,1,(maxPlayer))
            if(maximum<smin):
                action=a
                maximum=smin
        return action
    def max_valueAB(self,alpha,beta,depth,player):
        if(self.cutoff_test(depth)):
            return self.eval(player)
        v=-math.inf
        for a,s in self.successors():
            v=max(v,s.ai.min_valueAB(alpha,beta,depth-1,player))
            #print("max pivot :{}".format(v))
            if v>=beta:
                return v
            alpha=max(alpha,v)
        return v
    def min_valueAB(self,alpha,beta,depth,player):
        #if(self.terminal_test()):
         #   return self.utility()
        if(self.cutoff_test(depth)):
            return self.eval(player)
        v=math.inf
        for a,s in self.successors():
            v=min(v,s.ai.max_valueAB(alpha,beta,depth-1,player))
            if v<=alpha:
                return v
            beta=min(beta,v)
        return v

    def cutoff_test(self,depth):
        depthCut=0
        if(depthCut==depth or self.game.terminal_test()):
            return True
        else:
            return False