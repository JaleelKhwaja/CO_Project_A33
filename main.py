fl = "assembly_code1.txt"  # assembly code file name
file = open(fl, "r")
line_list = file.readlines()
file.close()

reg_dic = {"R0": 0, "R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0,"FLAGS": ['0', '0', '0', '0']}  # this is dictionary of valid register names with the data they contain.
opcode_list = ["add", "sub", "mov", "ld", "st", "mul", "div", "rs", "ls", "xor", "or", "and", "not", "cmp", "jmp", "jlt", "jgt", "je", "hlt"]
reg_list = ["R0", "R1", "R2", "R3", "R4", "R5", "R6"]

typA = ["add", "sub", "mul", "xor", "or", "and"]
typB = ["mov", "rs", "ls"]
typC = ["mov", "div", "not", "cmp"]
typD = ["ld", "st"]
typE = ["jmp", "jlt", "jgt", "je"]
typF = ["hlt"]
gn_err = ": General Syntax Error"

instn_lst = []  # list of all intstructions mostly won't be needed
var_dic = {}  # { name:{adrs:int, data:int}, ...} dictionary of variables
label_dic = {}  # {name:adrs, ...} dictionary of labels

# converts an integer(n) to binary with x bits
def intbin(n, x):
    s = format(n, f"0{x}b")
    return s

# converts register name to its address.
def reg_adr(s):
    if (s == "FLAGS"):
        return "111"
    n = int(s[1])
    return intbin(n, 3)

# converts flag to binary/mostly won't be needed
def flag_to_binary():
    return "000000000000" + "".join(reg_dic["FLAGS"])

def is_valid_var_instn(s):

    if len(s.split()) != 2 or s.split()[0] != "var" or s.split()[1] in var_dic:

        return False

    return True

#*************************************************
# ERROR CHECKER FUNCTIONS
def check_typA(instrn, ln_nmber):
    list = instrn.split()

    if len(list) != 4:
        print("line", ln_nmber, "General Syntax Error")
        return False
    if "FLAGS" in list[1:]:
        print("line", ln_nmber, ": Illegal use of FLAGS register!")
        return False
    for i in range(1, 4):
        if list[i] not in reg_list:
            print("line", ln_nmber, "Typos in Register name")
            return False

    return True
