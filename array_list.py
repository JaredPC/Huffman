
#An Array is a 
#List Containing any types,
#the size of the array,
#and the allocated space of the array
class List:
    def __init__(self, list, size, space):
        self.list = list        #python List
        self.size = size        #number of elements in the List
        self.space = space      #number of slots of memory allocated for the list

    def __eq__(self, other):
        return ((type(other) == List)
          and self.list == other.list
          and self.size == other.size
          and self.space == other.space
        )

    def __repr__(self):
        return ("List({!r}, {!r}, {!r})".format(self.list, self.size, self.space))

#None -> Array
#takes in no arguments and returns an empty Array
def empty_list():
    return List([None]*1,0,1)

#Array, Int, AnyType -> Array
#takes in an array, an integer index, and another value (of any type) as arguments and places the value at index position in the array
#Raises IndexError exception if index is not defined in the Array
#def add(alist, index, val):
#    if(index<0 or index>alist.size):
#        raise IndexError
#    else:
#        if(alist==List([None]*1,0,1)):
#            alist.space=alist.space+1
#            alist.list=[val]+[None]
#            alist.size=alist.size+1
#        else:
#            count=0
#            rlist=[]
#            for i in alist.list:
#                if(count==index):a
#                    rlist=rlist+[val]
#                if(i==None):
#                    pass
#                else:
#                    rlist=rlist+[i]
#                count=count+1
#            if(index==alist.size):
#                rlist=rlist+[val]
#            alist.size=alist.size+1
#            if(alist.size>alist.space):
#                alist.space=(alist.size)*2
#                rlist=rlist+[None]*(alist.size)
#            else:
#               rlist=rlist+[None]*(alist.space-alist.size)
#            alist.list=rlist
#        return alist

#def add(alist, index, val):
#    if(index<0 or index>alist.size):
#        raise IndexError
#    else:
#        if(alist==List([None]*1,0,1)):
#            alist.space=alist.space+1
#            alist.list=[val]+[None]
#            alist.size=alist.size+1
#        else:
#            if(alist.size+1>alist.space):
#                alist.space=(alist.size+1)*2
#                alist.list=alist.list+[None]*(alist.size+2)
#            hold=alist.list[index]
#            alist.list[index]=val
#            for i in range(index+1,alist.size+1):
#                next=alist.list[i]
#                alist.list[i]=hold
#                hold=next
#            alist.size=alist.size+1
#        return alist

def add(alist,index,val):
    if(index<0 or index>alist.size):
        raise IndexError
    else:
        if(alist==List([None]*1,0,1)):
            alist.space=alist.space+1
            alist.list=[val]+[None]
            alist.size=alist.size+1
        else:
            if(alist.size==alist.space):
                alist.space=(alist.size+1)*2
                rlist=[None]*alist.space
                for i in range(alist.size):
                    rlist[i]=alist.list[i]
                alist.list=rlist
            hold=alist.list[index]
            alist.list[index]=val
            for i in range(index+1,alist.size+1):
                next=alist.list[i]
                alist.list[i]=hold
                hold=next
            alist.size=alist.size+1
        return alist
    
def add_plus1(alist, index, val):
    if(index<0 or index>alist.size):
        raise IndexError
    else:
        if(alist==List([None]*1,0,1)):
            alist.space=alist.space+1
            alist.list=[val]+[None]
            alist.size=alist.size+1
        else:
            if(alist.size==alist.space):
                alist.space=(alist.size+1)
                rlist=[None]*alist.space
                for i in range(alist.size):
                    rlist[i]=alist.list[i]
                alist.list=rlist
            hold=alist.list[index]
            alist.list[index]=val
            for i in range(index+1,alist.size+1):
                next=alist.list[i]
                alist.list[i]=hold
                hold=next
            alist.size=alist.size+1
        return alist
    
def add_plus20(alist, index, val):
    if(index<0 or index>alist.size):
        raise IndexError
    else:
        if(alist==List([None]*1,0,1)):
            alist.space=alist.space+1
            alist.list=[val]+[None]
            alist.size=alist.size+1
        else:
            if(alist.size==alist.space):
                alist.space=(alist.size+20)
                rlist=[None]*alist.space
                for i in range(alist.size):
                    rlist[i]=alist.list[i]
                alist.list=rlist
            hold=alist.list[index]
            alist.list[index]=val
            for i in range(index+1,alist.size+1):
                next=alist.list[i]
                alist.list[i]=hold
                hold=next
            alist.size=alist.size+1
        return alist
    
#Array -> Int
#takes in a Array as an argument and returns the number of elements currently in the list
def length(alist):
    return alist.size

#Array, Int -> AnyType
#takes in a Array and an integer index and returns the value at the index position in the Array
#Raises IndexError exception if index is not defined in the Array
def get(alist,index):
    if(index<0 or index>=alist.size):
        raise IndexError
    else:
        return alist.list[index]
        
#Array, Int, AnyType -> Array
#takes a Array, an integer index, and another value and replaces the element at index position in the Array with the given value
#Raises IndexError exception if index is not defined in the Array
def set(alist,index,val):
    if(index<0 or index>=alist.size):
        raise IndexError
    else:
        alist.list[index]=val
        return alist

#Array, Int -> Array, AnyType
#takes an Array and an integer index as arguments and removes the element at the index position from the Array and returns the new Array and the removed AnyType
#Raises IndexError exception if index is not defined in the Array
def remove(alist, index):
    if(index<0 or index>=alist.size or alist==List([None]*1,0,1)):
        raise IndexError
    else:
        count=0
        rlist=[]
        val=None
        for i in alist.list:
            if(count==index):
                val=i
            else:
                rlist=rlist+[i]
            count=count+1
        alist.size=alist.size-1
        alist.list=rlist+[None]
    return (val,alist)


#Array, anyFunction -> None
#takes in an Array and a function as arguments and applies the provided function to the value at each position in the Array
def foreach(alist,func):
    for i in range(alist.size):
        func(alist.list[i])
        
#Array -> Array
#takes in a Array and a "less-than" function as arguments and sorts the Array such that the elements are in ascending order as determined by the "less-than" function
def sort(alist, comp):
    for i in range(alist.size+1):
        for j in reversed(range(1,i)):
            if(comp(alist.list[j],alist.list[j-1])==True):
                temp=alist.list[j]
                alist.list[j]=alist.list[j-1]
                alist.list[j-1]=temp
    return alist

#Compare function
def compareinc(a,b):
    if(a<b):
        return True
    elif(a>b):
        return False
    else:
        return True
#                        :)
        