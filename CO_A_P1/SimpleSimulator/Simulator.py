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

def flt_dec(n):
    n = n & 255
    s = intbin(n, 8);
    mantissa = s[3:]
    # print(mantissa)
    mantissa = 32 + binary_to_int(mantissa)
    exp = binary_to_int(s[:3]) - 3 - 5
    num = mantissa * (2 ** exp)
    # print(mantissa, exp)
    return num


def dec_flt(n):
    exp = 3
    while n >= 2:
        n = n / 2
        exp += 1
    while n < 1:
        n = n * 2
        exp = exp - 1
    afp = n - int(n)
    # print(afp)
    m = ''
    for i in range(5):
        afp = afp * 2
        bfp = afp - (afp - int(afp))
        afp = afp - bfp
        m = m + str(int(bfp))
        # print(bfp)
        bfp = 0
    # print(intbin(exp, 3), m)
    return str(intbin(exp, 3)) + m


def reset_flag():
    for i in reg_dic["FLAGS"]:
        reg_dic["FLAGS"][i]=0
def PC_update(i):
    global PC
    PC = i
#prints the value of PC as 7 bit binary
def PC_dump():
    print(intbin(PC, 7), end = "        ")

#prints the values of all register in a single line
def RF_dump():
    for i in reg_dic:
        if (i=="FLAGS"):
            print("000000000000" + str(reg_dic[i]["V"]) + str(reg_dic[i]["L"]) + str(reg_dic[i]["G"]) + str(reg_dic[i]["E"]) )
            break
        print(intbin(reg_dic[i], 16), end = " ")


#rreturn the value store in register R
def get_RF(R):
    return reg_dic[R]

#returns the instuction stored in MEM[PC]
def MEM_fetchDate(PC):
    return MEM[PC];

#prints all the 128 lines of the memeory
def MEM_dump():
    cnt=0
    for l in MEM:
        # if cnt==10:
        #     break
        print(l)
        cnt+=1


#single instn executin funs (the parameters are register names or decimal values)

def inc(l):
    r1 = l[0]
    sum = reg_dic[r1] + 1
    if (sum > 65535):
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        reg_dic[r1] = sum
        reset_flag()
    return False, PC+1

def dec(l):
    r1 = l[0]
    val = reg_dic[r1] - 1
    if val < 0:
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        reg_dic[r1] = val
        reset_flag()
    return False, PC+1

def lea(l):
    # print("st")
    r1, mem_adrs = l
    reg_dic[r1] = mem_adrs
    reset_flag()
    return False, PC+1
def strr(l):
    r1, r2 = l
    MEM[reg_dic[r2]] = intbin(reg_dic[r1], 16)
    reset_flag()
    return False, PC+1
def ldr(l):
    r1, r2 = l
    data = MEM[reg_dic[r2]]
    data = binary_to_int(data)
    reg_dic[r1] = data
    reset_flag()
    return False, PC+1
def add(l):
    # print("add")
    r1, r2, r3 = l
    sum = reg_dic[r2] + reg_dic[r3]
    # print(sum)
    if (sum > 65535):
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        reg_dic[r1] = sum
        reset_flag()
    return False, PC+1

def addf(l):
    # print("addf")
    r1, r2, r3 = l
    f2 = reg_dic[r2] & 255
    f3 = reg_dic[r3] & 255
    f2 = flt_dec(f2)
    f3 = flt_dec(f3)
    f1 = f2 + f3
    if (f1 > 31.5):
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        f1 = dec_flt(f1)
        f1 = binary_to_int(f1)
        reg_dic[r1] = f1
        reset_flag()
    return False, PC + 1


def subf(l):
    # print("subf")
    r1, r2, r3 = l
    f2 = reg_dic[r2] & 255
    f3 = reg_dic[r3] & 255
    f2 = flt_dec(f2)
    f3 = flt_dec(f3)
    f1 = f2 - f3
    print(f1, f2, f3)
    if (f1 < 0):
        # print("overflow")
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        f1 = dec_flt(f1)
        f1 = binary_to_int(f1)
        reg_dic[r1] = f1
        reset_flag()
    return False, PC + 1


def movf(l):
    # print("movf")
    r1, imm = l

    reg_dic[r1] = imm
    return False, PC + 1

def sub(l):
    # print("sub")
    r1, r2, r3 = l
    if (reg_dic[r3]>reg_dic[r2]):
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        dif = reg_dic[r2] - reg_dic[r3]
        reg_dic[r1] = dif
        reset_flag()
    return False, PC+1


def mov_b(l):
    # print("mov_b")
    # print("hi", l)
    r1, imm = l
    reg_dic[r1]=imm;
    reset_flag()
    return False, PC+1


def mov_c(l):
    # print("mov_c")
    r1, r2 = l
    if r2 == "FLAGS":
        bin = str(reg_dic[r2]["V"]) + str(reg_dic[r2]["L"]) + str(reg_dic[r2]["G"]) + str(reg_dic[r2]["E"])
        val = binary_to_int(bin)
    else:
        val = reg_dic[r2]
    reg_dic[r1] = val
    reset_flag()
    return False, PC+1


def ld(l):
    # print("ld")
    r1, mem_adrs = l
    data = MEM[mem_adrs]
    data = binary_to_int(data)
    reg_dic[r1] = data
    reset_flag()
    return False, PC+1


def st(l):
    # print("st")
    r1, mem_adrs = l
    MEM[mem_adrs] = intbin(reg_dic[r1], 16)
    reset_flag()
    return False, PC+1


def mul(l):
    # print("mul")
    r1, r2, r3 = l
    prod = reg_dic[r2] * reg_dic[r3]
    if prod > 65535:
        reg_dic["FLAGS"]["V"] = 1
        reg_dic[r1] = 0
    else:
        reg_dic[r1] = prod
        reset_flag()
    return False, PC+1


def div(l):
    # print("div")
    r3, r4 = l
    if reg_dic[r4] == 0:
        reg_dic["FLAGS"]["V"] = 1
        reg_dic["R0"] = 0
        reg_dic["R1"] = 0
    else:
        q = reg_dic[r3]//reg_dic[r4]
        r = reg_dic[r3]%reg_adrs_dic[r4]
        reg_dic["R0"] = q
        reg_dic["R1"] = r
        reset_flag()
    return False, PC+1


