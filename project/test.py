import json

def get_manual_json(manual):
    try:
        return json.load(open('project/'+manual+'.json'))
    except:
        return None

def table( input ):
    file = ''
    args = input.split(' ')
    if args[0] == 'gm1':
        file = open('project/gm1.json')
    elif args[0] == 'gm2':
        file = open('project/gm2.json')
    else:
        return "Invalid Manual!"
    data = json.load(file)
    if len(args)-1:
        args_split = args[1].split('.')
        size = len(args_split)
        if size != 2:
            return "Invalid Section Notation!"
        section=[]
        try:
            section = [int(num) for num in args_split]
        except ValueError:
            return "Invalid Section Notation!"
        if section[1]:
            return specific_item(data['content'][section[0]-1]['subsections'][section[1]-1],args[1])
        return specific_item(data['content'][section[0]-1],args[1])
    else:
        return items(data['content'])
            

def items(section, pre = ''):
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
        string += loc + " " + section[sn]['title'] + "\n"
        #print(string)
        if has_subsections(section[sn]):
            string += items( section[sn]['subsections'], loc )
    return string

def specific_item(section, pre):
    string = ''
    string += pre + " " + section['title'] + "\n"
    if has_subsections(section):
            string += items( section['subsections'], pre )
    return string

def has_subsections(section):
    try:
        return len(section['subsections'])
    except KeyError:
        return False

def read(data):
    args_split = data.split(' ')
    manual = args_split[0]
    manual_json = get_manual_json(manual)
    if not manual_json:
        return "Invalid Manual!"
    section_num = args_split[1]
    num_split = [ int(x) for x in section_num.split('.') ]
    if validate_section( manual, section_num ):
        out = ''
        if len(num_split) == 2:
            if num_split[1]:
                section = manual_json['content'][num_split[0]-1]['subsections'][num_split[1]-1]
                out += section['title']+"\n\n"
                for line in section['content']:
                    out += line + "\n"
                for sub in section['subsections']:
                    out += "\t" + sub['title'] + "\n\n"
                    for line in sub['content']:
                        out += "\t" + line + "\n"
            else:
                out += manual_json['content'][num_split[0]-1]['title']+"\n\n"
                for line in manual_json['content'][num_split[0]-1]['content']:
                    out += line + "\n"
                for sub in manual_json['content'][num_split[0]-1]['subsections']:
                    out += "\t" + sub['title'] + "\n\n"
                    for line in sub['content']:
                        out += "\t" + line + "\n"
                    for subsub in sub['subsections']:
                        out += "\t\t" + subsub['title'] + "\n\n"
                        for line in subsub['content']:
                            out += "\t\t" + line + "\n"
        else:
            subsub = manual_json['content'][num_split[0]-1]['subsections'][num_split[1]-1]['subsections'][num_split[2]-1]
            out += subsub['title'] + "\n\n"
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

def cmd( data ):
    args = data[1:].split(' ')
    main_arg = args.pop(0)
    if len(args) == 2:
        datas = args[0] + " " + args[1]
    else:
        datas = args[0]
    if main_arg == "table":
        return table(datas)
    elif main_arg == "read":
        return read(datas)
    return "Invalid Command!"
#print("Final:", table('gm2'), sep='\n')
while True:
    print(cmd(input()))
#print("Final:", table('gm1 3.0'), sep='\n')