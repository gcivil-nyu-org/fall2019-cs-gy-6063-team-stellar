import csv
import random
import datetime

def load_cuisine(file):
    with open(file,"r",encoding='utf-8') as in_f:
        cuisinelist=[]
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            cuisinelist.append(linelist[7])
        return cuisinelist[1:]
#change string to list
def str_to_list(string):
    string_content = string.strip('[').strip(']')
    string_list = string_content.split('\'')
    out_list = []
    for item in string_list:
        if item == ', ' or item == '':
            continue
        else:
            out_list.append(item)
    return out_list
def create_cuisine_table(cuisine_list,userlist):
    cuisine_table = {}
    for cuisine in cuisine_list:
        cuisine_table[cuisine] = []
    for user in userlist:
        real_p_cuisine_list = user['cuisine']
        for c in real_p_cuisine_list:
            cuisine_table[c].append(user['user_id'])

    return cuisine_table

def load_user(file):
    with open(file, "r") as in_f:
        userlist = []

        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            user_dict = {}
            user_dict["user_id"]=linelist[0]
            user_dict["school"]=linelist[1]
            user_dict["department"]=linelist[2]
            user_dict["cuisine"]=str_to_list(linelist[3])
            user_dict["prefer_department"]=str_to_list(linelist[4])
            user_dict["meet_history"]=str_to_list(linelist[5])
            userlist.append(user_dict)
        return userlist[1:]
cuisine_list=load_cuisine("datasource\DOHMH_New_York_City_Restaurant_Inspection_Results.csv")
userlist=load_user("users.csv")
cuisine_table=create_cuisine_table(cuisine_list,userlist)


def match(userlist,cuisine_table):
    match_result=[]
    unmached_user=[]
    matchpool=set()
    for user in userlist:
        matchpool.add(user['user_id'])

    for user in userlist :
        user_id=user['user_id']

        if user_id in matchpool:

            #remove selected user
            matchpool.remove(user_id)

            # get the preferred cuisine
            real_p_cuisine_list = user['cuisine']

            # find available users for this user(filter)
            available_set = set()
            for c in real_p_cuisine_list:
                available_set = available_set.union(set(cuisine_table[c]))
            available_set=available_set.intersection(matchpool)
            user_meet_history = user['meet_history']

            # remove met users
            if not len(user_meet_history) == 0:
                for u in user_meet_history:
                    available_set.remove(u[0])
            # pick a user from the available users
            try:
                match_user_id = random.choice(list(available_set))
                match_user = userlist[int(match_user_id)]
                match_user_meet_history = match_user['meet_history']

                matchpool.remove(match_user_id)
                result = str(user_id) + "----" + str(match_user_id)
                user_meet_history.append((match_user_id, today))
                match_user_meet_history.append((user_id, today))
                match_result.append(result)
            except Exception:
                unmached_user.append(user)
    print(match_result)
    print(unmached_user)





            ####


today=datetime.date.today()
print(today)
print(type(today))
match(userlist,cuisine_table)


