from node import node
from priorityQueue import priorityQueue as pq
from collections import defaultdict
import os
import io
import time
from prettytable import PrettyTable


def obtain_frequencies(aBook):
    """
    This method is used to obtain the frequencies of each character in the text file.
    :param aBook:
    :return:
    """
    with io.open("Books/" + aBook, 'r', encoding='utf8') as file:
        book = file.read()
    dict1 = defaultdict(int)
    for i in book:
        dict1[i] += 1
    return dict1


def build_huffman_tree(aDict):
    """
    This method is used to create the huffman tree using the node class and the the priority queue class.
    :param aDict:
    :return:
    """
    queue1 = pq()
    for key, value in aDict.items():
        queue1.insert_node(node(key, value))
    # print(queue1)
    while (queue1.get_size() > 1):
        left = queue1.extract_min()
        right = queue1.extract_min()
        root = node("NON_CHAR", left.get_value() + right.get_value())
        root.set_left(left)
        root.set_right(right)
        queue1.insert_node(root)
    huffman_root = queue1.extract_min()
    return huffman_root


def create_huffman_code(huffman_root, aString, aDict):
    """
    This method is used to create the huffman tree
    :param huffman_root: the root node that has the huffamn tree
    :param aString: empty string
    :param aDict: dictionary that contains the huffman code and the string.
    :return:
    """
    if huffman_root.get_left() is None and huffman_root.get_right() is None \
            and huffman_root.get_character() is not "NON_CHAR":
        aDict[huffman_root.get_character()] = aString
        return aDict
    create_huffman_code(huffman_root.get_left(), aString + "0", aDict)
    create_huffman_code(huffman_root.get_right(), aString + "1", aDict)


def encode_file(aBook, aDict, option):
    """
    This method is used to used to encode the files using huffman code and then write the file as an encoded file.
    :param aBook: the file name
    :param aDict:the dictionary that contains the huffman codes
    :param option: encode using fixed frequencies or variable frequencies.
    :return:
    """
    with io.open("Books/" + aBook, 'r', encoding='utf8') as file:
        book = file.read()
    if (option == 1):
        file = "encoded_books_normal/" + str(aBook) + "_encoded.txt"
    elif (option == 2):
        file = "encoded_books_fixed_freq/" + str(aBook) + "_encoded.txt"
    binary = ""
    for i in book:
        binary += aDict[i]
    padded_binary = binary + "0" * (len(binary) % 8)  # padding
    count = 0
    byte_size = ""
    bytes1 = bytearray()
    for i in padded_binary:
        if (count % 8 == 0):
            if (count != 0):
                bytes1.append(int(byte_size, 2))
            byte_size = ""
        byte_size += i
        count += 1
    with open(file, 'wb') as pen:
        pen.write(bytes(bytes1))


def decode_file(aBook, dict1, option):
    """
    This method decodes the book using the frequencies obtained, it takes the dictionary that contains the huffman codes
    and then reverses the key value pairs in order to decode them.
    :param aBook: the file name
    :param dict1: the dictionary that contains the characters and their huffman codes
    :param option: to decode the file using fixed frequencies or normal frequencies
    :return:
    """
    book = ""
    if (option == 1):
        with io.open("encoded_books_normal/" + aBook + "_encoded.txt", 'rb') as file:
            book = file.read()
    elif (option == 2):
        with io.open("encoded_books_fixed_freq/" + aBook + "_encoded.txt", 'rb') as file:
            book = file.read()
    dict2 = {}
    for key, value in dict1.items():
        dict2[value] = key
    binary_String = ""
    for i in book:
        binary_num = bin(i)
        binary_num = binary_num[2:].rjust(8, '0')
        binary_String += binary_num
    book_string = ""
    num1 = ""
    for i in binary_String:
        num1 += i
        if (dict2.get(num1)):
            book_string += dict2[num1]
            num1 = ""
    file = ""
    if (option == 1):
        file = "decoded_books_normal/" + str(aBook) + "_decoded.txt"
    elif (option == 2):
        file = "decoded_books_fixed_freq/" + str(aBook) + "_decoded.txt"
    with open(file, 'w', encoding='utf-8') as pen:
        pen.write(book_string)




