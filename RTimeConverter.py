import time, base64, os

# twisty: penatlty 1 is +2, penalty 2 is dnf
# ruwix: fourth row is +2, fifth is dnf

#info:
#times: millis
#scrambles: string, no space at the end
#dnfs, penalties: 1/0
#comments: string

def main():
    #make a banner
    print('-' * 80)
    print('*' * 36 + '3X3 ONLY' + '*' * 36)
    print('*' * 24 + 'Convert different timer formats!'+ '*' * 24)
    print('*' * 36 + '3X3 ONLY' + '*' * 36)
    print('-' * 80)

    #get file and start converting
    #file has to be in same dir as script
    current_path = str(os.path.dirname(os.path.realpath(__file__))) + '\\'

    while True:
        user_input = input('Enter input file path/name>>> ')
        if len(user_input)> 1:
            if user_input[0] == '/' or user_input[1] == ':':
                input_path = user_input
        input_path = current_path+ user_input

        try:
            print('Reading file...')
            input_file = open(input_path,'r')
            lines = input_file.readlines()
            break

        except IOError:
            print('File couldnt be read. Try again.')
            print('----------------------------')
            print('')

    while True:
        print('What should the file be interpreted as?')
        print('Ruwix.com:                   r/ruwix/ruwix.com')
        print('Twisty Timer:                t/twisty/twisty timer')
        print('(Case irrelevant)')
        action = input('>>> ').lower()

        if action == 'r' or action == 'ruwix' or action == 'ruwix.com':
            try:
                print('Interpreting as Ruwix.com data...')
                info = read_ruwix(lines[0])
                print('Data has successfully been read.')
                break
            except :
                print('Format not recognized. Try again.')
                print('----------------------------')
                print('')
        elif action == 't' or action == 'twisty' or action == 'twisty timer':
            try:
                print('Interpreting as Twisty Timer data...')
                info = read_twisty(lines)
                print('Data has successfully been read.')
                break
            except :
                print('Format not recognized. Try again.')
                print('----------------------------')
                print('')
        else:
            print('Not a valid format. Try again.')
            print('----------------------------')
            print('')

    while True:
        print('What should the file be converted to?')
        print('Ruwix.com:                   r/ruwix/ruwix.com')
        print('Twisty Timer:                t/twisty/twisty timer')
        print('(Case irrelevant)')
        action = input('>>> ').lower()

        if action == 'r' or action == 'ruwix' or action == 'ruwix.com':
            print('Converting to Ruwix.com data...')
            write_ruwix(info)
            print('Data has successfully been converted.')
            break
        elif action == 't' or action == 'twisty' or action == 'twisty timer':
            print('Converting to Twisty Timer data...')
            write_twisty(info)
            print('Data has successfully been converted.')
            break
        else:
            print('Not a valid format. Try again.')
            print('----------------------------')
            print('')

        print('Yay we done')
        print('Press enter to exit')
        input('')

def read_ruwix(line):

    #set all requirements for the Twisty Timer backup format
    c_date = int(time.time() *1000)
    lines = base64.b64decode(line.encode()).decode().split('\n')
    if len(lines) != 6:
        raise Exception()
    lines = lines[:2] + lines[3:]
    info = {'times' : [], 'scrambles' : [], 'penalties' :[], 'dnfs':[], 'comments':[],'dates':[]}
    for i in range(len(lines)):
        read = ''
        for j in range(lines[i].find(',') +1, len(lines[i])):
            char = lines[i][j]
            if char == ',' or char == ']':
                info[list(info)[i]].append(read[:-1] if i == 1 and read[-1] == ' ' else read)
                read = ''
            elif char == '"':
                pass
            else:
                read += char


    for i in range(len(info['times'])):
        info['dates'].append(str(c_date))

    return info

def write_ruwix(info):

    output_lines = ''

    for i in range(len(info)):
        if i == 5:
            pass
        else:
            line = '['
            if i < 2:
                line += '-1'
            elif i == 4:
                line += '""'
            else:
                line += '0'
            for o in info[list(info)[i]]:
                line += ','
                if i == 1 or i == 4:
                    line += '"' + o +'"'
                else:
                    line += o
            line += ']'

            if i != 4:
                line += '\n'

            output_lines += line

            if i == 1:
                output_lines += ('[-1' + ',2'*len(info['times']) + ']\n')
    
    output_lines = base64.b64encode(output_lines.encode()).decode()

    with open(str(os.path.dirname(os.path.realpath(__file__))) + '\\converted_solves.txt', 'w') as f:
        f.write(output_lines)

        


        

def read_twisty(lines):
    lines = lines[1:]

    info = {'times' : [], 'scrambles' : [], 'penalties' :[], 'dnfs':[], 'comments':[],'dates':[]}
    order = ['times','dates','scrambles','penalties','comments']

    for l in lines:
        count = 0
        read = ''
        i = 16
        while i < len(l):
            char = l[i]
            if char == '"':
                if count == 3:
                    if read == '2':
                        info['dnfs'].append('1')
                        info['penalties'].append('0')
                    elif read == '1':
                        info['dnfs'].append('0')
                        info['penalties'].append('1')
                    else:
                        info['dnfs'].append('0')
                        info['penalties'].append('0')
                    i += 2
                    count += 1
                elif count == 4:
                    info[order[count]].append(read)
                    break
                else:
                    info[order[count]].append(read)
                    i += 2    
                    count += 1
                read = ''
                
            else:
                read += char
            i+=1
    return info




def write_twisty(info):

    output_lines  = ['Puzzle,Category,Time(millis),Date(millis),Scramble,Penalty,Comment\n']
    for i in range(0,len(info['times'])):
        output_lines.append('"333";"Normal";"'+info['times'][i]+'";"' + info['dates'][i] +'";"'+info['scrambles'][i]+ '";"' +('2' if info['dnfs'][i]=='1' else info['penalties'][i] ) + '";"' +info['comments'][i] +'"\n')
    with open(str(os.path.dirname(os.path.realpath(__file__))) + '\\converted_solves.txt', 'w') as f:
        for l in output_lines:
            f.write(l)

if __name__ == "__main__":
    main()
