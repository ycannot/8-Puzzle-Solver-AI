# Solves a randomized 8-puzzle using A* algorithm with plug-in heuristics

import random
import math

finishState = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]

def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    try:
        return seq.index(item)
    except:
        return -1

class Puzzle8:

    def __init__(self):
        # heuristic value
        self._hval = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
        # the action (i.e., the direction of the move) that has applied to the parent node.
        self.direction = None 
        self.nodes_expanded=0
        self.matrix = []
        self.cost = 0
        for i in range(3):
            self.matrix.append(finishState[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.matrix == other.matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.matrix[row]))
            res += '\r\n'
        return res
    
    def change_state(self, l):
        """ change the state of the current puzzle to l"""
        if len(l) != 9:
            print('length of the list should be 9')
        self.matrix = []    
        for i in range(3):
            self.matrix.append(l[i*3:i*3+3])


    def clone(self):
        """ Create a copy of the existing puzzle"""
        p = Puzzle8()
        for i in range(3):
            p.matrix[i] = self.matrix[i][:]
        return p

    def getLegalMoves(self): #yapýlabilecek hamlelerin listini verir [(0, 2, 'up'), (2, 2, 'down'), (1, 1, 'left')]
        """ Returns the set of available moves as a list of tuples, each tuple contains the row and col position 
        with which the free space (0) may be swapped """
        # get row and column of the empty piece
        row, col = self.find(0)
        free = []

        # find which pieces can move there
        if row > 0:
            free.append([row - 1, col, 'up'])
        if row < 2:
            free.append([row + 1, col, 'down'])
        if col > 0:
            free.append([row, col - 1, 'left'])
        if col < 2:
            free.append([row, col + 1, 'right' ])

        return free
       
    
    def generateMoves(self):
        """ Returns a set of puzzle objects that are successors of the current state   """
        free = self.getLegalMoves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self.clone()
            p.swap(a,b[0:2])
            p.direction = b[2] # up, down, left or right
            p._depth = self._depth + 1
            p._parent = self
            return p
        # map applies the function swap_and_clone to each tuple in free, returns a list of puzzle objects
        return map(lambda pair: swap_and_clone(zero, pair), free)

    def generateSolutionPath(self, path): #solution path yaratýr. en son p.generateSolutionPath([path]) yapýlacak.
        """ construct the solution path by recursively following the pointers to the parent  """
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent.generateSolutionPath(path)



    def shuffle(self, step_count):
        """shuffles the puzzle by executing step_count number of random moves"""
        for i in range(step_count):
            row, col = self.find(0)
            free = self.getLegalMoves()
            target = random.choice(free)
            self.swap((row, col), target[0:2])
            row, col = target[0:2]

    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        """returns the value at the specified row and column"""
        return self.matrix[row][col]

    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)
        
    def isGoal(self):
        """check if we reached  the goal state"""
        puzzle=Puzzle8()
        puzzle.matrix= [[0, 1, 2],
                       [3, 4, 5],
                       [6, 7, 8]]
        
        return puzzle == self
    
    def BFS(self):
        """Performs BFS for goal state"""
        print("this is BFS")
        copy=self.clone()
        query=[copy]
        path=[]
        self.nodes_expanded=0
        while query:
            if copy.isGoal():
                #self.generateSolutionPath(copy)
                self._depth=path[-1]._depth
                temp=[copy]  
                temp1=[]
                path=path[::-1]
                for i in path:
                    k=0
                    for j in list(i.generateMoves()):
                        k+=1
                        if j==temp[-1]:
                            temp.append(i)
                            temp1.append(i.getLegalMoves()[k-1])
                path.append(self)
                path=temp[::-1]
                temp1.append([0,0,'start'])
                path_to_goal=temp1[::-1]
                
                for i in range(len(path)):
                    print(path[i],path_to_goal[i][2])
                    print()
                self._parent=path
                self.direction=path_to_goal
                self.nodes_expanded=len(path)+len(query)
                return path 
            
            copy=query.pop(0)
            
           
            if not copy in path:
                path+=[copy]  
                query.extend(list(copy.generateMoves()))
                
        
        
        
    def DFS(self):
        """Performs DFS for goal state"""
        print("this is DFS")
        copy=self.clone()
        copy1=self.clone()
        self.direction=[[0,0,"start"]]
        query=[copy]
        path=[]
        self._depth=0
        self.nodes_expanded=0
        while query:
            
            if copy.isGoal():
                #self.generateSolutionPath(copy)
                self._parent=path
                x=0
                for i in path: 
                    print(i,self.direction[x][2])
                    x+=1
                self.nodes_expanded=len(path)+len(query)
                return path
                
                
            
            copy=query.pop(0)
            
            
            if copy not in path:
                self._depth+=1
                path+=[copy]
                x=0
                for i in copy1.generateMoves():
                    if i==copy:
                        self.direction.append(copy1.getLegalMoves()[x])
                    x+=1
                
                query=list(copy.generateMoves())
                copy1=copy.clone()
                    
            
            
        
    def Astarsearch(self, h):
        """Performs A* search for goal state.
        h(move) - heuristic function, returns an integer
        """
        print("this is A*")
        copy=self.clone()
        query=[copy]
        path=[]
        self.nodes_expanded=0
        self._depth=0
        
        while query:
            lst=[]
            for i in query:
                lst.append(i.cost)
                self=copy.clone()
            if copy.isGoal() and copy.cost<=min(lst):
                #self.generateSolutionPath(copy)
                self._depth=path[-1]._depth
                temp=[copy]  
                temp1=[]
                path=path[::-1]
                for i in path:
                    k=0
                    for j in list(i.generateMoves()):
                        k+=1
                        if j==temp[-1]:
                            temp.append(i)
                            temp1.append(i.getLegalMoves()[k-1])
                path.append(self)
                path=temp[::-1]
                temp1.append([0,0,'start'])
                path_to_goal=temp1[::-1]
                
                for i in range(len(path)):
                    print(path[i],path_to_goal[i][2])
                    print()
                self._parent=path
                self.direction=path_to_goal
                self.nodes_expanded=len(path)+len(query)
                #self._depth=len(self.direction)
                return path 
            
            copy=query.pop(lst.index(min(lst)))
            oldVal=lst.pop(lst.index(min(lst)))
            for i in list(copy.generateMoves()):
                i.cost+=oldVal+1
                query.append(i)
                lst.append(oldVal+1)
            for i in path:
                for j in query:
                    if (j.matrix == i.matrix) and (j.cost<i.cost):
                        i=j
                
           
            if not copy in path:
                path+=[copy]  
                

