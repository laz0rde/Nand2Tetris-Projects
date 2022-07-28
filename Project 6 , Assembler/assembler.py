from asyncio.windows_events import NULL
import re

dest_table = {
    "":"000",
    "M":"001",
    "D":"010",
    "DM":"011",
    "MD":"011",
    "A":"100",
    "AM":"101",
    "AD":"110",
    "ADM":"111"
}

comp_table = {
    "0":"0101010",
    "1":"0111111",
    "-1":"0111010",
    "D":"0001100",
    "A":"0110000",
    "!D":"0001101",
    "!A":"0110001",
    "-D":"0001111",
    "-A":"0110011",
    "D+1":"0011111",
    "A+1":"0110111",
    "D-1":"0001110",
    "A-1":"0110010",
    "D+A":"0000010",
    "D-A":"0010011",
    "A-D":"0000111",
    "D&A":"0000000",
    "D|A":"0010101",
    "M":"1110000",
    "!M":"1110001",
    "-M":"1110011",
    "M+1":"1110111",
    "M-1":"1110010",
    "D+M":"1000010",
    "D-M":"1010011",
    "M-D":"1000111",
    "D&M":"1000000",
    "D|M":"1010101"
}

jump_taple = {
    "":"000",
    "JGT":"001",
    "JEQ":"010",
    "JGE":"011",
    "JLT":"100",
    "JNE":"101",
    "JLE":"110",
    "JMP":"111"
}

symbols_table = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD":"24576",
    "SP":"0",
    "LCL":"1",
    "ARG":"2",
    "THIS":"3",
    "THAT":"4",
}

def removeWhiteSpaces():
    file1 = open('./pong/Pong.asm', 'r')
    Lines = file1.readlines()
    Result = ""
    for line in Lines:
        if len(line.strip()) == 0:
            continue

        Result += line
    return Result

def removeComments(Result):
    Result1 = ""

    for line in Result.splitlines():
        indicies = [(m.start(0), m.end(0)) for m in re.finditer(r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)', line)]
        if len(indicies) == 1:
            Result1 += line[0:indicies[0][0]]+'\n'
        else:
            line += '\n'
            Result1 += line
    
    return Result1

def solveSymbols1():
    
    
    Summ = removeComments(removeWhiteSpaces())
    count = -5
    for line in Summ.splitlines():
        
        if '(' in line:
            symbols_table.update({str(line[1:-1].strip()):str(count)})
            count -= 1
        
        count +=1
        # print(line,count)

        # if '@' in line:
        #     if isinstance(line[3:],str):
        #         if line[3:] not in symbols_table:
        #             symbols_table.update( {str(line[3:].strip()):str(n)} )
        #             n+=1
        #         continue

def clearExtras():
    Result=""

    Summ = removeComments(removeWhiteSpaces())
    for line in Summ.splitlines():
        if '(' in line or len(line) ==0:
            continue
        
        line += '\n'
        Result += line.lstrip()
    
    return Result

def solveSymbols2():
    n=15
    fResults = clearExtras()
    for line in fResults.splitlines():
        if '@' in line:
            if type(line[1:]) == str:
                if line[1:].strip() not in symbols_table:
                    symbols_table.update({str(line[1:].strip()):str(n)})
                    n+=1

def translateSymbols():
    Result = ""
    FinalResult = clearExtras()
    for line in FinalResult.splitlines():
        if line.startswith('@'):
            if not line[1:].isnumeric():
                line = '@' + str(symbols_table.get(line[1:],"0"))
                line += '\n'
                Result += line
            else:
                line+='\n'
                Result+=line
        else:
            line+='\n'
            Result+=line
    
    return Result

def resolveInstructions():
    Result=""

    Summ = translateSymbols()
    for line in Summ.splitlines():
        if line.startswith('@'):
            line = '0' + format(int(line[1:]),'015b') + '\n'
            Result += line
        else:
            if "=" in line and ";" not in line:
                eq = line.strip().split('=')
                valDest = dest_table.get(eq[0])
                valComp = comp_table.get(eq[1])
                line = '111' + str(valComp) + str(valDest) + '000' + '\n'
                Result += line
                # print(eq)
            elif ";" in line and "=" not in line:
                eq=line.strip().split(';')
                valComp = comp_table.get(eq[0])
                valJmp = jump_taple.get(eq[1])
                line = '111' + str(valComp) + '000' + str(valJmp) + '\n'
                Result += line

            elif "=" in line and "=" in line:
                eq = line.strip().split('=')
                eqEx = eq[1].split(";")

                valDest = dest_table.get(eq[0])
                valComp = comp_table.get(eqEx[0])
                valJmp = jump_taple.get(eqEx[1])
                line = '111' + str(valComp) + str(valDest) + str(valJmp) + '\n'
                Result += line
                # print(eq)
                

    return Result

solveSymbols1()
solveSymbols2()
# print(resolveInstructions())
f = open("Pong.hack","w")
f.write(resolveInstructions())


# print(symbols_table)
# print (translateSymbols())

# print(resolveInstructions())
# resolveInstructions()
