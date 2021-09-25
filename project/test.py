import json

def get_manual_json(manual):
    try:
        return json.load(open(manual+'.json'))
    except:
        return None

def table( data ):
    file = ''
    man = get_manual_json( data[0] )
    if not man:
        return "Invalid Manual!"
    if len(data)-1:
        args_split = data[1].split('.')
        size = len(args_split)
        if size != 2:
            return "Invalid Section Notation!"
        section=[]
        try:
            section = [int(num) for num in args_split]
        except ValueError:
            return "Invalid Section Notation!"
        if section[1]:
            return specific_item(data['content'][section[0]-1]['subsections'][section[1]-1],data[1])
        return specific_item(data['content'][section[0]-1],data[1])
    else:
        return items(data['content'])
            

def items(section, pre = '', start_tab=''):
    string = ''
    for sn in range(len(section)):
        loc = ''
        if pre:
            pre_split = pre.split('.')
            if int(pre_split[1]):
                loc = pre+"."+str(sn+1)
            else:
                loc = pre_split[0]+'.'+str(sn+1)
        else:
            loc = str(sn+1)+".0"
        string += start_tab + loc + ' ' + section[sn]['title'] + "\n"
        #print(string)
        if has_subsections(section[sn]):
            string += items( section[sn]['subsections'], loc, start_tab+'\t')
    return string

def specific_item(section, pre):
    string = ''
    string += pre + ' ' + section['title'] + "\n"
    if has_subsections(section):
            string += items( section['subsections'], pre, '\t' )
    return string

def has_subsections(section):
    try:
        return len(section['subsections'])
    except KeyError:
        return False

def read(data):
    manual = data[0]
    manual_json = get_manual_json(manual)
    if not manual_json:
        return "Invalid Manual!"
    section_num = data[1]
    num_split = [ int(x) for x in section_num.split('.') ]
    if validate_section( manual, section_num ):
        out = ''
        if len(num_split) == 2:
            if num_split[1]:
                section = manual_json['content'][num_split[0]-1]['subsections'][num_split[1]-1]
                out += '__**'+section['title']+'**__'+"\n\n"
                for line in section['content']:
                    out += line + "\n"
                for sub in section['subsections']:
                    out += "\t" + "__**" + sub['title'] +'**__'+ "\n\n"
                    for line in sub['content']:
                        out += "\t" + line + "\n"
            else:
                section = manual_json['content'][num_split[0]-1]
                out += '__**' + section['title'] + '**__' + "\n\n"
                for line in section['content']:
                    out += line + "\n"
                for sub in section['subsections']:
                    out += "\t" + '__**' + sub['title'] + '**__' + "\n\n"
                    for line in sub['content']:
                        out += "\t" + line + "\n"
                    for subsub in sub['subsections']:
                        out += "\t\t" + '__**' + subsub['title'] + '**__'  + "\n\n"
                        for line in subsub['content']:
                            out += "\t\t" + line + "\n"
        else:
            subsub = manual_json['content'][num_split[0]-1]['subsections'][num_split[1]-1]['subsections'][num_split[2]-1]
            out += '__**' + subsub['title'] + '**__' + "\n\n"
            for line in subsub['content']:
                out += line + "\n"
        return out
    return "Invalid Section!"

def validate_section(manual, section):
    man = get_manual_json(manual)
    try:
        num_split = [ int(x) for x in section.split('.') ]
    except ValueError:
        return False
    size = len(num_split)
    try:
        if size >= 2 and size <= 3:
            if not num_split[1]:
                s = man['content'][num_split[0]-1]
                return size == 2
            s = man['content'][num_split[0]-1]['subsections'][num_split[1]-1]
            if size == 3:
                s2 = s['subsections'][num_split[2]-1]
                return True
            return True
    except Exception as e:
        return False

def help(args):
    with open('project/help.json') as f:
        h = json.load(f)
        out = ''
        if args:
            try:
                section = h[args[0]]
                out += '**'+section['header']+'**'+'\n'
                out += section['syntax']+'\n'
                for line in section['info']:
                    out += line + '\n'
            except:
                out = "Command " + args[0] + " not found!"
        else:
            cmds = list(h.keys()).sort()
            for cmd in cmds:
                out += help([cmd])+'\n'
    return out

def rule( data ):
    if data:
        pass
    else:
        pass

def cmd( data ):
    global active
    args = data[1:].split(' ')
    main_arg = args.pop(0)
    if main_arg == "table":
        return table(args)
    elif main_arg == "read":
        return read(args)
    elif main_arg == "help":
        return help(args)
    elif main_arg == "exit":
        active = False
        return 'Exiting...'
    return "Invalid Command!"
#print("Final:", table('gm2'), sep='\n')
active = True
while active:
    i = input("> ")
    print(">",i)
    print(cmd(i))
#print("Final:", table('gm1 3.0'), sep='\n')