def main():
    p = Puzzle8() # when we create the puzzle object, it's already in the goal state
    p.shuffle(20) # that's why we shuffle to start from a random state which is 20 steps away from from the goal state
    print(p)
    p.change_state([1,2,5,3,4,0,6,7,8])
    print(p)
    print("----------------------------------")
    with open("output.txt","w") as f:
        p.BFS()
        f.write("this is BFS\n\n")
        for i in range(len(p._parent)):
            f.write(str(p._parent[i])+str(p.direction[i][2])+"\n\n")
        l=[]
        for i in p.direction:
            l.append(i[2])        
        f.write("depth: "+str(p._depth)+"\n"+"cost: "+str(p._depth)+"\npath to goal: "+str(l)+"\n"+"nodes_expanded: "+str(p.nodes_expanded)+"\n\n")
        p.Astarsearch(2)
        f.write("this is A* search\n\n")
        for i in range(len(p._parent)):
            f.write(str(p._parent[i])+str(p.direction[i][2])+"\n\n")
        l=[]
        for i in p.direction:
            l.append(i[2])
        f.write("depth: "+str(p._depth)+"\n"+"cost: "+str(p.cost)+"\npath to goal: "+str(l)+"\n"+"nodes_expanded: "+str(p.nodes_expanded)+"\n\n")  
        p.change_state([1,2,0,3,4,5,6,7,8])
        p.DFS()
        f.write("this is DFS\n\n")
        for i in range(len(p._parent)):
            f.write(str(p._parent[i])+str(p.direction[i][2])+"\n\n")
        l=[]
        for i in p.direction:
            l.append(i[2])        
        f.write("depth: "+str(p._depth)+"\n"+"cost: "+str(p._depth)+"\npath to goal: "+str(l)+"\n"+"nodes_expanded: "+str(p.nodes_expanded)+"\n\n")
        
        
        
        
    f.close()
    p.BFS()
    #p.DFS()
    p.Astarsearch(0)
    print(p._parent)
    print(p.direction)
    
    print(p._depth)
    
if __name__ == "__main__":
    main()