def fixed_frequency_compression(aBook):
    """
    This method uses fixed frequencies to encode and decode the book.
    :param aBook: file name
    :return: none
    """
    with io.open("Books/" + aBook, 'r', encoding='utf8') as file:
        book = file.read()
    fixed_dict = {" ": 17.1662, "!": 0.0072, "\"": 0.2442, "#": 0.0179, "$": 0.0561,
                  "%": 0.0160, "&": 0.0226, "\'": 0.2447, "(": 0.2178, ")": 0.2233, "*": 0.0628,
                  "+": 0.0215, ",": 0.7384, "-": 1.3734, ".": 1.5124, "/": 0.1549, "0": 0.5516,
                  "1": 0.4594, "2": 0.3322, "3": 0.1847, "4": 0.1348, "5": 0.1663, "6": 0.1153,
                  "7": 0.1030, "8": 0.1054, "9": 0.1024, ":": 0.4354, ";": 0.1214, "<": 0.1225,
                  "=": 0.0227, ">": 0.1242, "?": 0.1474, "@": 0.0073, "A": 0.3132, "B": 0.2163,
                  "C": 0.3906, "D": 0.3151, "E": 0.2673, "F": 0.1416, "G": 0.1876, "H": 0.2321,
                  "I": 0.3211, "J": 0.1726, "K": 0.0687, "L": 0.1884, "M": 0.3529, "N": 0.2085,
                  "O": 0.1842, "P": 0.2614, "Q": 0.0316, "R": 0.2519, "S": 0.4003, "T": 0.3322,
                  "U": 0.0814, "V": 0.0892, "W": 0.2527, "X": 0.0343, "Y": 0.0304, "Z": 0.0076,
                  "[": 0.0086, "\\": 0.0016, "]": 0.0088, "^": 0.0003, "_": 0.1159, "`": 0.0009,
                  "a": 5.1880, "b": 1.0195, "c": 2.1129, "d": 2.5071, "e": 8.5771, "f": 1.3725,
                  "g": 1.5597, "h": 2.7444, "i": 4.9019, "j": 0.0867, "k": 0.6753, "l": 3.1750,
                  "m": 1.6437, "n": 4.9701, "o": 5.7701, "p": 1.5482, "q": 0.0747, "r": 4.2586,
                  "s": 4.3686, "t": 6.3700, "u": 2.0999, "v": 0.8462, "w": 1.3034, "x": 0.1950,
                  "y": 1.1330, "z": 0.0596, "{": 0.0026, "|": 0.0007, "}": 0.0026, "~": 0.0003}
    dict1 = defaultdict(int)
    for i in book:
        if (fixed_dict.get(i) is None):
            dict1[i] += 1
    length_of_book = len(book)
    for key, value in fixed_dict.items():
        dict1[key] = int(value * length_of_book)
    huffman_root = build_huffman_tree(dict1)
    dict2 = {}
    create_huffman_code(huffman_root, "", dict2)
    encode_file(aBook, dict2, 2)
    decode_file(aBook, dict2, 2)


def compare_compression(aBook, time1, time2, run):
    """
    This method compares the various texts to analyze the compression ratios and prints the time taken for each operation.
    Additionally it writes the results to a file called result.txt
    :param aBook: this is the book that is is being compared
    :param time1: the time taken to encode and decode the file normally without fixed frequencies
    :param time2: the time taken to encode and decode the file with fixed frequencies
    :param run: the iteration number
    :return: the dictionary with book name as key and its data as value
    """
    s1 = os.path.getsize("encoded_books_normal/" + aBook + "_encoded.txt")
    s2 = os.path.getsize("Books/" + aBook)
    s3 = os.path.getsize("encoded_books_fixed_freq/" + aBook + "_encoded.txt")
    compression_normal = (s2 / s1)
    compression_fixed = (s2 / s3)
    print("*" * 10, aBook, "*" * 10)
    print("Compression with normal frequencies: ", "%0.3f" % compression_normal, ", time taken = ", "%0.3f" % time1,
          " seconds.")
    print("Compression with fixed frequencies: ", "%0.3f" % compression_fixed, ", time taken = ", "%0.3f" % time2,
          " seconds.")
    file = "results.txt"
    with open("Books/" + aBook, 'r', encoding='utf8') as original:
        book_original = original.read()
    with open("decoded_books_normal/" + aBook + "_decoded.txt", 'r', encoding='utf-8') as normal:
        book_decoded_normal = normal.read()
    with open("decoded_books_fixed_freq/" + aBook + "_decoded.txt", 'r', encoding='utf-8') as fixed:
        book_decoded_fixed = fixed.read()
    difference_normal = set(book_original).difference(book_decoded_normal)
    difference_fixed = set(book_original).difference(book_decoded_fixed)
    diff_fixed = "No difference" if len(difference_fixed) == 0 else str(difference_fixed)
    diff_normal = "No difference" if len(difference_fixed) == 0 else str(difference_normal)
    print("Text different between original book and book encoded and decoded with fixed frequencies: ", diff_fixed)
    print("Text different between original book and book encoded and decoded without fixed frequencies: ",
          diff_normal)

    with open(file, 'a', encoding='utf-8') as pen:
        s1 = "*" * 20 + "Interation number: " + str(run) + "*" * 20 + "\n"
        s2 = "*" * 10 + aBook + "*" * 10 + "\n"
        s3 = "Compression with normal frequencies: " + ("%0.3f" % compression_normal) + ", time taken = " + (
                "%0.3f" % time1) + " seconds.\n"
        s4 = "Compression with fixed frequencies: " + ("%0.3f" % compression_fixed) + ", time taken = " + (
                "%0.3f" % time2) + " seconds.\n"
        pen.write(s1)
        pen.write(s2)
        pen.write(s3)
        pen.write(s4)
        pen.write("Difference between book and normally decoded text\n")
        pen.write(diff_normal+"\n")
        pen.write("Difference between book and text decoded with fixed frequencies\n")
        pen.write(diff_fixed+"\n")

    return {aBook: [compression_normal, time1, compression_fixed, time2]}


