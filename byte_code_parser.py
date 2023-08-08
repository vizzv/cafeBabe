import pprint as pp
import io
def u4(f):
    return f.read(4)
def u2(f):
    return f.read(2)
def u1(f):
    return f.read(1)
def u_n(f,n):
    return f.read(n)


def byte_to_int(b):
    return int.from_bytes(b,'big')

CONSTANT_Utf8	=1
CONSTANT_Integer=3
CONSTANT_Float	=4
CONSTANT_Long	=5
CONSTANT_Double	=6
CONSTANT_Class	=7
CONSTANT_String	=8
CONSTANT_Fieldref=9
CONSTANT_Methodref=10
CONSTANT_InterfaceMethodref=11
CONSTANT_NameAndType=12
CONSTANT_MethodHandle=15
CONSTANT_MethodType	=16
CONSTANT_InvokeDynamic	=18

access_flags_class=[
    ("ACC_PUBLIC",0x0001),	
    ("ACC_FINAL",0x0010),	
    ("ACC_SUPER",0x0020),	
    ("ACC_INTERFACE",0x0200),
    ("ACC_ABSTRACT",0x0400),
    ("ACC_SYNTHETIC",0x1000),
    ("ACC_ANNOTATION",0x2000),
    ("ACC_ENUM",0x4000)]

access_flags_feilds=[
   ("ACC_PUBLIC",0x0001),	
   ("ACC_PRIVATE",0x0002),
   ("ACC_PROTECTED",0x0004),	
   ("ACC_STATIC",0x0008),	
   ("ACC_FINAL",0x0010),	
   ("ACC_VOLATILE",0x0040),	
   ("ACC_TRANSIENT",0x0080),	
   ("ACC_SYNTHETIC",0x1000),	
   ("ACC_ENUM",0x4000)	
]

access_flags_methods=[
    ("ACC_PUBLIC",0x0001),	
    ("ACC_PRIVATE",0x0002),	
    ("ACC_PROTECTED",0x0004),
    ("ACC_STATIC",0x0008),	
    ("ACC_FINAL",0x0010),
    ("ACC_SYNCHRONIZED",0x0020),	
    ("ACC_BRIDGE",0x0040),
    ("ACC_VARARGS",0x0080),	
    ("ACC_NATIVE",0x0100),
    ("ACC_ABSTRACT",0x0400),	
    ("ACC_STRICT",0x0800),
    ("ACC_SYNTHETIC",0x1000),	
]
def parse_access_flag_class(flags:int):
    return[name for(name,value) in access_flags_class if (flags&value)!=0]

def parse_access_flag_feilds(flags:int):
    return[name for(name,value) in access_flags_feilds if (flags&value)!=0]

def parse_access_flag_methods(flags:int):
    return[name for(name,value) in access_flags_methods if (flags&value)!=0]




