# Duncan Clarke
# 20056561
# I certify that this submission contains my own work, except as noted.
import os
import heapq

class node:
    """ A  node in the huffman tree, representing a character
    Attributes
    ---------------
    char (int)
        An integer containing the ascii value of the character
    freq (int):
        The frequency of the character
    left (node):
        The left child of the node in the tree (defaults to None)
    right (node):
        The right child of the node in the tree (defaults to None)
    """
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    def __lt__(self, other):
        # Modified comparison to compare frequencies of each node for tree building/traversing purposes
        return self.freq < other.freq

##########################
### Code-Building Module ###
##########################

def Code_Building(files):

    # Create dictionary of printable ascii codes with corresponding frequencies, all frequencies starting at 0
    frequencies = {10:0}
    for i in range(32, 127):
        frequencies[i] = 0

    # iterate through each file in the canonical collection
    for file in files:
        # iterate through each character in file string, incrementing ascii frequencies accordingly
        for char in file:
            frequencies[ord(char)] += 1

    # add character and frequencies as nodes in priority queue Q
    Q = []
    for elem in frequencies:
        freq = frequencies[elem]
        heapq.heappush(Q,node(elem, freq, None, None))
    heapq.heapify(Q)
    while len(Q) > 1:
        left = heapq.heappop(Q)
        right = heapq.heappop(Q)
        new = node(str(left.char) + str(right.char), left.freq + right.freq, left, right)
        heapq.heappush(Q, new)
    codes = getCodes(Q[0])
    # output all codestrings to a text file
    f = open("codestrings.txt", "w")
    for key, value in codes.items():
        f.write(str(key) + " " + str(value) + "\n")
    f.close()
    return codes

def getCodes(node, code='', codes = {}):
    # Traverses huffman tree and creates a dictionary with each character and corresponding huffman code
    if node.left == None: # No left node -> node must be leaf
        if code == "":
            # no huffman code exists
            code = "0"
        # add full codeword of leaf node character
        codes[node.char] = code
    else:
        getCodes(node.left, code+"0", codes)
        getCodes(node.right, code+"1", codes)
    return codes

#####################
### Encoding Module ###
#####################

def encode(file):
    # read huffman codestrings from file and build a dictionary of codestrings
    f = open("codestrings.txt", "r")
    lines = f.readlines()
    f.close()
    codes = {}
    for line in lines:
        code = line.split()
        codes[code[0]] = code[1]
    # encode given file with codes
    encoded = ''
    for char in file:
        ascii = ord(char) # convert current character to ascii representation
        # find ascii code in code dictionary and add encoded representation to the encoded string
        for key, value in codes.items():
            if key == str(ascii):
                encoded = encoded + value
                break
    return encoded

#####################
### Decoding Module ###
#####################

def decode(encoded):
    # read huffman codestrings from file and build a dictionary of codestrings
    f = open("codestrings.txt", "r")
    lines = f.readlines()
    f.close()
    codes = {}
    for line in lines:
        code = line.split()
        codes[code[0]] = code[1]
    # build a binary tree from the root with 0 left children and 1 right children
    initial = binary_node(None,'')
    root = build_tree(initial, initial, codes)
    node = root
    decoded = ''
    for char in encoded:
        # follow the binary tree down based on each bit read from encoded string
        if char == "0":
            node = node.left
        else:
            node = node.right
        if node.left == None and node.right == None:
            # Leaf node -> add decoded character to decoded string
            decoded += chr(int(node.char))
            node = root # restart from root
    # Produce encoded version of the encoded file
    f = open("File2ASCII_decoded.txt", "w")
    f.write(decoded)
    f.close()

class binary_node():
    """ A  node in a tree representing huffman codes, each node representing a binary string
    Attributes
    ---------------
    char (int)
        An integer containing the ascii value of the character
    code (int):
        The binary string
    left (node):
        The left child of the node in the tree (defaults to None)
    right (node):
        The right child of the node in the tree (defaults to None)
    """
    def __init__(self, char, code, left=None, right=None):
        self.char = char
        self.code = code
        self.left = left
        self.right = right

def build_tree(root, node, codes):
    # current node value is a relevant code
    if node.code in codes.values():
        for key in codes:
            if codes[key] == node.code:
                node.char = key
    # current node value is not relevant code
    else:
        if any((node.code + '0') in code for code in codes.values()):
            new = binary_node(None, node.code + '0')
            node.left = new
            build_tree(root, new, codes)
        if any((node.code + '1') in code for code in codes.values()):
            new = binary_node(None, node.code + '1')
            node.right = new
            build_tree(root, new, codes)
    return root

def main():
    #########################
    ### Part 1 demonstration ###
    #########################

    # open file1 and file2... read the contents into strings
    file = open("file1ASCII.txt", 'r')
    file_1 = file.read()
    file.close()
    file = open("file2ASCII.txt", 'r')
    file_2 = file.read()
    file.close()
    # build the codestring file for file1
    Code_Building([file_1])
    # encode file2 with the codestring generated from file1
    encoded = encode(file_2)
    # decode file2 with the codestring generated from file1
    decode(encoded)

    #########################
    ### Part 2 demonstration ###
    #########################

    # CANONICAL COLLECTION 1

    filenames = ['Earth', 'Mystery', 'Myths', 'Simak', 'Wodehouse']

    # read files in canonical collection and build codestring dictionary
    canonical_collection_1 = []
    file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Canonical Collection 1','words1ASCII.txt'),'r')
    canonical_collection_1.append(file.read())
    file.close()
    Code_Building(canonical_collection_1)

    # read and encode files in Data.zip, measuring the amount of bits in each encoded file in a dictionary
    sizes_1 = {}
    for filename in filenames:
        file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Data 20191031', filename + 'ASCII.txt'),'r')
        encoded = encode(file.read())
        sizes_1[filename] = len(encoded)
    print("Canonical Collection 1 encoded file lengths:")
    print(sizes_1)
    print("\n")


    # CANONICAL COLLECTION 2

    # read files in canonical collection and build codestring dictionary
    canonical_collection_2 = []
    for i in range(1,11):
        file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Canonical Collection 2','Short Text ' + str(i) + 'ASCII.txt'),'r')
        canonical_collection_2.append(file.read())
        file.close()
    Code_Building(canonical_collection_2)

    # read and encode files in Data.zip, measuring the amount of bits in each encoded file in a dictionary
    sizes_2 = {}
    for filename in filenames:
        file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Data 20191031', filename + 'ASCII.txt'),'r')
        encoded = encode(file.read())
        sizes_2[filename] = len(encoded)
    print("Canonical Collection 2 encoded file lengths:")
    print(sizes_2)
    print("\n")

    # CANONICAL COLLECTION 3

    # read files in canonical collection and build codestring dictionary
    canonical_collection_3 = []
    file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Canonical Collection 3','ChestertonASCII.txt'),'r')
    canonical_collection_3.append(file.read())
    file.close()
    file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Canonical Collection 3','DickensASCII.txt'),'r')
    canonical_collection_3.append(file.read())
    file.close()
    Code_Building(canonical_collection_3)

    # read and encode files in Data.zip, measuring the amount of bits in each encoded file in a dictionary
    sizes_3 = {}
    for filename in filenames:
        file = open(os.path.join(os.path.dirname('Assignment 3.py'),'Data 20191031', filename + 'ASCII.txt'),'r')
        encoded = encode(file.read())
        sizes_3[filename] = len(encoded)
    print("Canonical Collection 3 encoded file lengths:")
    print(sizes_3)


if __name__== "__main__":
  main()
