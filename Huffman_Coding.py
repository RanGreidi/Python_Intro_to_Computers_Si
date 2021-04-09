import Huffman_code_interface
from functools import total_ordering
import os
import math

class HeapNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

class HuffmanCoding(Huffman_code_interface.HuffmanCoding):  # This is the way you construct a class that inherits properties

    def __init__(self, path):
        self.path = path
        self.heap = []
        self.coding_dictionary = {}
        self.reverse_mapping = {}
        self.compressed_file_path = None
        self.extension=''
        self.freq_dict={}
        self.compress()

    def make_bin_frequency_dict(self, text):
        frequency = {}

        for byte in iter(lambda: text.read(1), b''):
            byte=int.from_bytes(byte, byteorder='big')
            if not byte in frequency:
                frequency[byte] = 0
            frequency[byte] += 1
        self.freq_dict = frequency
        return frequency
      
    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        self.freq_dict = frequency            
        return frequency
    
    def sort_node_list(self, node_list): 
        ''' this takes a list of nodes and return a new list with nodes but sorted'''
        node_list= sorted(node_list, key=lambda HeapNode: HeapNode.freq)
        return node_list
  
    def make_heap(self, frequency): 

        ''' this makes a sorted list (called heap) with sorted by thier 
        freq nodes and makes self.heap as that list
        input: a dict with char and frq
        output: changes self.heap to a list of sortes nodes
        '''
        for key in frequency:
            self.heap.append((frequency[key],key)) 
        node_heap = []
        for let in self.heap:
            node = HeapNode(let[1],let[0])
            node_heap.append(node)
        self.heap = node_heap
        self.heap=self.sort_node_list(self.heap)    
        
    def merge_nodes(self):
        '''build the f tree, it takes self.heap and makes it a tree'''
        while(len(self.heap)>1):
            node1 = self.heap.pop(0)
            node2 = self.heap.pop(0)

            merged = HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
    
            self.heap.append(merged)
            self.heap=self.sort_node_list(self.heap)
    
    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.coding_dictionary[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = self.heap[0]
        current_code = ""
        self.make_codes_helper(root, current_code)
        
    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.coding_dictionary[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        ''' this function does the following:
        becouse we cannot write a not devisiable by 8 sized file to the harddisck it takes the divides all
        of the chars in the binery string and checks how many chars we need to add so the numbr of ones and zeros
        wil be a multiple of 8 then it adds a byte that represents the number of how many zeros we added so we can remembr when we
        decompress '''
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_bin_encoded_text(self,file):
        encoded_text = ""
        for byte in iter(lambda: file.read(1), b''):
            byte=int(int.from_bytes(byte, byteorder='big'))
            encoded_text += self.coding_dictionary[byte]
        return str(encoded_text)

    def get_byte_array(self, padded_encoded_text):
        ''' so now i have a string ('10010102' for exp) and its size is number of chars* 8 bits
        we want to make it smaller, so bytearray takes the whole string and makes it a int which has a size
        of 8 bits which is a lot less  '''
        if(len(padded_encoded_text) % 8 != 0):
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename +"_Compressed"+".bin"
        if file_extension =='.txt':
            self.extension='.txt'
            with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
                text = file.read()
                
                frequency = self.make_frequency_dict(text)
                self.make_heap(frequency)
                self.merge_nodes()
                self.make_codes()

                encoded_text = self.get_encoded_text(text)
                padded_encoded_text = self.pad_encoded_text(encoded_text)

                b = self.get_byte_array(padded_encoded_text)
                output.write(bytes(b))
        if file_extension == '.bin':
            self.extension='.bin'
            with open(self.path, 'rb') as file, open(output_path, 'wb') as output:
                frequency = self.make_bin_frequency_dict(file)
                self.make_heap(frequency)
                self.merge_nodes()
                self.make_codes()
            with open(self.path, 'rb') as file1, open(output_path, 'wb') as output:
                encoded_text = self.get_bin_encoded_text(file1)
                padded_encoded_text = self.pad_encoded_text(encoded_text)
                b = self.get_byte_array(padded_encoded_text)
                output.write(bytes(b))
        self.compressed_file_path=output_path
        return output_path

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decode_bin_text(self, encoded_text):
        current_code = ""
        decoded_text = []

        for bit in encoded_text:
            current_code += bit
            if(current_code in self.reverse_mapping):
                character = self.reverse_mapping[current_code]    # a number need to be a  byte  again (01010101)
                decoded_text.append(character)
                current_code = ""

        return bytearray(decoded_text)

    def decompress_file(self, input_path):
        filename, file_extension = os.path.splitext(self.path)

        if  self.extension =='.txt':
            output_path = filename + "_decompressed" + ".txt"
            with open(input_path, 'rb') as file, open(output_path, 'w') as output:
                bit_string = ""

                byte = file.read(1)
                while byte != b"":
                    byte = ord(byte)
                    bits = bin(byte)[2:].rjust(8, '0')
                    bit_string += bits
                    byte = file.read(1)

                encoded_text = self.remove_padding(bit_string)

                decompressed_text = self.decode_text(encoded_text)
                
                output.write(decompressed_text)
        if  self.extension =='.bin':
            output_path = filename + "_decompressed" + ".bin"   
            with open(input_path, 'rb') as file, open(output_path, 'wb') as output:             
                bit_string = ""
                byte = file.read(1)
                while byte != b"":
                    byte = ord(byte)
                    bits = bin(byte)[2:].rjust(8, '0')
                    bit_string += bits
                    byte = file.read(1)     
                encoded_text = self.remove_padding(bit_string)  #ones and zeros
                decompressed_array=self.decode_bin_text(encoded_text)
                output.write(decompressed_array)

        return str(output_path)       

    def calculate_entropy(self):
        ''' This method calculates the entropy associated with the distribution
         of symbols in a previously compressed file.
        Input: None.
        Output: entropy (float).
        '''
        #tot sum
        tot_sum=0
        for char1 in self.freq_dict:
            tot_sum+=self.freq_dict[char1]
        #entropy
        entnropy = 0
        for char in self.freq_dict:
            w_i=self.freq_dict[char]/tot_sum #wi
            entnropy +=w_i * math.log(w_i,2)
        entnropy = entnropy*(-1) 
        return float(entnropy)

if __name__ == '__main__':  # You should keep this line for our auto-grading code.
    'bassad'