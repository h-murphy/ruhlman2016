#Using python-docx module to parse the Ruhlman word files
#(rough)
#Megan, 4/12/16

import docx
from docx import Document
import os
import csv
import pandas as pd


#all the files

f = open('2010.docx')
document = docx.Document(f)
paragraphs = [p.text for p in document.paragraphs]
# print paragraphs[0:50]


types = ["short talks", "panel", "performance", "long performance",\
          "poster session", "literary reading/ short performance", "exhibition",\
        "field studies/ performance"]

#break up paragraphs into sessions. parser = types
indices = []
for i,p in enumerate(paragraphs):
    if "(" in p:
        tipe = p.split("(")[1].split(")")[0]
        if tipe in types:
            indices.append(i)

sesh = []
for i in range(0, len(indices)):
    if i < len(indices)-1:
        sesh.append(paragraphs[indices[i]:indices[i+1]])
    else:
        sesh.append(paragraphs[indices[i]:])
    
sesh_inds = []
for s in sesh:
    sesh_inds.append([])
    for j,v in enumerate(s):
        if 'advisor' in v:
            sesh_inds[-1].append(j)

def ad_major(ad):
    major_return = []
    ad_return = []
    ad = ad.split(' and ')
    if len(ad) == 1: #only one advisor
        v = ad[0].split(', ',1)
        major_return = [v[1]]
    elif len(ad) == 2:
        ad = [x.split(", ") for x in ad]
        if len(ad[0]) ==2 and len(ad[1]) ==1:#second cell is part of advisor's major
            major_return = [ad[0][1] + ' and ' + ad[1][0]]
        elif len(ad[0]) ==2 and len(ad[1])==2:#two advisors
            major_return = [ad[0][1], ad[1][1]]
        elif len(ad[0])==4:#two advisors + one advisor
            major_return = [ad[0][1], ad[0][3], ad[1][1]]
    else:
        if "Physical Education" in ad[0]:#PE instructors
            pe = ad[0].split(", ",1)[1] + ' and ' + ad[1].split(",")[0]
            if len(ad) == 4:#two PE instructors
                major_return = [pe, pe]
            else:#one PE instructor, one advisor
                major_return = [pe, ad[2].split(", ")[1]]
        else:#special case
            major_return = [ad[0].split(", ")[1]+ ' and '+ad[1], ad[2].split(", ")[1]]
    major_return = [x.split(",")[0].strip() for x in major_return]
    return major_return

def p_mjr_and_yr(p):
    #init
    students = []
    years = []
    majors = []
    
    presenters = p.split(",")
    i = 0
    while i < len(presenters):
        split = presenters[i].split(u'\u2019')

        #student - count for "and"
        if "and" in split[0]:
            students.append(split[0].split("and")[1].strip())
        else:
            students.append(split[0].strip())

        #years
        years.append(u'20'+split[1].strip())
        i += 1 #increment

        #majors - account for undeclared
        if i < len(presenters): #2nd to last elt in lst or earlier
            if u'\u2019' in presenters[i]:#if next is presenter, not major
                majors.append("Unspecified")
            else:
                majors.append(presenters[i].strip())
                i += 1
        else:
            majors.append("Unspecified")
        
    students = u', '.join(students)
    majors = u', '.join(majors)
    years = u', '.join(years)
    return students, majors, years

#init
projects = [] #dict of each project
titles = []

for i,s in enumerate(sesh):
    inds = sesh_inds[i]
    for j,p in enumerate(inds):
        titles.append(s[p-2])
        title = s[p-2].strip()
        if title == "/":
            title = sesh[i][0].split(" (")[0]
        students = s[p-1].strip()
        s_info = p_mjr_and_yr(students)
        advisor = "ADVISOR: " + s[p].split(": ")[1].strip()
        major = u', '.join(ad_major(advisor))
        projects.append({"Title": title, \
                         "Advisor_Major": major,\
                         "Advisor": advisor, \
                         "Students": s_info[0],\
                         "Student_Major": s_info[1], \
                         "Student_Year": s_info[2], \
                         "Year": u'2010'
                        })
        if j < len(inds)-1:
            for v in range(p+1, inds[j+1]):
                if s[v][-1] != " ":
                    end = v+1
                    break
            projects[-1].update({"Abstract": ''.join(s[p+1:end])})
        else:
            if len(s[-1]) > 26:
                projects[-1].update({"Abstract": ''.join(s[p+1:])})
            else:
                projects[-1].update({"Abstract": ''.join(s[p+1:-1])})

all_projects = {}
for k, v in enumerate(projects):
    all_projects[k] = v
    
projects = pd.DataFrame(all_projects).T
projects.to_csv("2010.csv", encoding='utf-8')