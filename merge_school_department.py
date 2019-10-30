import csv


def merge(school, department):
    with open(school, "r", encoding="utf-8") as in_f1, open(
        department, "r", encoding="utf-8"
    ) as in_f2:
        read_school = csv.reader(in_f1)
        read_department = csv.reader(in_f2)
        schoollists = []
        departmentlists = []
        for i in read_school:
            schoollists.append(i)
        for i in read_department:
            departmentlists.append(i)
        school_department = {}
        id_school = {}
        for schoolitem in schoollists[1:]:
            id_school[schoolitem[1]] = schoolitem[0]
            school_department[schoolitem[0]] = []
        for departmentitem in departmentlists[1:]:
            school_department[id_school[departmentitem[1]]].append(departmentitem[0])
        return school_department


merge("datasource\\School.csv", "datasource\\Department.csv")


# csvFile = open('datasource\\Department.csv', "r")
# reader = csv.reader(csvFile)
# for i in reader:
#     print(i)
