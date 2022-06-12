import timeit
from timeit import default_timer as timer
start = timer()
# SQL server connection:
import mysql.connector
db = mysql.connector.connect(
    host= "localhost",
    user= "ELECTOR",
    password= "c-env_n57rdx",
    database="elector"
)
mycursor = db.cursor()
path = r'C:\Users\USER\Desktop\מנדי\Elector\elector_full.txt'
input_file = open(path, encoding="utf8")

numbers = "1234567890"
alphabet = "abcdefghijklmnopqrstuvwxyz -/אבגדהוזחטיכךלמםנןסעפףצץקרשת"

def city_f(address):
    find = address.find(",")
    city = address[(find+1):(len(address))]
    return city
def street_f(address):
    global numbers
    i = 0
    while address[i] != "," and address[i] not in numbers:
        i += 1
    street = address[0:i]
    return street
def home_number_f(address):
    end = address.find(",")
    part = address[0:end]
    start = part.rfind(" ")
    num = address[start+1:end]
    return num

def orgnaizing_elector(line,counter):
    line = find_problem_and_fix(line)
    if len(line) < 20:
        line = backupfixer(line,comma_indexes(line))
    commaindexes = comma_indexes(line)
    first_name = ""
    last_name = ""
    id = ""
    address = ""
    street = ""
    address = ""
    city_id = ""
    city = ""
    for comma in range(0, len(commaindexes)):
        match comma:
            case 0:
                first_name = line[0:commaindexes[comma]-1]
            case 1:
                last_name = line[(commaindexes[comma-1]) + 2:(commaindexes[comma]) - 1]
            case 2:
                id = line[(commaindexes[comma-1]) + 2:(commaindexes[comma]) - 1]
            case 3:
                address = line[(commaindexes[comma-1]) + 2:(commaindexes[comma]) - 1]
            case 4:
                city_id = line[(commaindexes[comma-1]) + 2:(commaindexes[comma]) -1]
    try:
        street = street_f(address=address)
        city = city_f(address=address)
        address = home_number_f(address=address)
    except:
        city = address
        address = " - "
        street = " - "
    finally:
        print("first name is "+first_name)
        print("last name is "+last_name)
        print("ID is "+id)
        print("address is: "+address)
        print("street is: "+street)
        print("city is: "+city)
        print("home number: " + address)
        print("city_id is: "+city_id)
        sql_query = "INSERT INTO main_data (First_Name, Last_Name, ID, City, Street, Address, City_ID, Line_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (first_name,last_name,id,city,street,address,city_id,counter)
        mycursor.execute(sql_query, val)
        db.commit()
        print(mycursor.rowcount, "record inserted.")
    return commaindexes

def find_problem_and_fix(line_1):
    global numbers,alphabet
    line_set = ""
    comma_index = comma_indexes(line_1)
    print(comma_index)
    line_len = len(line_1)
    print(line_len)
###################################
    mistake = 1
    finish = False