def encode_and_decode_books(list_of_books, run):
    """
    This method takes in a list of books and performs the operations to encode, decode, check the difference between the
    two texts and then print the compression ratios and times.
    :param list_of_books: the list of books to the encoded and decoded.
    :param run: the iteration count.
    :return: a dictionary where the key is the name of the book and it's value is a list that contains compression
    ratios and execution time.
    """
    aDict = {}
    for book in list_of_books:
        time1 = time.time() #time stamp
        dict1 = obtain_frequencies(book) #this method retrieves the frequencies of each character in the book.
        huffman_root = build_huffman_tree(dict1) #this method is used to build the huffman tree.
        dict1 = {}
        create_huffman_code(huffman_root, "", dict1) #This method creates the huffman code for each character/
        encode_file(book, dict1, 1) #this method encodes the file according to the huffman code and writes the file.
        decode_file(book, dict1, 1) #this method decodes the encoded file.
        time2 = time.time()
        time3 = time.time()
        fixed_frequency_compression(book) #this method encodes and decodes the file using fixed frequencies.
        time4 = time.time()
        dict1 = compare_compression(book, time2 - time1, time4 - time3, run) #this method compares the text files.
        for key, value in dict1.items():
            aDict[key] = value
    return aDict


def iterate_through_folder(folder):
    list_of_books = []
    for file_name in os.listdir(folder):
        list_of_books.append(file_name)
    return list_of_books

def main():
    """
    This is the main method it iterates through the folder "Books" and does the process of encoding
    or decoding.
    :return: None
    """
    # the method returns all the books present in the folder "Books"
    list_of_books = iterate_through_folder("Books")
    #to change the number of iterations:
    number_of_iterations = 10
    """This dictionary is used to store all the compression ratios and time taken for each operation
    Once the dictionary is complete it's values are divided by the number of iterations to find the
    average runtime and the average compression ratio"""
    dict1 = {}
    for i in range(0, number_of_iterations):
        """the following function returns a dictionary where the key is the name of the book and it's value is a
        list, this contains the compression ratio for fixed frequencies and it's execution time and the compression
        ratio for non-fixed frequencies and it's execution time"""
        aDict = encode_and_decode_books(list_of_books, i)
        if (i != 0):
            for key, value in aDict.items():
                value[0] += value[0] #adding values from previous iterations to the dictionary
                value[1] += value[1]
                value[2] += value[2]
                value[3] += value[3]
                dict1[key] = value
        else:
            dict1 = aDict
    for key, value in dict1.items():
        # dividing each value in the list by the number of iterations to obtain average
        value[0] = value[0] / number_of_iterations
        value[1] = value[1] / number_of_iterations
        value[2] = value[2] / number_of_iterations
        value[3] = value[3] / number_of_iterations
        dict1[key]=value
    print("Average compression and average time taken with ",number_of_iterations," runs:")
    table1 = PrettyTable(['Name of the text','compression ratio (normal frequencies)','Time taken normal (seconds)',
                          'compression ratio (fixed frequencies)','Time taken fixed (seconds)'])
    for key, value in dict1.items():
        table1.add_row([key,"%0.3f" %value[0],"%0.3f" %value[1],"%0.3f" %value[2],"%0.3f" %value[3]])
    print(table1)






if __name__ == '__main__':
    main()
