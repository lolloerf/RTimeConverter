import time, base64, os

# twisty: penatlty 1 is +2, penalty 2 is dnf
# ruwix: fourth row is +2, fifth is dnf

def main():
    print('-' * 80)
    print('*' * 18 + 'Convert Ruwix.com to Twisty Timer Save Files'+ '*' * 18)
    print('*' * 18 + 'Convert Twisty Timer to Ruwix.com Save Files'+ '*' * 18)
    print('-' * 80)

    while True:
        input_path = str(os.path.dirname(os.path.realpath(__file__))) + '\\' + input('Enter input file name>>> ')

        try:
            input_file = open(input_path,'r')
            print('Interpreting file...')
            lines = input_file.readlines()
            if lines[0][0] == '"':
                print('Format recognized. \nConverting...')
                o_lines = twisty(lines)
                print('Converted.')
            else:
                print('Format not recognized. \nConverting...')
                o_lines = ruwix(lines[0])
                print('Converted.')
            break
        
        except IOError:
            print('File couldnt be read. Try again.')
            print('----------------------------')
            print('')
        except:
            print('Format not readable. Try again.')
            print('----------------------------')
            print('')


def ruwix(input_str):


    c_time = int(time.time() *1000)
    lines = base64.b64decode(input_str.encode()).decode().split('\n')
    if len(lines) != 6:
        raise Exception()
    lines = lines[:2] + lines[3:]
    info = {'times' : [], 'scrambles' : [], 'penalties' :[], 'dnfs':[], 'comments':[] }
    for i in range(len(lines)):
        read = ''
        for j in range(lines[i].find(',') +1, len(lines[i])):
            char = lines[i][j]
            if char == ',' or char == ']':
                info[list(info)[i]].append(read)
                read = ''
            else:
                read += char
    
    output_lines  = ['Puzzle,Category,Time(millis),Date(millis),Scramble,Penalty,Comment\n']
    for i in range(0,len(info['times'])):
        output_lines.append('"333";"Normal";"'+str(info['times'][i])+'":"' + str(c_time) +'";'+info['scrambles'][i][:-2] + info['scrambles'][i][-1] + ';"' +('2' if info['dnfs'][i]=='1' else info['penalties'][i])+ '";' +info['comments'][i] +'\n')
    with open(str(os.path.dirname(os.path.realpath(__file__))) + '\\converted_solves.txt', 'w') as f:
        for l in output_lines:
            f.write(l)

if __name__ == "__main__":
    main()