# Does they checked? :
    fn = False
    fn_error = 0
    ln = False
    ln_error = 0
    ad = False
    ad_error = 0
    fn_e_index = 1
    ln_e_index = fn_e_index+1
    ad_e_index = ln_e_index+3
    if len(comma_index) >= 8:
        while finish != True:
            for i in range(mistake):
                for c in range(line_len):
                    cindex = line_1[c]
                    #This is for the 'First_Name' :
                    if line_len > 10:
                        if (c == ((comma_index[fn_e_index])-2)):
                            if (cindex == "צ") or (cindex == "ז") or (cindex == "ג") or (cindex == "ח") or (cindex == "ת"):
                                if (line_1[comma_index[ln_e_index] + ((comma_index[ln_e_index + 1] - comma_index[ln_e_index]) // 2)] in numbers) and (fn_error == 0):
                                    line_set = line_set + "'" + line_1[comma_index[fn_e_index-1]+1:comma_index[fn_e_index]] + "'" +","
                                    fn_error += 1
                                elif fn_error == 0:
                                    line_set = line_set + "'" + fixed_line(name_err="fn", line= line_1, comma_indexes=comma_index) + "'" + ","
                                    comma_index.pop(fn_e_index)
                                    fn_error = fn_error + 1
                                    mistake += 1
                            elif fn_error == 0:
                                line_set = line_set + "'" + line_1[comma_index[fn_e_index-(1+fn_error)]+2:comma_index[fn_e_index]-1] +"'"+","
                        fn = True
                        # this is for the 'Last_name' and 'ID':
                        if (c == (comma_index[ln_e_index]-2)):
                            if cindex in alphabet:
                                if line_1[comma_index[ln_e_index] + ((comma_index[ln_e_index + 1] - comma_index[ln_e_index]) // 2)] in numbers:
                                    if ln_error == 0:
                                        line_set = line_set + "'" + line_1[comma_index[ln_e_index - (1 + ln_error)]+2:comma_index[ln_e_index]-1] + "'" + ","
                                        line_set = line_set + "'" + line_1[comma_index[ln_e_index]+2:comma_index[ln_e_index+1]-1] + "'" + ","
                                else:
                                    line_set = line_set + "'" + fixed_line(name_err="ln", line=line_1, comma_indexes=comma_index) + "'" +","
                                    comma_index.pop(ln_e_index)
                                    line_set = line_set + "'" + line_1[comma_index[ln_e_index] + 2:comma_index[ln_e_index + 1] - 1] + "'" + ","
                                    # ln_e_index += 1
                                    mistake += 1
                                    ln_error += 1
                            elif ln_error == 0:
                                line_set = line_set + "'" + fixed_line(name_err="ln-id", line=line_1, comma_indexes=comma_index) + "'" + ","
                        ln = True
                        #This is for 'Address' :
                        if (c == (comma_index[ad_e_index]-2)):
                            if cindex in alphabet or (cindex in numbers and cindex == "0"):
                                if line_1[comma_index[ad_e_index] + 2] == "0":
                                    if ad_error == 0:
                                        line_set = line_set + "'" + line_1[comma_index[ad_e_index - 1]+2:comma_index[ad_e_index]-1] + "'"
                                elif ad_error  == 0:
                                    line_set = line_set + "'" + fixed_line(name_err="ad", line=line_1, comma_indexes=comma_index) + "'"
                                    comma_index.pop(ad_e_index)
                                    mistake += 1
                                    ad_error += 1
                        if (c == comma_index[len(comma_index)-1]) and (len(comma_index) >= 9 ):
                            city_id = line_1[comma_index[8]:line_len - 1]
                            line_set += city_id
                        ad = True
                    else:
                        line_set += cindex
                    if (fn==True) and (ln==True) and (ad==True):
                        finish = True
    line_set += ","
    line_set += "'"
    return str(line_set)

def backupfixer(line,commainexes):
    global alphabet,numbers
    fixed = ""
    count = 0
    id_count = 0
    for c in range(commainexes[0],len(line)):
        if line[c] in alphabet or line[c] == "'":
            if count < 49:
                fixed += line[c]
                count += 1
            else:
                fixed += ","
                count = 0
        elif line[c] == ",":
            fixed += " "
            count += 1
        elif line[c] in numbers:
            if id_count < 10:
                if line[c-2] == ",":
                    fixed += ","
                    fixed += line[c]
                    id_count += 1
                    count = 0
                else:
                    fixed += line[c]
                    id_count += 1
        if id_count >= 9 and id_count <= 10:
            fixed += ","
            id_count += 1
    return fixed

def comma_indexes(line):
    comma_i = []
    leng = len(line)
    for c in range(0, leng):
        if line[c] == ",":
            if line[c+1] == "'" and line[c-1] == "'":
                if (c-2 >= 0):
                    if line[c-2] != ",":
                        comma_i.append(c)
    return comma_i
def geresh_indexes(line):
    geresh_i = []
    for c in range(0,len(line)):
        if line[c] == "'":
            geresh_i.append(c)
    return geresh_i

def fixed_line(name_err,line,comma_indexes):
    global alphabet,numbers
    # Starts Values:
    comma_c = 0
    fixed = ""
    # Fix problem of dividing the first_name because of ' in the middle of the name:
    if name_err == "fn":
        err_place = 0
        #Start a loop in the range of err_place to end of the error:
        for c in range(comma_indexes[err_place]+1, comma_indexes[err_place+2]):
            char = line[c]
            if char in alphabet:
                fixed += char
            elif char == ",":
                comma_c += 1
                if comma_c == 2:
                    fixed += ","
            elif char == "'":
                if ((c > comma_indexes[err_place]+1)and(c < comma_indexes[err_place+2]-1)):
                    if fixed[len(fixed)-1] != "'":
                        fixed += "'"
    # Fix the same problem as the previous but in the last_name:
    elif name_err == "ln":
        err_place = 2
        for c in range(comma_indexes[err_place-1]+1, comma_indexes[err_place + 1]):
            char = line[c]
            if char in alphabet:
                fixed += char
            elif (char == "'") and (line[c+3] in alphabet):
                if len(fixed) > 1:
                    if fixed[len(fixed)-1] != "'":
                        fixed += char
    # Fix problem of mixing the last_name with the ID number:
    elif name_err == "ln-id":
        err_place = 1
        num_1 = ""
        num_2 = ""
        ln = ""
        comma = False
        for c in range(comma_indexes[err_place]+1, comma_indexes[err_place + 2]):
            char = line[c]
            if char in alphabet:
                ln += char
            elif char == ",":
                comma = True
            elif char == "'":
                if len(fixed) > 1:
                    if fixed[len(fixed) - 1] != "'":
                        if fixed[len(fixed)-1] == "," or ((fixed[len(fixed)-1] in alphabet) and (fixed[len(fixed)-1] != " ")):
                            fixed += "'"
            elif char in numbers:
                if comma != True:
                    if num_1 != "":
                        num_1 += char
                    else:
                        num_1 += char
                else:
                    num_2 += char
        fixed = fixed +"'"+ln+"','"+num_2+num_1+"'"
    # Fix the same problem as the first two did but in the address:
    elif name_err == "ad":
        err_place = 4
        for c in range(comma_indexes[err_place] + 1, comma_indexes[err_place + 2]):
            char = line[c]
            if char in alphabet:
                fixed += char
            elif char == "'":
                if len(fixed) > 1:
                    if fixed[len(fixed) - 1] != "'":
                        if fixed[len(fixed) - 1] == "," or (
                                (fixed[len(fixed) - 1] in alphabet) and (fixed[len(fixed) - 1] != " ")):
                            fixed += "'"
            elif (char in numbers):
                if ((c == comma_indexes[err_place + 2]) and (char != "0")):
                    fixed += char
            elif char == "(":
                fixed += ")"
            elif char == ")":
                fixed += "("
    return str(fixed)
# line_1 = "'8275023','ג','ודית','רגב','055270615','','קלאוזנר יוסף 11/7, ראשון לציון','0','0','false'"

# pppp = "'11349836','עומר','אלמעאבדה','301600466','','אבו ג','ווייעד )שבט( 0','שבט אבו ג'ווייעד '','0','0'"
# ooooo = "'10681584','כפיר','שחר','065732422','','מחנה יוכבד 27, מחנה יוכבד','0','0','false','706'"
# print(find_problem_and_fix(pppp))
# print(find_problem_and_fix(ooooo))
# line_p = "'10896864','ת','אירה'','נוג','יידאת'','036999555','','נוג','ידאת 0','בועיינה-נוג'ידאת''"
# line_w = "'10896864','ת','אירה'','נוג'יידאת'','036999555','','נוג','ידאת 0','בועיינה-נוג'ידאת''"
# print(backupfixer(line_w,comma_indexes(l)))
# ee = find_problem_and_fix(line_p)
# print(ee)
# print(comma_indexes(ee))
counted = 2704056
counter = 1
line = input_file.readline()
while line != "endless":
    counter += 1
    line = str(input_file.readline())
    if counter >= counted :
        print(line)
        orgnaizing_elector(line,counter=counter)
        print("counter:",counter)
input_file.close()
# print(find_problem_and_fix(line_p))
#print(find_problem_and_fix(line_w))
#print(line_w)
# print(find_problem_and_fix(line_p))
# print(orgnaizing_elector(line_p,1))
ends = timer()
print(ends- start)
