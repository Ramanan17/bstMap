import os
from string import punctuation
class HashSet:
  def __init__(self,lists=None):
    self.word_list = lists
    self.encoded_collection = []
    self.applyHash()
  def applyHash(self):
    for word in self.word_list:
      hashValue = [ord(char) for char in word]
      if hashValue not in self.encoded_collection:
        self.encoded_collection.append(hashValue)
  def getData(self):
    return ["".join([chr(value) for value in encodes])for encodes in self.encoded_collection]
    
# Define Node object for bst class
class Node(object):
    def __init__(self, parent, key, value):
        self.key = key
        self.value = value
        self.size = 1 
        self.parent = parent
        self.left = None
        self.right = None
    
    # Update the size (important!)
    def update(self):
        self.size = (0 if self.left is None else self.left.size) + (0 if self.right is None else self.right.size) 

    # Add an additional member to the Node.
    def insert(self, key, value):
        self.size += 1
        if key < self.key:
            if self.left is None:
                self.left = Node(self, key, value)                
                return self.left
            else:
                return self.left.insert(key, value)
        else:
            if self.right is None:
                self.right = Node(self, key, value)   
                return self.right
            else:
                return self.right.insert(key, value)

    # Search the Node for a member.
    def search(self, key):
        if key == self.key:
            return self
        elif key < self.key:
            if self.left is None:
                return None
            else:
                return self.left.search(key)
        else:
            if self.right is None:
                return None
            else:
                return self.right.search(key)

    # Returns Node with the smallest key in the subtree.
    def minimum(self): # Basically walks down the tree.
        current = self
        while current.left is not None:
            current = current.left
        return current
        
    # Returns the node with the smallest key larger than this node's key, or None if this has the largest key in the tree.
    def successor(self):
        if self.right is not None:
            return self.right.minimum()
        current = self
        while current.parent is not None and current.parent.right is current:
            current = current.parent
        return current.parent

    # Delete the Node from tree
    def delete(self):
        # Basically to delete, set the pointer of the parent directly onto the subtree. No need to handle garbage collecvtion.
        if self.left is None or self.right is None:
            if self is self.parent.left:
                self.parent.left = self.left or self.right
                if self.parent.left is not None:
                    self.parent.left.parent = self.parent
            else:
                self.parent.right = self.left or self.right
                if self.parent.right is not None:
                    self.parent.right.parent = self.parent 
            current = self.parent
            while current.key is not None:
                current.update()
                current = current.parent
            return self
        else:
            s = self.successor()
            self.key, s.key = s.key, self.key
            return s.delete()        
            
    def __repr__(self):
        return "Node with key:" + str(self.key) + ""

# Binary search tree implementation.
class BinarySearchTree(object):
    def __init__(self):
        self.root = None
        self.Node = Node
        self.psroot = self.Node(None, None, None)
    
    def reroot(self):
        self.root = self.psroot.left

    # Insert into the tree.
    def insert(self, key, value):
        if self.root is None:
            self.psroot.left = self.Node(self.psroot, key, value)
            self.reroot()
            return self.root
        else:
            return self.root.insert(key, value)
    
    # Return the node for key if is in the tree. Default None.
    def search(self, key):
        if self.root is None:
            return None
        else:
            return self.root.search(key) 
    
    # Delete the node for key t if it is in the tree.
    def delete(self, key):
        node = self.search(key)
        if not node is None:
            deleted = node.delete()
            self.reroot()
            return deleted
        return None

    def __repr__(self):
        return "BST"
class HashMap(object):
  def __init__(self, size):
    self.count = 0
    # This is a fixed size!!!
    self.size = size
    self.stack = [BinarySearchTree() for i in range(size)]

  # Still rely on python for the hash.
  def hashme(self, key):
    return key.__hash__() % self.size

  def set(self, key, value):
    hashvalue = self.hashme(key)
    # If the key already exists, find it and set the value.
    findNode = self.stack[hashvalue].search(key)
    if not findNode is None: # Handle replacement
      findNode.value = value
    else: # The key does not exist, so add its hash (which is always a number) to the tree.
      self.stack[hashvalue].insert(key, value)
      self.count += 1
    # We will always return True here because worst case, we just append it to a list. This has speed problems but by nature of being fixed size, we can't do much about it.
    return True

  def get(self, key):
    hashvalue = self.hashme(key)
    # This defaults None.
    findNode = self.stack[hashvalue].search(key)
    if not findNode is None:
      return findNode.value
    return None

  def delete(self, key):
    hashvalue = self.hashme(key)
    findNode = self.stack[hashvalue].search(key)
    if not findNode is None:
      retval = self.stack[hashvalue].delete(key)
      self.count -= 1
      return retval.value
    return None

  # As with chaining, it is possible to have load factor > 1.
  def load(self):
    if (self.count + self.size == 0): 
      return 0
    return self.count / float(self.size)

  # Python has default __getitem__ and __setitem__ functions.
  def __getitem__(self, key):
    return self.get(key)

  def __setitem__(self, key, value):
    return self.set(key, value)

  def __repr__(self):
    return "HashMap of size :%d" % self.size 



# Get the txt files
files = list(filter(lambda x:"txt" in x,os.listdir()))

# Read and process each file:
for file in files:
  print(f"\nProcessing File {file}(May take some time)...\n")
  words = []
  count_dictionary = {}
  f = open(file,"r")
  for line in f.readlines():
    word_list = list(filter(lambda x:x.isalpha() and len(x)>4 and x not in list(punctuation),line.replace("\n","").split()))
    words+=word_list


  unique_words = list(set(words))
  word_dict = dict.fromkeys(unique_words,0)
  for word in words:
    if len(word)>4:
      word_dict[word]+=1
  filtered_words =list(sorted(word_dict.items(),key=lambda x:(x[1],x[0]),reverse=True))[:10]
  # print(filtered_words)
  print("Results of python set and dictionary:")
  print("*"*36)
  print(f"{'words':<10} {'count':>10}\n")
  for word,count in filtered_words:
    print(f"{word:<10} {count:>10}")
  print("\nProcessing the data with custom hashMap and BST.(May take quite a bit of time time please wait...)")
  hashSet = HashSet(words)
  bstMap = HashMap(len(words))
  for word in hashSet.getData():
    bstMap.set(word,None)
  for word in words:
      value = bstMap.get(word)
      if value is None:
        bstMap.set(word,1)
      else:
        bstMap.set(word,value+1)
  filtered_values = sorted([(key,bstMap.get(key)) for key in hashSet.getData()],key=lambda x:(x[1],x[0]),reverse=True)[:10]
  print("\nResults of custom HasMap and BST:")
  print("*"*36)
  print(f"{'words':<10} {'count':>10}\n")
  for word,count in filtered_values:
    print(f"{word:<10} {count:>10}")
  



  

