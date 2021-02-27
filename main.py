from sys import stdin,stdout
import math

#   READERS -----------------------------------------------
def readln() -> str: return stdin.readline().rstrip()
def readBoardParams():
    line= readln().split(' ')
    board_size=int(line[0]) #N
    max_slide=int(line[1]) #M , represents the maximum number of slides allowed
    return board_size,max_slide

def readBoard(size):
    board=[]
    flatten_board=[]
    count=0
    #occ=[0]*11 #(log2(2048))
    for k in range(size):
        ln=readln().split(' ')
        board_line=[]
        for n in ln:
            x=int(n)
            board_line.append(x)
            if(x!=0):
                flatten_board.append(x)
                count+=1
                #occ[int(math.log2(x))]+=1
        board.append(board_line) #append has better performance than concat (+), append uses the same list while concat creates a new instance of a list
    return board,flatten_board,count #,occ

#   PRINTERS ----------------------------------------------
def outln(n: int) -> None: 
    stdout.write(str(n))
    stdout.write('\n')

def printBoard(board: list, size: int) -> None:
    for i in range(size):
        for j in range(size): 
            stdout.write(str(board[i][j])+' ')
        stdout.write('\n')

#   SLIDERS -----------------------------------------------
def slideRight(board: list, size: int):
    #a new matrix is created so that 'board' remains imaculated
    board_after= [None]*size 
    after_elem_count, before_elem_count = 0, 0
    for row in range(size):
        aux = []
        non_zeros=0
        for column in range(size):
            elem=board[row][column]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count,board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count
        
    return before_elem_count,after_elem_count,board_after  

def slideLeft(board:list, size:int):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = []
        non_zeros=0
        for column in range(size-1,-1,-1):
            elem=board[row][column]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count

    return before_elem_count,after_elem_count,board_after

def slideDown(board,size):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = []
        non_zeros=0
        for column in range(size):
            elem=board[column][row]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count

    #transpose matrix
    #board_after=[[board_after[column][row] for column in range(size)] for row in range(size)] 
    return before_elem_count,after_elem_count,board_after
    
def slideUp(board,size):
    board_after= [None]*size 
    before_elem_count, after_elem_count = 0, 0
    for row in range(size):
        aux = []
        non_zeros=0
        for column in range(size-1,-1,-1):
            elem=board[column][row]
            if elem!=0:
                aux.append(elem)
                non_zeros+=1
        after_count, board_after[row] = slide(aux, size, non_zeros)
        before_elem_count+=non_zeros
        after_elem_count+=after_count

    #transpose matrix
    #board_after = [[board_after[column][row] for column in range(size)] for row in range(size)] 
    return before_elem_count,after_elem_count,board_after
 
def slide(orig_row:list, size:int, non_zeros:int):
    # orig_row:   ''compressed'' line e.g: [1,3] instead of [1,0,3,0] 
    # size:  size of original board
    # non_zeros: equal to len(orig_row)
    final= [0]*size
    orig_col, final_col= non_zeros-2, 0
    while orig_col>=0:
        if orig_row[orig_col]==orig_row[orig_col+1]:
            #merge
            final[final_col]= orig_row[orig_col]*2
            orig_col-=2
            non_zeros-=1
        else:
            final[final_col]= orig_row[orig_col+1]
            if orig_col==0:
                final_col+=1
                final[final_col]= orig_row[orig_col]
                final_col+=1
                break
            orig_col-=1
        final_col+=1
    #para o caso em que só temos um elemento na lista diferente de 0 OU p.exemplo: [4,4,4]
    if orig_col==-1: final[final_col]= orig_row[0]

    return non_zeros,final 

def addBoardsToHashTable(hash_table,slide_count,str_board): #(hash_table,slide_count,board,str_board,board_size)
    #add board as it is
    hash_table[str_board]=slide_count
    """
    #add equivelent boards:
    #transpose matrix
    transpose_board=[[board[column][row] for column in range(board_size)] for row in range(board_size)] 
    hash_table[str(transpose_board)]=slide_count
    #print(transpose_board)
    #inverse matrix
    inverse_board=[board[row][::-1] for row in range(board_size)] 
    #print(inverse_board)
    hash_table[str(inverse_board)]=slide_count
    #transpose inverse matrix
    transpose_inverse_board=[transpose_board[row][::-1] for row in range(board_size)] 
    #print(transpose_inverse_board)
    hash_table[str(transpose_inverse_board)]=slide_count
     """