def parse_class_file(file_path):
    clazz={}
    with open(file_path, mode='rb') as file: # b is important -> binary
        
        clazz['magic'] = hex(byte_to_int(u4(file)))
        clazz['minor']=byte_to_int(u2(file))
        clazz['major']=byte_to_int(u2(file))
        pool_count=byte_to_int(u2(file))

        constant_pool=[]
    

        for i in range(pool_count-1):
            cp_info={}
            tag=byte_to_int(u1(file))
            if(tag== CONSTANT_Methodref):
                cp_info['class_index']=byte_to_int(u2(file))
                cp_info['name_type_index']=byte_to_int(u2(file))
                cp_info['tag']="CONSTANT_Methodref"
            
            elif(tag== CONSTANT_Class):
                cp_info['name_index']=byte_to_int(u2(file))
                cp_info['tag']="CONSTANT_Class" 
            elif(tag== CONSTANT_NameAndType):
                cp_info['name_index']=byte_to_int(u2(file))
                cp_info['discriptor_index']=byte_to_int(u2(file))      
                cp_info['tag']="CONSTANT_NameAndType" 
            
            elif(tag== CONSTANT_Utf8):
                cp_info['tag']="CONSTANT_Utf8"
                length=byte_to_int(u2(file))
                cp_info['length']=length
                cp_info['bytes']=u_n(file,length) 
            elif(tag==CONSTANT_Fieldref):
                cp_info['tag']="CONSTANT_Fieldref"
                cp_info['class_index']=byte_to_int(u2(file))
                cp_info['name_type_index']=byte_to_int(u2(file))
            elif(tag==CONSTANT_String):
                cp_info['tag']="CONSTANT_String"
                cp_info['string_index']=byte_to_int(u2(file))
            elif(tag==CONSTANT_Integer):
                cp_info['tag']="CONSTANT_Integer"
                cp_info['bytes']=u4(file)
            elif(tag==CONSTANT_Float):
                cp_info['tag']="CONSTANT_Float"
                cp_info['bytes']=u4(file) 
            elif(tag==CONSTANT_Long):
                cp_info['tag']="CONSTANT_Long"
                cp_info['high_bytes']=u4(file)
                cp_info['low_bytes']=u4(file)
            elif(tag==CONSTANT_Double):
                cp_info['tag']="CONSTANT_Double"
                cp_info['high_bytes']=u4(file)
                cp_info['low_bytes']=u4(file)

            elif(tag==CONSTANT_InterfaceMethodref):
                cp_info['tag']="CONSTANT_InterfaceMethodref"
                cp_info['class_index']=byte_to_int(u2(file))
                cp_info['name_and_type_index']=byte_to_int(u2(file))

            elif(tag==CONSTANT_MethodHandle):
                cp_info['tag']="CONSTANT_MethodHandle"
                cp_info['reference_kind']=u1(file)
                cp_info['reference_index']=byte_to_int(u2(file))

            elif(tag==CONSTANT_MethodType):
                cp_info['tag']="CONSTANT_MethodType"
                cp_info['discriptor_index']=byte_to_int(u2(file))
                
            elif(tag==CONSTANT_InvokeDynamic):
                cp_info['tag']="CONSTANT_InvokeDynamic"
                cp_info['bootstrap_method_attr_index']=byte_to_int(u2(file))
                cp_info['name_and_type_index']=byte_to_int(u2(file))
            else:
                print(tag)
                print("xx_xx")
                assert False,f"invalid tag:{tag}"  

            constant_pool.append(cp_info)
            
            
        #print("constant pool is = ",end="")
        #pp.pprint(constant_pool)
        clazz['constant_pool']=constant_pool 

        clazz['access_flags']=parse_access_flag_class(byte_to_int(u2(file)))

        clazz['this_class']=byte_to_int(u2(file))

        clazz['super_class']=byte_to_int(u2(file))

        interface_count=byte_to_int(u2(file))

        clazz['interfaces_count']=interface_count
        interfaces=[]
        
        for i in range(interface_count):
            a=byte_to_int(u2(file))+1
            interfaces.append(a)
        clazz['interfaces']=interfaces    
        
        fields_count=byte_to_int(u2(file))
        clazz['fields_count']=fields_count
        
        feilds=[]
        for j in range(fields_count):
            feild_info={}
            feild_info['access_flages']=parse_access_flag_feilds(byte_to_int(u2(file)))
            feild_info['name_index']=byte_to_int(u2(file))
            #pp.pprint(feild_info['name_index'])
            #pp.pprint(clazz['constant_pool'][feild_info['name_index']]['bytes'])
            
            feild_info['descriptor_index']=byte_to_int(u2(file))
            attributes_count=byte_to_int(u2(file))
            feild_info['attributes_count']=attributes_count
            attributes=[]
            for k in range(attributes_count):
                attribute_info={}
                attribute_info['attribute_name_index']=byte_to_int(u2(file))
                attr_length=byte_to_int(u4(file))
                attribute_info['attribute_length']=attr_length
                attribute_info['info']=u_n(file,attr_length)
                attributes.append(attribute_info)
            feild_info['attributes_info']=attributes
            feilds.append(feild_info)
        clazz['feilds']=feilds

        methods_count=byte_to_int(u2(file))
        clazz['methods_count']=methods_count

        methods=[]
        
        for j in range(methods_count):
            method_info={}
            method_info['access_flages']=parse_access_flag_methods(byte_to_int(u2(file)))
            method_info['name_index']=byte_to_int(u2(file))
            #pp.pprint(method_info['name_index'])
            #pp.pprint(clazz['constant_pool'][method_info['name_index']]['bytes'])
            
            method_info['descriptor_index']=byte_to_int(u2(file))
            
            attributes=[]
            attributes_count=byte_to_int(u2(file))
            for j in range(attributes_count):
                attribute={}
                attribute['attribute_name_index']=byte_to_int(u2(file))
                attribute_length=byte_to_int(u4(file))
                attribute['info']=u_n(file,attribute_length)
                attributes.append(attribute)
            method_info['attributes']=attributes
            methods.append(method_info)
        clazz['methods']=methods       
        
        attributes_count=byte_to_int(u2(file))
        attributes=[]
        for j in range(attributes_count):
            attribute_info={}
            attribute_info['attribute_name_index']=byte_to_int(u2(file))
            attribute_length=byte_to_int(u4(file))
            attribute_info['attribute_length']=attribute_length
            attribute_info['info']=u_n(file,attribute_length)
            attributes.append(attribute_info)

        clazz['attributes']=attributes    
    return clazz

