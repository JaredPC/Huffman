
#A AnyList is either
#None
#or a node containing a value and a remaining list. 
class Pair:
    def __init__(self, first, rest):
        self.first = first          #Value 
        self.rest = rest            #Anylist representing the rest of the list

    def __eq__(self, other):
        return ((type(other) == Pair)
          and self.first == other.first
          and self.rest == other.rest
        )

    def __repr__(self):
        return ("Pair({!r}, {!r})".format(self.first, self.rest))
    
#None -> AnyList
#takes in no arguments and returns an empty list
def empty_list():
    return None

#AnyList, Int, AnyType -> AnyList
#takes in a list, an integer index, and another value (of any type) as arguments and places the value at index position in the list
#Raises IndexError exception if index is not defined in the list
def add(alist,index,val):
    if(index<0):
        raise IndexError
    elif(index == 0):
        return Pair(val,alist)
    else:
        if(alist==None):
            raise IndexError
        return Pair(alist.first, add(alist.rest, index-1, val))

#AnyList -> Int
#takes in a list as an argument and returns the number of elements currently in the list
def length(alist):
    if(alist == None):
        return 0
    else:
        return 1 + length(alist.rest)
    
#Anylist, Int -> Int
#takes in a list and an integer index and returns the value at the index position in the list
#Raises IndexError exception if index is not defined in the list
def get(alist,index):
    if(index < 0 or alist == None):
        raise IndexError
    elif(index==0):
        return alist.first
    else:
        return get(alist.rest,index-1)
    
#AnyList, Int, AnyType -> AnyList
#takes a list, an integer index, and another value and replaces the element at index position in the list with the given value
#Raises IndexError exception if index is not defined in the list
def set(alist,index,val):
    if(index<0 or alist==None):
        raise IndexError
    elif(index==0):
        return(Pair(val,alist.rest))
    else:
        return Pair(alist.first, set(alist.rest,index-1,val))

#AnyList, Int -> AnyList, AnyType
#takes a list and an integer index as arguments and removes the element at the index position from the list and returns the new Anylist and the removed AnyType
#Raises IndexError exception if index is not defined in the list
def remove(alist, index):
    if(index < 0 or alist == None):
        raise IndexError
    elif(index == 0):
        if(alist.rest == None):
            return (alist.first,None)
        return (alist.first,Pair(alist.rest.first,alist.rest.rest))
    else:
        remove_call=remove(alist.rest, index-1)
        return (remove_call[0],Pair(alist.first, remove_call[1]))
    
#AnyList, anyFunction -> None
#takes in an Array and a function as arguments and applies the provided function to the value at each position in the Array
def foreach(alist,func):
    if(alist==None):
        pass
    else:
        func(alist.first)
        if(alist.rest!=None):
            foreach(alist.rest,func)

#AnyList -> AnyList
#takes in a List and a "less-than" function as arguments and sorts the list such that the elements are in ascending order as determined by the "less-than" function
def sort(alist, comp):
    if(alist==None):
        return None
    rlist=Pair(alist.first,None)
    alist=alist.rest
    while (alist != None):
        val=alist.first
        alist=alist.rest
        if(comp(val,rlist.first) == True):
            rlist=Pair(val,rlist)
        else:
            search=rlist
            while(search.rest != None and comp(val,search.rest.first)==False):
                search=search.rest
                remove(rlist,length(rlist)-1)
            search.rest=Pair(val,search.rest)
            add(rlist,length(rlist)-1,search)
    return rlist

#LinkedList, AnyType, Function -> LinkedList
#takes in a sorted linked list, a value, and your implemented comes_before() and returns a sorted list with the val
def insert_sorted(llist,val,comp):
    if(llist==None):
        return Pair(val,None)
    elif(comp(val,llist.first)):
        return Pair(val,llist)
    else:
        return Pair(llist.first,insert_sorted(llist.rest, val, comp))

#Compare function
def compareinc(a,b):
    if(a<b):
        return True
    elif(a>b):
        return False
    else:
        return True
    