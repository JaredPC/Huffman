import unittest
import filecmp
import array_list
import linked_list
from huffman_bits_io import *


#String -> List
#takes in a text-file name and opens the file and counts the frequency of occurrences of all the characters within that file.
def count_occurances(path):
    file=open_file(path)
    if(file==None):
        return None
    else:
        huffcount=array_list.List([0]*256,256,256)
        for line in file:
            for ch in line:
                val=ord(ch)
                huffcount=array_list.set(huffcount, val , array_list.get(huffcount,val)+1)
        file.close()
        return huffcount

#File Directory -> File
#takes in a File Directory and opens that file and returns that file
def open_file(path):
    try:
        file=open(path,'r')
    except (FileNotFoundError, IOError):
        print("{} : No such file or directory".format(path), flush=True)
        file=None
    return file


#A Huffman Tree is a Binary tree containing either
#-A leaf with a character and a frequency of that character
#-A Node with a character, frequency, and a right and left subtree
#Leaf:
class Leaf:             
    def __init__(self, char, freq):
        self.char = char        #Int (Ascii representation of Character)
        self.freq = freq        #Int (frequency of that character)

    def __eq__(self, other):
        return ((type(other) == Leaf)
          and self.char == other.char
          and self.freq == other.freq
        )

    def __repr__(self):
        return ("Leaf({!r}, {!r})".format(self.char, self.freq))

#Node:
class Node:
    def __init__(self, char, freq, left, right):
        self.char = char        #Int (Ascii representation of Character)
        self.freq = freq        #Int (frequency of that character)
        self.left = left        #left subtree
        self.right = right      #right subtree

    def __eq__(self, other):
        return ((type(other) == Node)
          and self.char == other.char
          and self.freq == other.freq
          and self.left == other.left
          and self.right == other.right
        )

    def __repr__(self):
        return ("Node({!r}, {!r}, {!r}, {!r})".format(self.char, self.freq, self.left, self.right))

#Tree -> String
#creates a string from a given Huffman tree by traversing the tree in a pre-order traversal and appending the characters of the visited leaf nodes.
def huff_tostring(tree):
    if(tree==None):
        return ""
    elif(type(tree) == Leaf):
        return chr(tree.char)
    else:
        return huff_tostring(tree.left) + huff_tostring(tree.right)

#Tree, Tree -> True/False
#takes in 2 trees and returns true if the first tree comes before the second
def comes_before(a, b):
    if(a.freq < b.freq):
        return True
    elif(a.freq > b.freq):
        return False
    else:
        return (a.char<b.char)
    
#ArrayList -> Tree
#takes in a list of occurrences of characters and returns the root node of the created tree.
def build_Hufftree(alist):
    llist = convert_llist(alist)
    while (linked_list.length(llist) > 1):
        node1,llist=linked_list.remove(llist, 0)
        node2,llist=linked_list.remove(llist, 0)
        n=Node(0,(node1.freq+node2.freq),node1,node2)
        n.char=(node1.char<node2.char) and node1.char or node2.char
        llist=linked_list.insert_sorted(llist, n, comes_before)
    if(llist==None):
        return None
    else:
        return linked_list.get(llist, 0)

#ArrayList -> LinkedList
#takes in an arrayList of character counts and returns a linked list of leaf nodes
def convert_llist(alist):
    llist=None
    for i in range(array_list.length(alist)-1):
        g=array_list.get(alist, i)
        if(g != 0):
            llist=linked_list.insert_sorted(llist,Leaf(i,g),comes_before)
    return llist

#Tree, ArrayList -> None
#takes in a tree and traverses the huffman tree and builds a list of character codes
def build_codes(tree,alist,accl=""):
    if(tree==None):
        return tree
    if(type(tree)==Node):
        build_codes(tree.left,alist,accl+"0")
        build_codes(tree.right,alist,accl+"1")
    else:
        array_list.set(alist,tree.char,accl)

