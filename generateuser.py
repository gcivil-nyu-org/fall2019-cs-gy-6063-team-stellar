import random
import csv
import sqlite3
import datetime


def load_school(file):
    with open(file,"r",encoding='utf-8') as in_f:
        schoollist=[]
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            schoollist.append((linelist[0], linelist[1]))
        return schoollist[1:]


def load_department(file):
    with open(file, "r",encoding='utf-8') as in_f:
        departmentlist = []
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            departmentlist.append((linelist[0], linelist[1]))
        return departmentlist[1:]


def load_cuisine(file):
    with open(file,"r",encoding='utf-8') as in_f:
        cuisinelist=[]
        f_csv = csv.reader(in_f)
        for linelist in f_csv:
            if linelist[7] in cuisinelist:
                continue
            cuisinelist.append(linelist[7])
        return cuisinelist[1:]


def merge(school_list, department_list):
    school_department = {}
    id_school = {}
    department_school = {}
    school = []
    department = []
    for schoolitem in school_list:
        school.append(schoolitem[0])
        id_school[str(schoolitem[1])] = schoolitem[0]
        school_department[schoolitem[0]] = []
    for departmentitem in department_list:
        department.append(departmentitem[0])
        school_department[id_school[str(departmentitem[1])]].append(departmentitem[0])
        department_school[departmentitem[0]] = [id_school[str(departmentitem[1])]]

    school_department["select school"] = department
    return school, department, school_department, department_school


def generateuser(N, schools, cuisines):
    userlist = []
    all_department = []
    for s in schools:
        all_department = all_department+school_department[s]

    for user_id in range(0,N):
        user={}
        user["user_id"]=user_id
        school_id=random.randint(0,len(schools)-1)
        user["school"]=schools[school_id]
        departments=school_department[schools[school_id]]
        department_id=random.randint(0,len(departments)-1)
        user["department"]=departments[department_id]
        p_cuisine_number=random.randint(1,len(cuisines)-1)
        p_cuisine=random.sample(cuisines,p_cuisine_number)
        user["prefered cuisines"]=p_cuisine
        p_department_number=random.randint(1,len(all_department)-1)
        p_department=random.sample(all_department,p_department_number)
        user["prefered departments"]=p_department
        user["meet history"]=[]
        userlist.append(user)
    return userlist
def save_users(path,userlist):
    with open(path, 'w',newline='',encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(userlist[0].keys())
        for user in userlist:
            w.writerow(user.values())
            cur.execute(
                "INSERT INTO homepage_userrequest (user_id, service_type,time_stamp, cuisine, school, department) VALUES (?, ?, ?, ? , ? ,?)",
                (
                    user["user_id"],
                    user["service_type"],
                    datetime.datetime.now(),
                    str(user["prefered cuisines"]),
                    user["school"],
                    user["prefered departments"],
                ),
            )
    conn.commit()
    conn.close()


# Usage:
# N: the number of user you want to generate
# Selected_school: Generate users from selected school


N=10
selected_school=['Tandon School of Engineering']

# execute code
department_list=load_department("datasource\\Department.csv")
school_list=load_school("datasource\\School.csv")
cuisine_list=load_cuisine("datasource\DOHMH_New_York_City_Restaurant_Inspection_Results.csv")
school, department, school_department, department_school=merge(school_list,department_list)
userlist=generateuser(N,selected_school,cuisine_list[:3])
save_users("users.csv",userlist)