def find_method_by_name(clazz,name:bytes):
    return [ method 
            for method in clazz['methods']
                if clazz['constant_pool'][method['name_index']-1]['bytes']==name ]

def find_attributes_by_name(clazz,attributes,name:bytes):
    return [attr
    for attr in attributes 
    if clazz['constant_pool'][attr['attribute_name_index']-1]['bytes'] == name]            

def get_bytes_from_index(clazz,index:int):
    if ((index<=0) or (index>len(clazz['constant_pool'])) ):
        return 0
    myelement=clazz['constant_pool'][index -1]
    if(myelement['tag'] == 'CONSTANT_Fieldref'):
        return get_bytes_from_index(clazz,myelement['class_index'])
    elif(myelement['tag']=='CONSTANT_Methodref'):
        return get_bytes_from_index(clazz,myelement['class_index'])
    elif(myelement['tag']=='CONSTANT_Class'):
        return get_bytes_from_index(clazz,myelement['name_index'])
    elif(myelement['tag']=='CONSTANT_NameAndType'):
        return get_bytes_from_index(clazz,myelement['name_index'])
    elif(myelement['tag']=='CONSTANT_String'):
        return get_bytes_from_index(clazz,myelement['string_index'])
    elif(myelement['tag']=='CONSTANT_InvokeDynamic'):
        return get_bytes_from_index(clazz,myelement['bootstrap_method_attr_index'])
    elif(myelement['tag']=='CONSTANT_Utf8'):
        return myelement['bytes'].decode("utf_8")
    
    else:
        print(f"{myelement} is not implemented in get_bytes_from_index")
        return "highOnMaal"
        
    
def parse_code_attributes_from_byte_code(myByte:bytes):
    code_attribute={}
    with io.BytesIO(myByte)  as f:
        
        code_attribute['max_stack']=byte_to_int(u2(f))
        code_attribute['max_locals']=byte_to_int(u2(f))
        code_length=byte_to_int(u4(f))
        code_attribute['code_length']=code_length
        code=[]
        for index in range(code_length):
            code.append(u1(f))
        code_attribute['code']=code
        exception_table_length=byte_to_int(u2(f))
        code_attribute['exception_table_length']=exception_table_length
        exception_table=[]
        for index in range(exception_table_length):
            exception={}
            exception['start_pc']=byte_to_int(u2(f))
            exception['end_pc']=byte_to_int(u2(f))
            exception['handler_pc']=byte_to_int(u2(f))
            exception['catch_type']=u2(f)
            exception_table.append(exception)
        code_attribute['exception_table']=exception_table

        attributes_count=byte_to_int(u2(f))
        code_attribute['attributes_count']=attributes_count
        attributes=[]
        for j in range(attributes_count):
            attribute_info={}
            attribute_info['attribute_name_index']=byte_to_int(u2(f))
            attribute_length=byte_to_int(u4(f))
            attribute_info['attribute_length']=attribute_length
            attribute_info['info']=u_n(f,attribute_length)
            attributes.append(attribute_info)

        code_attribute['attributes']=attributes
    return code_attribute

