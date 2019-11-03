import csv
import random
def load_cuisine(file):
    with open(file,"r",encoding='utf-8') as in_f:
        cuisinelist=[]
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            cuisinelist.append(linelist[7])
        return cuisinelist[1:]
mylist=["a","b","c","d","e","f","g","h"]
ewlist = random.sample(mylist, 6)
print(ewlist)
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
# print(userlist)
for cuisine in cuisine_list:
    cuisine_table[cuisine]=[]
for user in userlist:
    p_cuisine_str=user[3].strip('[').strip(']')
    p_cuisine_list=p_cuisine_str.split('\'')
    real_cuisine_list=[]
    for item in p_cuisine_list:
        if item == ', ' or item == '':
            continue
        else:
            real_cuisine_list.append(item)
#     print(real_cuisine_list)
#     for c in real_cuisine_list:
#         cuisine_table[c].append(user[0])
# print(cuisine_table)



