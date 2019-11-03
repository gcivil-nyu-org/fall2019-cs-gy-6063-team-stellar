import csv
def load_cuisine(file):
    with open(file, "r") as in_f:
        cuisinelist = []
        while True:
            line = in_f.readline()
            if not line:
                break
            linelist = line.strip().split(",")
            if not linelist[7].strip('\"') in cuisinelist:
                cuisinelist.append(linelist[7].strip('\"'))
        cuisinelist = cuisinelist[1:]
        return cuisinelist
cuisine_list=load_cuisine("datasource\DOHMH_New_York_City_Restaurant_Inspection_Results.csv")
cuisine_table={}
def load_user(file):
    with open(file, "r") as in_f:
        userlist = []
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            userlist.append(linelist)
        return userlist[1:]
userlist=load_user("users.csv")
print(userlist)
for cuisine in cuisine_list:
    cuisine_table[cuisine]=[]
for user in userlist:
    p_cuisine_str=user[3].strip('[').strip(']')
    p_cuisine_list=p_cuisine_str.split(',')
    print(p_cuisine_list)


