import byte_code_parser as myParser
import pprint as pp
import io

file_path_='./Main.class'

myClass=myParser.parse_class_file(file_path=file_path_)
const_pool=myClass['constant_pool']

main=myParser.find_method_by_name(myClass,b'main')

# pp.pprint(main)

attr= [ attr
        for i in main
            for attr in i['attributes'] ]


attrss=myParser.find_attributes_by_name(myClass,attr,b'Code')

for attr in attrss:
    byte_arr=myParser.parse_code_attributes_from_byte_code(attr['info'])
    instructions=myParser.parse_byte_code_from_attribute(myClass,byte_arr['code'])
    for instruct in instructions:
        
        print(instruct['opcode'],end=' ')
        try :
            for operand in instruct['operand']:
                print(operand,end=" ")
        except:
            pass        
        print()    