def parse_byte_code_from_attribute(clazz,bytess:bytearray):
    
    index=0
    instructions=[]
    
    while(index<len(bytess)):
        instruction={}
        operand=[]
        if(bytess[index]==b'\xb2'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="getstatic"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand
        elif(bytess[index]==b'\xb3'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="putstatic"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand    
        elif(bytess[index]==b'\x12'):
            index+=1
            subindex1=byte_to_int(bytess[index])
            instruction['opcode']="ldc"
            operand.append(get_bytes_from_index(clazz,subindex1))
            instruction['operand']=operand
        elif(bytess[index]==b'\xb1'):
            
            instruction['opcode']="return"
            instruction['operand']=operand    
        elif(bytess[index]==b'\xb4'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="getfield"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand
        elif(bytess[index]==b'\xb5'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="putfield"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand    
        elif(bytess[index]==b'\xb6'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="invokevirtual"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand 
        elif(bytess[index]==b'\xbb'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="new"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand
        elif(bytess[index]==b'\xbc'):
            typess={4:"T_BOOLEAN",
                    5:"T_CHAR",
                    6:"T_FLOAT",
                    7:"T_DOUBLE",
                    8:"T_BYTE	",
                    9:"T_SHORT",
                    10:"T_INT",
                    11:"T_LONG"}
            index+=1
            atype=byte_to_int(bytess[index])
            operand.append(typess[atype])
            instruction['opcode']="newarray"
            instruction['operand']=operand
        
        elif(bytess[index]==b'\xb7'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="invokespecial"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand
        elif(bytess[index]==b'\xb8'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="invokestatic"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            instruction['operand']=operand
        elif(bytess[index]==b'\xba'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            instruction['opcode']="invokedynamic"
            operand.append(get_bytes_from_index(clazz,(subindex1<<8)|subindex2))
            operand.append(0)
            operand.append(0)
            instruction['operand']=operand
        elif(bytess[index]==b'"'):
            
            instruction['opcode']="fload_0"
            instruction['operand']=operand
        elif(bytess[index]==b'#'):
            
            instruction['opcode']="fload_1"
            instruction['operand']=operand
        elif(bytess[index]==b'$'):

            instruction['opcode']="fload_2"
            instruction['operand']=operand
        elif(bytess[index]==b'%'):
            
            instruction['opcode']="fload_3"
            instruction['operand']=operand    
        elif(bytess[index]==b'C'):
            
            instruction['opcode']="fstore_0"
            instruction['operand']=operand
        elif(bytess[index]==b'D'):
            
            instruction['opcode']="fstore_1"
            instruction['operand']=operand
        elif(bytess[index]==b'E'):
            instruction['opcode']="fstore_2"
            instruction['operand']=operand
        elif(bytess[index]==b'F'):
            
            instruction['opcode']="fstore_3"
            instruction['operand']=operand                               
        elif(bytess[index]==b'Y'):
            
            instruction['opcode']="dup"
            instruction['operand']=operand
        elif(bytess[index]==b'K'):
            
            instruction['opcode']="astore_0"
            instruction['operand']=operand     
        elif(bytess[index]==b'L'):
            
            instruction['opcode']="astore_1"
            instruction['operand']=operand
        elif(bytess[index]==b'M'):
            
            instruction['opcode']="astore_2"
            instruction['operand']=operand
        elif(bytess[index]==b'N'):
            
            instruction['opcode']="astore_3"
            instruction['operand']=operand
        elif(bytess[index]==b':'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            operand.append(get_bytes_from_index(clazz,subindex1))
            instruction['opcode']="astore"

        elif(bytess[index]==b'*'):
            
            instruction['opcode']="aload_0"
            instruction['operand']=operand         
        elif(bytess[index]==b'+'):
            
            instruction['opcode']="aload_1"
            instruction['operand']=operand 
        elif(bytess[index]==b','):
            
            instruction['opcode']="aload_2"
            instruction['operand']=operand
        elif(bytess[index]==b'-'):
            
            instruction['opcode']="aload_3"
            instruction['operand']=operand
        elif(bytess[index]==b'\x1a'):
            
            instruction['opcode']="iload_0"
            instruction['operand']=operand    
        elif(bytess[index]==b'\x1b'):
            
            instruction['opcode']="iload_1"
            instruction['operand']=operand    
        elif(bytess[index]==b'\x1c'):
            
            instruction['opcode']="iload_2"
            instruction['operand']=operand
        elif(bytess[index]==b'\x1d'):
            
            instruction['opcode']="iload_3"
            instruction['operand']=operand 
        elif(bytess[index]==b';'):
            
            instruction['opcode']="istore_0"
            instruction['operand']=operand
        elif(bytess[index]==b'<'):
            
            instruction['opcode']="istore_1"
            instruction['operand']=operand       
        elif(bytess[index]==b'='):
            
            instruction['opcode']="istore_2"
            instruction['operand']=operand
        elif(bytess[index]==b'>'):
            
            instruction['opcode']="istore_3"
            instruction['operand']=operand
        elif(bytess[index]==b'`'):
            
            instruction['opcode']="iadd"
            instruction['operand']=operand
            

        elif(bytess[index]==b'\x00'):
            
            instruction['opcode']="nop"
            instruction['operand']=operand
        elif(bytess[index]==b'\x01'):
            
            instruction['opcode']="aconst_null"
            instruction['operand']=operand        
        elif(bytess[index]==b'\x02'):
            
            instruction['opcode']="iconst_m1"
            instruction['operand']=operand    
        elif(bytess[index]==b'\x03'):
            
            instruction['opcode']="iconst_0"
            instruction['operand']=operand    
        elif(bytess[index]==b'\x04'):
            
            instruction['opcode']="iconst_1"
            instruction['operand']=operand
        elif(bytess[index]==b'\x05'):
            
            instruction['opcode']="iconst_2"
            instruction['operand']=operand
        elif(bytess[index]==b'\x06'):
            
            instruction['opcode']="iconst_3"
            instruction['operand']=operand
        elif(bytess[index]==b'\x07'):
            
            instruction['opcode']="iconst_4"
            instruction['operand']=operand
        elif(bytess[index]==b'\x08'):
            
            instruction['opcode']="iconst_5"
            instruction['operand']=operand
        elif(bytess[index]==b'\x0b'):
            
            instruction['opcode']="fconst_0"
            instruction['operand']=operand
        elif(bytess[index]==b'\x0c'):
            
            instruction['opcode']="fconst_1"
            instruction['operand']=operand
        elif(bytess[index]==b'\x0d'):
            
            instruction['opcode']="fconst_2"
            instruction['operand']=operand              
        elif(bytess[index]==b'\x10'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            operand.append(get_bytes_from_index(clazz,subindex1))
            instruction['opcode']="bipush"
            instruction['operand']=operand     
        elif(bytess[index]==b'\x19'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            operand.append(get_bytes_from_index(clazz,subindex1))
            instruction['opcode']="aload"
            instruction['operand']=operand
        elif(bytess[index]==b'\x9f'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            instruction['opcode']="if_icmpeq"
            instruction['operand']=operand    
        elif(bytess[index]==b'\xa0'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            instruction['opcode']="if_icmpne"
            instruction['operand']=operand    
        elif(bytess[index]==b'\xa1'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            instruction['opcode']="if_icmplt"
            instruction['operand']=operand    
        elif(bytess[index]==b'\xa2'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            instruction['opcode']="if_icmpge"
            instruction['operand']=operand    
        elif(bytess[index]==b'\xa3'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            instruction['opcode']="if_icmpgt"
            instruction['operand']=operand
        elif(bytess[index]==b'\xa4'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8 )|subindex2
            operand.append(indexx)
            
            instruction['opcode']="if_icmple"
            instruction['operand']=operand
        elif(bytess[index]==b'\x4f'):
           
            instruction['opcode']="iastore"
            instruction['operand']=operand
        elif(bytess[index]==b'\x33'):
           
            instruction['opcode']="baload"
            instruction['operand']=operand
        elif(bytess[index]==b'\x34'):
           
            instruction['opcode']="caload"
            instruction['operand']=operand       
        elif(bytess[index]==b'\x54'):
           
            instruction['opcode']="bastore"
            instruction['operand']=operand
        elif(bytess[index]==b'\x55'):
           
            instruction['opcode']="castore"
            instruction['operand']=operand     
        elif(bytess[index]==b'\x84'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            
            operand.append(subindex1)
            operand.append(subindex2)
            
            instruction['opcode']="iinc"
            instruction['operand']=operand
        elif(bytess[index]==b'\xa7'):
            
            index+=1
            subindex1=byte_to_int(bytess[index])
            index+=1
            subindex2=byte_to_int(bytess[index])
            indexx=(subindex1<<8)|subindex2
            operand.append(indexx)
            
            
            instruction['opcode']="goto"
            instruction['operand']=operand
        elif(bytess[index]==b'W'):
            instruction['opcode']="pop"
            instruction['operand']=operand
        elif(bytess[index]==b'.'):
            instruction['opcode']="iaload"
            instruction['operand']=operand                                                                                              
        else:
            print(f"{bytess[index]} is not implemented in parse_byte_code_from_attribute")  
        instructions.append(instruction)

        index+=1
       
    return instructions