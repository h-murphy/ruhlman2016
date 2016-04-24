#Using python-docx module to parse the Ruhlman word files
#(rough)
#Megan, 4/12/16

import docx
from docx import Document
import os
import csv


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
    presenters = p.split(", ")
    split = p.split(u'\u2019')
    years = []
    for i,s in enumerate(split):
        if i%2 == 1 and s[0] == u'1':
            years.append('20'+s[:2])
            if years[-1] == '20Co':
                print p
    years = ', '.join(years)
    majors = ', '.join([x for x in presenters if x.find(u'\u2019') == -1])
#     years = [u'20'+x[x.find(u'\u2019')+1:] for x in presenters if x.find(u'\u2019') != -1]
    students = [x[:x.find(u'\u2019')-1] for x in presenters if x.find(u'\u2019') != -1]
    if len(students) > 1:
        if "and" in students[-1]:
            students[-1] = students[-1].split("and ")[1]
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
            print
            title = sesh[i][0].split(" (")[0]
        students = s[p-1].strip()
        s_info = p_mjr_and_yr(students)
        advisor = "ADVISOR: " + s[p].split(": ")[1].strip()
        major = u', '.join(ad_major(advisor))
        projects.append({"Title": title, \
                         "Advisor_Major": major,\
                         "Advisor": advisor, \
                         "Students": students,\
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
    
projects = pd.DataFrame(all_projects)
projects = projects.T

projects.to_csv("cleaned_2010.csv", encoding='utf-8')