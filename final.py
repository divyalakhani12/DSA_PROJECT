def new_node(char=None,freq=0,left=None,right=None):
    '''
    

    Parameters:
    char (str): 
    freq (int):
    left (NoneType):
    right (NoneType):

    Returns:
    dict: 
    '''
    return {"char":char,"freq":freq,"left":left,"right":right} 

def calculate_frequencies(text):
    '''
    Finds the frequency of all the characters in text.

    Parameters:
    text (str): The text from the file.

    Returns:
    list: A list of dictinary representing frequency in the format:
        {char, freq, left: None, right: None}
    '''
    frequency={}
    for char in text:
        if char in frequency:
            frequency[char]=frequency[char]+1
        else:
            frequency[char]=1
    result=[]
    for char,freq in frequency.items():
        result.append(new_node(char,freq))
    return result

def priority_queueenqueue(queue,item): 
    '''
    Enqueue an item onto the priority_queue (represented as a list)

    Parameters:
    queue (list): 
    item (tuple):

    Return: None
    '''
    queue.append(item) # item=(leaf["freq"], count, leaf)
    idx=len(queue)-1 #stores the index of the last item (newly added item) 
    
    #while the new node is smaller than its parent, swap them.
    while idx>0:
        parent=(idx-1)//2 #child node 
        #parent node = idx*2+1 
        if queue[idx]<queue[parent]:
            queue[idx],queue[parent]=queue[parent],queue[idx]
            idx=parent
        else:
            break

def priority_queuedequeue(queue): #returns the smallest item thats the root node!
    '''
    Dequeue the item from the start of the queue. 

    Parameters:
    queue (list): 

    Returns:
    : 
    '''

    if not queue:
        return "queue is empty!"
    #root node is at index 0
    queue[0],queue[-1]=queue[-1],queue[0] #swapping the root node with the last element
    root_node=queue.dequeue()
    idx=0
    n=len(queue)
    #rearrange the list so that the order is correct again

    while not False:
        left=2*idx+1
        right=2*idx+2

        x=idx
        #check if the left child is smaller than the current smallest
        if left < n and queue[left]< queue[x]:
            x = left
            #check if the right child is smaller
        if right < n and queue[right] < queue[x]:
            x = right
        #if the smallest child is smaller than the current node, swap them
        if x != idx:
            queue[idx], queue[x] = queue[x], queue[idx]
            idx=x
        else:
            break

    return root_node

def build_huffman_tree(leaves):
    '''
    Builds huffman tree based

    Parameters:
    leaves (list): list of dictionaries 

    Returns:
    priority queue: 
    '''

    priority_queue=[]
    count=0  #to keep track of the order of the nodes
    for i in leaves:
        #enqueue (frequency, count, node)
        priority_queueenqueue(priority_queue, (i["freq"], count, i))
        count+=1

    # Build the Huffman tree by merging the two smallest nodes repeatedly
    while len(priority_queue)>1:
        freq1,_,left= priority_queuedequeue(priority_queue)
        freq2,_,right = priority_queuedequeue(priority_queue)
        merged=new_node(None, freq1 + freq2, left, right)
        priority_queueenqueue(priority_queue, (merged["freq"], count, merged))
        count += 1

    # The remaining node is the root of the Huffman tree
    return priority_queue[0][2]

def generate_huffman_codes(node, prefix="", codes=None):
    '''
    Generates unique code for aeach character

    Parameters:
    node (str): list of dictionaries 
    prefix (str):
    codes: 

    Returns:
    priority queue: 
    '''

    if codes is None:
        codes={}
    if node["char"] is not None: 
        codes[node["char"]]=prefix
    else:
        generate_huffman_codes(node["left"],  prefix + '0', codes)
        generate_huffman_codes(node["right"], prefix + '1', codes)
    return codes

def huffman_encode_file(filename):
    '''
    Reads, ecodes and generates a binary file.

    Parameters:
    filename (str):

    Returns:
    
     
    '''

    # 1) read and strip
    with open(filename, encoding='utf-8', errors='ignore') as f: #utf-8: text file can handle a wide variety of characters
        text_in_file=f.read().strip()

    # 2) build leaves and tree
    leaves=calculate_frequencies(text_in_file) 
    root=build_huffman_tree(leaves)

    # 3) generate codes
    codes=generate_huffman_codes(root)

    # 4) encode
    bit_string=''.join(codes[ch] for ch in text_in_file)

    return text_in_file,bit_string,codes

if __name__ == "__main__":
    filen=input("Enter the filename and write its extension(.txt) : ")
    actual_text,encoded_text,all_the_values=huffman_encode_file(filen)
    print("Word:",actual_text)
    print("Huffman code:",encoded_text)
    print("Converted values:",all_the_values)

    padded_bit_string = encoded_text + '0' * ((8 - len(encoded_text) % 8) % 8)  # pad to full bytes
    byte_array = bytearray()

    for i in range(0, len(padded_bit_string), 8):
        byte = padded_bit_string[i:i+8]
        byte_array.append(int(byte, 2))

    # Write binary data to file
    with open("compressed_output.bin", "wb") as bin_file:
        bin_file.write(byte_array)