#String, String -> String
#takes in an input file name with data and Huffman encodes it to the output file name. Returns the Huffman Tree in string form
def huffman_encode(infile,outfile):
    chrcount=count_occurances(infile)                   #Arraylist containing the counts of each character
    htree=build_Hufftree(chrcount)                      #HuffmanTree of all the characters
    codelist=array_list.List([None]*256,256,256)        #Arraylist containing the codes of each character
    build_codes(htree, codelist)
    bitwriter=HuffmanBitsWriter(outfile)                #HuffmanBitsWriter
    header_writer(bitwriter,chrcount)                   #Writes the header
    file_encoder(bitwriter, infile, codelist)           #Encodes the file
    bitwriter.close()                                   #Closes the HuffmanBitsWriter
    return huff_tostring(htree)                         

#HuffmanBitsWriter, ArrayList -> None
#Takes in a HuffmanBitsWriter and an arraylist of character counts and writes the header for the encoded file
def header_writer(bitwriter,alist):
    count=0
    for i in range(array_list.length(alist)-1):
        if(array_list.get(alist,i) != 0):
            count+=1
    bitwriter.write_byte(count)
    for i in range(array_list.length(alist)-1):
        if(array_list.get(alist,i) != 0):
            bitwriter.write_byte(i)
            bitwriter.write_int(array_list.get(alist,i))

#HuffmanBitsWriter, String, ArrayList -> None
#Takes in a HuffmanBitsWriter, name of file and an arraylist of character codes and writes the file to the file
def file_encoder(bitwriter, infile, alist):
    file=open_file(infile)
    for line in file:
            for ch in line:
                bitwriter.write_code(array_list.get(alist,ord(ch)))
    file.close()
    
#String, String -> None
#takes in a compressed text file and writes the decompressed text into an output text file.
def huffman_decode(infile,outfile):
    bitreader=HuffmanBitsReader(infile)                 #Creates the HuffmanBitsReader object
    charcount=header_reader(bitreader)                  #Creates an ArrayList of chracter counts
    htree=build_Hufftree(charcount)                     #Creates a Huffman Tree out of the character count list
    count=0
    for i in range(256):
        count+=array_list.get(charcount,i)
    file=open(outfile,'w')                         #Creates the File we are writing to
    while(count>0):
        file.write(read_bin(htree, bitreader))
        count-=1
    bitreader.close()
    file.close()
    
#HuffmanBitsReader, HuffmanTree -> Character
#Takes in a HuffmanBitsReader and a HuffmanTree and returns a single ASCII character
def read_bin(htree,bitreader):
    if(type(htree)==Leaf):
        return chr(htree.char)
    else:
        bit=bitreader.read_bit()
        if(bit==True):
            return read_bin(htree.right, bitreader)
        else:
            return read_bin(htree.left, bitreader)
    
    
#HuffmanBitsReader -> ArrayList
#Takes in a HuffmanBitsReader and returns an Arraylist containing the count of each character in the file
def header_reader(bitreader):
    alist= array_list.List([0]*256,256,256)
    count=bitreader.read_byte()
    for i in range(count):
        char=bitreader.read_byte()
        num=bitreader.read_int()
        alist=array_list.set(alist,char,num)
    return alist


