#import random
#import logging
#import typing; from typing import *
#import itertools
#from itertools import product
#from sample_players import null_score, open_move_score, improved_score

class SearchTimeout(Exception):
    """Subclass base exception for code clarity."""
    pass

SCORE=0
MOVE=1
NO_MOVES=(-1,-1)
POS_INF=float('inf')
NEG_INF=float('-inf')


def custom_score(game, player) -> float:
# This dynamic heuristic attempts to use domain-specific info of open squares
# to measure which phase in the game we are at.
# Emprical results show an average of around 14 open squares at game end, 
# compared to 49 at game start. This can be simplied to 
# 14/49=3.5 at end game, 1.0 at start    
# For this version we use this ratio to 
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    
    #count_total_positions = float(game.height * game.width)
    #count_empty_coords = float(len(game.get_blank_spaces()))
    #w=count_empty_coords/count_total_positions
    #k=count_total_positions/count_empty_coords
    k=game.move_count
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return  float(- opp_moves) if k<20 else float(own_moves)

def custom_score_2(game, player) -> float:

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    k=game.move_count/30.
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(k*own_moves - opp_moves) 
    
    #return ((1-w)*own_moves - w*opp_moves)**2

def custom_score_3(game, player) -> float:

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    k=game.move_count/30.
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - k*opp_moves) 
#    return k**2*own_moves - opp_moves




class IsolationPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

class MinimaxPlayer(IsolationPlayer):

    def __init__(self,search_depth=3,score_fn=custom_score,timeout=25):
        super().__init__(search_depth=search_depth, score_fn=score_fn, timeout=timeout)

    def get_move(self, game, time_left):
        
        legal_moves=game.get_legal_moves()
        if not legal_moves:
            return NO_MOVES
        
        best_move = legal_moves[0]
        #alternative approach: use greedy scoring to find default best move
        #not supported by the pa unittests
    #    greedy=[(self.score(game.forecast_move(m),self),m) for m in legal_moves]
    #    best_move=max(greedy)[MOVE]
        self.time_left=time_left
    #    try: 
        best_move = self.minimax(game, depth=self.search_depth)
     #       return best_move
 #       except SearchTimeout:
  #          pass
        return best_move

    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
#        if not legal_moves:
#            return(-1,-1)
        best_move=legal_moves[0]
        
        actions=[]
        for m in legal_moves:
            try:
                a=(self.min_value(game.forecast_move(m),self.search_depth-1,self.time_left),m)
                actions.append(a)
            except SearchTimeout:
                break
        best_move= max(actions)[MOVE]
        return best_move 
    
    
    def min_value(self,g,d,time_left):
        if time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        best_score=POS_INF        
        if d<1:
            return self.score(g,self)
        
        legal_moves = g.get_legal_moves()
        if not legal_moves:
            return g.utility(self)
                
        try:
            actions=[(self.max_value(g.forecast_move(m),d-1,time_left),m) for m in legal_moves]
            best_score=min(actions,key=lambda a:a[SCORE])[SCORE]
        except SearchTimeout:
            pass
        return best_score

    def max_value(self,g,d,time_left):
        if time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout
        best_score=NEG_INF        
        if d<1:
            return self.score(g,self)
        legal_moves = g.get_legal_moves()
        if not legal_moves:
            return g.utility(self)
                
        try:
            actions=[(self.min_value(g.forecast_move(m),d-1,time_left),m) for m in legal_moves]
            best_score=max(actions,key=lambda a:a[SCORE])[SCORE]
        except SearchTimeout:
            pass
        return best_score

  
class AlphaBetaPlayer(IsolationPlayer):

    def __init__(self,search_depth=3,score_fn=custom_score,timeout=40):
        super().__init__(search_depth=search_depth, score_fn=score_fn, timeout=timeout)

    def get_move(self, game, time_left):
        best_move=NO_MOVES
        self.time_left=time_left
        for i in range(1,100): 
            try:
                best_move= self.alphabeta(game, depth=i)
            except SearchTimeout:
                break
        return best_move

    def alphabeta(self, game,depth,alpha=float("-inf"),beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return NO_MOVES
        best_score,best_move=NEG_INF,legal_moves[0]
        
        for m in legal_moves:
            try:
                action=(self.minimizer(game.forecast_move(m),self.search_depth-1,alpha,beta,self.time_left),m)
                if action[SCORE] > best_score:
                    best_score,best_move=action
                if best_score>=beta:
                    break
                alpha=max(best_score,alpha)
            except SearchTimeout:
                pass
        return best_move
    
    def minimizer(self,g,d,a,b,t):
        if t() < self.TIMER_THRESHOLD:
            raise SearchTimeout
        if d<1:
            return self.score(g,self)
        legal_moves = g.get_legal_moves()
        if not legal_moves:
            return g.utility(self)        
        best_score=POS_INF
        for m in legal_moves:
            action=(self.maximizer(g.forecast_move(m),d-1,a,b,t),m)
            best_score=min(action[SCORE],best_score)
            if best_score<=a:
                break         
            b=min(best_score,b)
        return best_score
                    
    
    def maximizer(self,g,d,a,b,t):
        if t() < self.TIMER_THRESHOLD:raise SearchTimeout
        if d<1:return self.score(g,self)
        legal_moves = g.get_legal_moves()
        if not legal_moves:return g.utility(self)        
        best_move,best_score=legal_moves[0],float("-inf")
        for m in legal_moves:
            action=(self.minimizer(g.forecast_move(m),d-1,a,b,t),m)
            if action[SCORE] > best_score:
                best_score,best_move=action
            if best_score >= b:
                break
            a=max(best_score,a)
        return best_score


 