"""
def isOdd(n):
    return n%2==1
"""

#   RECURSIVITY -------------------------------------------
def recursiveTries(board,board_size,slide_count,hash_table,min_estimate):
    global max_slide
    if(slide_count<=max_slide):
        before_elem_count_l,after_elem_count_l,after_board_l=slideLeft(board,board_size)
        before_elem_count_r,after_elem_count_r,after_board_r=slideRight(board,board_size)
        before_elem_count_u,after_elem_count_u,after_board_u=slideUp(board,board_size)
        before_elem_count_d,after_elem_count_d,after_board_d=slideDown(board,board_size)
        if after_elem_count_r==1 or after_elem_count_l==1 or after_elem_count_u==1 or after_elem_count_d==1:
            #para o caso da matrix inicial ter apenas 1 elemento no inicio 
            if before_elem_count_r==1 or before_elem_count_l==1 or before_elem_count_u==1 or before_elem_count_d==1: return slide_count-1
            else: 
                if(slide_count==min_estimate):
                    max_slide=0 #force end of all recursion if min_estimate possible has been reached
                return slide_count
        else:
            str_board=str(after_board_l)
            if str_board in hash_table and slide_count>=hash_table[str_board]: 
                l=-1
            else:
                hash_table[str_board]=slide_count
                l= recursiveTries(after_board_l,board_size,slide_count+1,hash_table,min_estimate)

            str_board=str(after_board_r)
            if str_board in hash_table and slide_count>=hash_table[str_board]: r=-1
            else:
                hash_table[str_board]=slide_count
                r=recursiveTries(after_board_r,board_size,slide_count+1,hash_table,min_estimate)
            
            str_board=str(after_board_u)
            if str_board in hash_table and slide_count>=hash_table[str_board]: u=-1
            else:
                hash_table[str_board]=slide_count
                u = recursiveTries(after_board_u,board_size,slide_count+1,hash_table,min_estimate)

            str_board=str(after_board_d)
            if str_board in hash_table and slide_count>=hash_table[str_board]: d=-1
            else:
                hash_table[str_board]=slide_count
                d = recursiveTries(after_board_d,board_size,slide_count+1,hash_table,min_estimate)
            
            #print(" r:{}\n l:{}\n u:{}\n d:{}\n".format(r,l,u,d))
            if(r>=0 or l>=0 or u>=0 or d>=0): return  min(i for i in [r,l,u,d] if i>=0)
            else: return -1
    else: return -1

def getMinSlide(board,board_size,min_estimate):
    #get value of minimum slides needed to finish the game.
    #if number of slides needed is greater than max_slide, return 'no solution'
    hash_table=dict() #reset
    answer = recursiveTries(board,board_size,1,hash_table,min_estimate)
    if answer == -1: return 'no solution'
    else: return str(answer)

"""
def isCandidate(occ):
    count=0
    for i in range(11):
        count+=occ[i]*2**i
    return isBase2(int(count))

def isBase2(n):
    return (n & (n-1) == 0) and n != 0
"""

def func(flatten_board,elem_count):
    #flatten_board has no zeros
    slide_count=0
    while(slide_count<=max_slide):
        if(elem_count<=1):
            return slide_count
        flatten_board.sort()
        i=0
        aux=[]
        limite=elem_count-2
        while(i<=limite):
            x=flatten_board[i]
            if(x==flatten_board[i+1]):
                aux.append(x*2)
                i+=2
                elem_count-=1
            else:
                aux.append(x)
                if i==limite:
                    aux.append(flatten_board[i+1])
                    break
                i+=1
        if(i==limite+1):
            aux.append(flatten_board[i])
        flatten_board=aux
        slide_count+=1
    return -1

def main() -> None:
    global max_slide
    num_testcases= int(readln())
    #read test case parameters from stdin
    for k in range(num_testcases):
        board_size, max_slide= readBoardParams()
        #read board content from stdin
        board,flatten_board,elem_count=readBoard(board_size)

        """
        #check if board isn't impossible
        if(isCandidate(occ)):
            outln(getMinSlide(board,board_size))
        else:
            outln('no solution')
        """
        min_slide_estimate=func(flatten_board,elem_count)
        if(min_slide_estimate!=-1):
            #print('ok {}'.format(min_slide_estimate))
            outln(getMinSlide(board,board_size,min_slide_estimate))
        else:
            outln('no solution')


max_slide=0 #global

if __name__=='__main__': main()

#pypy3 main.py -m py_compile < test.txt