class TestHoffman(unittest.TestCase):
    test1=Leaf(10,10)
    def test_leaf__repr__(self):
        self.assertEqual(repr(self.test1), "Leaf(10, 10)")
    def test_leaf__eq__(self):
        self.assertEqual(self.test1==Leaf(10,10), True)
        self.assertEqual(self.test1==Leaf(9,10), False)
    test2=Node(10,20,Leaf(10,10),Leaf(11,10))
    def test_node__repr__(self):
        self.assertEqual(repr(self.test2), "Node(10, 20, Leaf(10, 10), Leaf(11, 10))")
    def test_node__eq__(self):
        self.assertEqual(self.test2==Node(10,20,Leaf(10,10),Leaf(11,10)), True)
        self.assertEqual(self.test2==Node(10,20,Leaf(10,5),Leaf(11,10)), False)
    def test_count_occurances(self):
        help=count_occurances("help.txt")
        self.assertEqual(help,None)
        self.assertEqual(count_occurances("none.txt"),None)
        self.assertEqual(count_occurances("test1.txt"),array_list.List([0]*10+[1]+[0]*21+[2]+[1]*64+[2]*7+[1]*23+[0]*129,256,256))
    def test_open_file(self):
        self.assertEqual(open_file("none.txt"),None)
    def test_huff_tostring(self):
        self.assertEqual(huff_tostring(None),"")
        self.assertEqual(huff_tostring(Node(71,20,Leaf(71,10),Leaf(80,10))),"GP")
        self.assertEqual(huff_tostring(Node(69,40,Node(69,20,Leaf(69,10),Leaf(71,10)),Node(75,20,Leaf(75,10),Leaf(76,10)))),"EGKL")
    def test_comes_before(self):
        self.assertEqual(comes_before(Leaf(10,10),Leaf(11,15)), True)
        self.assertEqual(comes_before(Leaf(10,20),Leaf(11,15)), False)
        self.assertEqual(comes_before(Node(10,20,Leaf(10,10),Leaf(11,10)),Leaf(11,20)), True)
    def test_convert_llist(self):
        self.assertEqual(convert_llist(array_list.List([10,0,0,1,2,3,0],7,7)),
                         linked_list.Pair(Leaf(3, 1), linked_list.Pair(Leaf(4, 2), linked_list.Pair(Leaf(5, 3), linked_list.Pair(Leaf(0, 10), None)))))
    def test_build_Hufftree(self):
        self.assertEqual(build_Hufftree(array_list.List([0]*256,256,256)),None)
        self.assertEqual(build_Hufftree(count_occurances("test1.txt")),Node(10, 104, Node(10, 40, Node(103, 16, Node(103, 8, Node(103, 4, Leaf(103, 2), Node(105, 2, Leaf(105, 1), Leaf(106, 1))), Node(107, 4, Node(107, 2, Leaf(107, 1), Leaf(108, 1)), Node(109, 2, Leaf(109, 1), Leaf(110, 1)))), Node(111, 8, Node(111, 4, Node(111, 2, Leaf(111, 1), Leaf(112, 1)), Node(113, 2, Leaf(113, 1), Leaf(114, 1))), Node(115, 4, Node(115, 2, Leaf(115, 1), Leaf(116, 1)), Node(117, 2, Leaf(117, 1), Leaf(118, 1))))), Node(10, 24, Node(119, 8, Node(119, 4, Node(119, 2, Leaf(119, 1), Leaf(120, 1)), Node(121, 2, Leaf(121, 1), Leaf(122, 1))), Node(123, 4, Node(123, 2, Leaf(123, 1), Leaf(124, 1)), Node(125, 2, Leaf(125, 1), Leaf(126, 1)))), Node(10, 16, Node(10, 8, Node(10, 4, Node(10, 2, Leaf(10, 1), Leaf(33, 1)), Leaf(32, 2)), Node(34, 4, Node(34, 2, Leaf(34, 1), Leaf(35, 1)), Node(36, 2, Leaf(36, 1), Leaf(37, 1)))), Node(38, 8, Node(38, 4, Node(38, 2, Leaf(38, 1), Leaf(39, 1)), Node(40, 2, Leaf(40, 1), Leaf(41, 1))), Node(42, 4, Node(42, 2, Leaf(42, 1), Leaf(43, 1)), Node(44, 2, Leaf(44, 1), Leaf(45, 1))))))), Node(46, 64, Node(46, 32, Node(46, 16, Node(46, 8, Node(46, 4, Node(46, 2, Leaf(46, 1), Leaf(47, 1)), Node(48, 2, Leaf(48, 1), Leaf(49, 1))), Node(50, 4, Node(50, 2, Leaf(50, 1), Leaf(51, 1)), Node(52, 2, Leaf(52, 1), Leaf(53, 1)))), Node(54, 8, Node(54, 4, Node(54, 2, Leaf(54, 1), Leaf(55, 1)), Node(56, 2, Leaf(56, 1), Leaf(57, 1))), Node(58, 4, Node(58, 2, Leaf(58, 1), Leaf(59, 1)), Node(60, 2, Leaf(60, 1), Leaf(61, 1))))), Node(62, 16, Node(62, 8, Node(62, 4, Node(62, 2, Leaf(62, 1), Leaf(63, 1)), Node(64, 2, Leaf(64, 1), Leaf(65, 1))), Node(66, 4, Node(66, 2, Leaf(66, 1), Leaf(67, 1)), Node(68, 2, Leaf(68, 1), Leaf(69, 1)))), Node(70, 8, Node(70, 4, Node(70, 2, Leaf(70, 1), Leaf(71, 1)), Node(72, 2, Leaf(72, 1), Leaf(73, 1))), Node(74, 4, Node(74, 2, Leaf(74, 1), Leaf(75, 1)), Node(76, 2, Leaf(76, 1), Leaf(77, 1)))))), Node(78, 32, Node(78, 16, Node(78, 8, Node(78, 4, Node(78, 2, Leaf(78, 1), Leaf(79, 1)), Node(80, 2, Leaf(80, 1), Leaf(81, 1))), Node(82, 4, Node(82, 2, Leaf(82, 1), Leaf(83, 1)), Node(84, 2, Leaf(84, 1), Leaf(85, 1)))), Node(86, 8, Node(86, 4, Node(86, 2, Leaf(86, 1), Leaf(87, 1)), Node(88, 2, Leaf(88, 1), Leaf(89, 1))), Node(90, 4, Node(90, 2, Leaf(90, 1), Leaf(91, 1)), Node(92, 2, Leaf(92, 1), Leaf(93, 1))))), Node(94, 16, Node(94, 8, Node(94, 4, Node(94, 2, Leaf(94, 1), Leaf(95, 1)), Node(96, 2, Leaf(96, 1), Leaf(104, 1))), Node(97, 4, Leaf(97, 2), Leaf(98, 2))), Node(99, 8, Node(99, 4, Leaf(99, 2), Leaf(100, 2)), Node(101, 4, Leaf(101, 2), Leaf(102, 2))))))))
    def test_build_codes(self):
        test3=Node(71,20,Leaf(71,10),Leaf(80,10))
        test4=array_list.List([None]*256,256,256)
        test5=None
        test6=array_list.List([None]*256,256,256)
        build_codes(test3, test4)
        build_codes(test5, test6)
        self.assertEqual(test4,array_list.List([None]*71+["0"]+[None]*8+["1"]+[None]*175,256,256))
        self.assertEqual(test6,array_list.List([None]*256,256,256))
    def test_huffman_encode(self):
        huff=huffman_encode("file0.txt","file0_encoded.bin")
        huffman_decode("file0_encoded.bin", "file0Result.txt")
        self.assertEqual(huff," bdca")
        self.assertTrue(filecmp.cmp("file0.txt","file0Result.txt"))
        self.assertTrue(filecmp.cmp("file0_encoded.bin", "file0_encoded_check.bin"))
        huffman_encode("TestMedium.txt", "medium_encode.bin")
        huffman_decode("medium_encode.bin", "TestMediumResult.txt")
        self.assertTrue(filecmp.cmp("TestMedium.txt", "TestMediumResult.txt"))
    def test_huffman_decode(self):
        huffman_decode("file0_encoded_check.bin", "file0_decoded.txt")
        self.assertTrue(filecmp.cmp("file0_decoded.txt","file0.txt"))
        huffman_encode("emptytest.txt", "emptyencode.bin")
        huffman_decode("emptyencode.bin", "emptyresult.txt")
        self.assertTrue(filecmp.cmp("emptytest.txt","emptyresult.txt"))
if __name__ == "__main__":
    #print(count_occurances("test1.txt"))
    #print(huffman_encode("file0.txt","file0_encoded.bin"))
    #print(huffman_encode("TestMedium.txt", "medium_encode.bin"))
    #huffman_decode("medium_encode.bin", "medium_decode.txt")
    #print(huffman_encode("TestLong.txt", "encodelong.bin"))
    #huffman_decode("encodelong.bin", "longresult.txt")
    #print(filecmp.cmp("longresult.txt", "TestLong.txt"))
    #huffman_encode("emptytest.txt", "emptyencode.bin")
    #huffman_decode("emptyencode.bin", "emptyresult.txt")
    unittest.main()
        