import unittest
from linked_list import *

class TestCase(unittest.TestCase):
    def test_interface(self):
        temp_list = empty_list()
        temp_list = add(temp_list, 0, "Hello!")
        length(temp_list)
        get(temp_list, 0)
        temp_list = set(temp_list, 0, "Bye!")
        remove(temp_list, 0)
    test1=None
    test2=Pair(10,None)
    test3=Pair(10,Pair(20,Pair(30,None)))
    def test__repr__(self):
        self.assertEqual(repr(self.test3),"Pair(10, Pair(20, Pair(30, None)))")
        self.assertEqual(repr(self.test2),"Pair(10, None)")
    def test__eq__(self):
        self.assertEqual(self.test1==None,True)
        self.assertEqual(self.test2==Pair(10,None),True)
    def test_empty_list(self):
        self.assertEqual(empty_list(),self.test1)
    def test_add(self):
        self.assertEqual(add(None,0,5), Pair(5,None))
        self.assertRaises(IndexError,add,Pair(10,None),-1,5)
        self.assertRaises(IndexError,add,Pair(10,None),3,5)
        self.assertEqual(add(Pair(10,Pair(20,Pair(30,None))),1,15), Pair(10,Pair(15,Pair(20,Pair(30,None)))))
        self.assertEqual(add(Pair(10,Pair(20,Pair(30,None))),3,35), Pair(10,Pair(20,Pair(30,Pair(35,None)))))
    def test_length(self):
        self.assertEqual(length(None), 0)
        self.assertEqual(length(Pair(10,None)), 1)
    def test_get(self):
        self.assertEqual(get(Pair(10,None),0),10)
        self.assertEqual(get(Pair(10,Pair(20,Pair(30,None))),2),30)
        self.assertRaises(IndexError,get,Pair(10,None),-1)
        self.assertRaises(IndexError,get,Pair(10,None),3)
    def test_remove(self):
        self.assertEqual(remove(Pair(10,None),0),(10,None))
        self.assertEqual(remove(Pair(10,Pair(20,Pair(30,None))),2),(30,Pair(10,Pair(20,None))))
        self.assertRaises(IndexError,remove,Pair(10,None),-1)
        self.assertRaises(IndexError,remove,Pair(10,Pair(20,Pair(30,None))),3)
        self.assertEqual(remove(Pair(10,Pair(20,Pair(30,None))),0),(10,Pair(20,Pair(30,None))))
        self.assertEqual(remove(Pair(10,Pair(20,Pair(30,None))),1),(20,Pair(10,Pair(30,None))))
    def test_set(self):
        self.assertEqual(set(Pair(10,None),0,5), Pair(5,None))
        self.assertEqual(set(Pair(10,Pair(20,Pair(30,None))),1,15), Pair(10,Pair(15,Pair(30,None))))
        self.assertRaises(IndexError,set,Pair(10,None),-1,5)
        self.assertRaises(IndexError,set,Pair(10,Pair(20,Pair(30,None))),3,10)
    def test_foreach(self):
        def addone(i):
            return i+1
        foreach(self.test2,addone)
        foreach(self.test1,addone)
        foreach(self.test3,addone)
        self.assertEqual(compareinc(5,5),True)
        self.assertEqual(compareinc(5,6),True)
        self.assertEqual(compareinc(6,5),False)
        #self.assertEqual(test5,List([1,2,3,4,5]+[None]*5,5,10))
        #self.assertEqual(self.test1,self.test1)
    def test_sort(self):
        test5=None
        test6=Pair(3,Pair(1,Pair(5,Pair(4,None))))
        test8=Pair("c",Pair("a",Pair("b",Pair("d",None))))
        test7=Pair(3,Pair(1,Pair(5,Pair(4,Pair(2,Pair(6,None))))))
        test9=Pair(6,Pair(1,Pair(5,Pair(4,Pair(2,Pair(3,None))))))
        self.assertEqual(sort(test5,compareinc),None)
        self.assertEqual(sort(test6,compareinc),Pair(1, Pair(3, Pair(4, Pair(5, None)))))
        self.assertEqual(sort(test7,compareinc),Pair(1, Pair(2, Pair(3, Pair(4, Pair(5, Pair(6, None)))))))
        self.assertEqual(sort(test9,compareinc),Pair(1, Pair(2, Pair(3, Pair(4, Pair(5, Pair(6, None)))))))
        self.assertEqual(sort(test8,compareinc),Pair('a', Pair('b', Pair('c', Pair('d', None)))))
    def test_insert_sorted(self):
        test10=Pair(10,Pair(20,Pair(30,None)))
        test11=None
        self.assertEqual(insert_sorted(test11,10,compareinc),Pair(10, None))
        self.assertEqual(insert_sorted(test10,5,compareinc), Pair(5,Pair(10,Pair(20,Pair(30,None)))))
        self.assertEqual(insert_sorted(test10,25,compareinc), Pair(10, Pair(20, Pair(25, Pair(30, None)))))
if (__name__ == '__main__'):
    unittest.main()
    