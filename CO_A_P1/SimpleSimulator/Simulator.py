import sys

reg_dic = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "FLAGS": {"V":0, "L":0, "G":0, "E":0}}  # this is dictionary of valid register names with the data they contain.
reg_adrs_dic = {"000":"R0", "001":"R1", "010":"R2", "011":"R3", "100":"R4", "101":"R5", "110":"R6", "111":"FLAGS"}
opcode_list = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]

b_opcd = {"00000":"add", "00001":"sub","00010":"mov_b", "00011":"mov_c",

          "00100":"ld", "00101":"st", "00110":"mul", "00111":"div",

          "01000": "rs", "01001":"ls" , "01010":"xor", "01011":"or",

          "01100":"and", "01101":"not", "01110":"cmp", "01111":"jmp",

          "11100":"jlt", "11101":"jgt", "11111":"je", "11010":"hlt", "10000":"addf", "10001":"subf", "10010":"movf", "10110":"inc", "10111":"dec", "10011":"lea", "10100":"ldr", "10101":"strr"}

#setting MEM to all 0s
MEM = ["0"*16 for i in range(128)]

#Loading Memory from stdin
line_list = sys.stdin.readlines()
for i in range(len(line_list)):
    MEM[i] = line_list[i].strip()

PC = 0
halted = False
#Funcitons****************************************************
#return the the opcode name and type from a binary string s
def opcode_is(s):
    op_code = s[:5]
    for i in b_opcd.keys():
        if i==op_code:
            return(b_opcd[i])

#pulls all the operands from an instruction and returns it in a list
def pull_operands(s):
    op_code = s[:5]
    A = ["00000", "00001", "00110", "01010", "01011", "01100", "10000", "10001"]
    B = ["00010", "01000", "01001"]
    B_new = ["10010"]
    C = ["00011", "00111", "01101", "01110", "10100", "10101"]
    D = ["00100", "00101", "10011"]
    E = ["01111", "11100", "11101", "11111"]
    G = ["10110", "10111"]
    l = []
    # 0000000000000000
    if op_code in A:
        l.append(s[7:10])
        l.append(s[10:13])
        l.append(s[13:16])
    elif op_code in B:
        l.append(s[6:9])
        l.append(s[9:16])
    elif op_code in B_new:
        l.append(s[5:8])
        l.append(s[8:16])
    elif op_code in C:
        l.append(s[10:13])
        l.append(s[13:16])
    elif op_code in D:
        l.append(s[6:9])
        l.append(s[9:16])
    elif op_code in E:
        l.append(s[9:16])
    elif op_code in G:
        l.append(s[6:9])

    elif op_code == "11010":
        l = []
    return l


def intbin(n, x):
    s = format(n, f"0{x}b")
    return s
def binary_to_int(binary_string):
    decimal_value = int(binary_string, 2)
    return decimal_value
