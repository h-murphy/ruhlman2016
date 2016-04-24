
#Takes class year and finds its associated class color
def give_color(year):
    if (2016-year)%4 == 0:
        return "red"
    elif (2015-year)%4 == 0:
        return "green"
    elif (2014-year)%4 == 0:
        return "purple"
    else:
        return "yellow"


#Takes a csv file and renders bar graph of student participation as function class color
def class_colors(csv_file):
    frame = pd.DataFrame(projects)
    allyears = frame["Student_Year"].values.tolist()
    class_colors = []
    for i in allyears:
        ys = eval(i)
        if type(ys) == int:
            class_colors.append(give_color(ys))
        else:
            colors_lst = []
            for j in ys:
                colors_lst.append(give_color(j))
            class_colors.append(", ".join(colors_lst))
    frame['Student_Color'] = class_colors
    allcolors = u', '.join(frame["Student_Color"].values.tolist()).split(", ")
    counter=collections.Counter(allcolors)
    distrib = dict(counter)

    pd.DataFrame(distrib, index=["Number of Students"]).T.plot.bar(rot=0, \
                                                         figsize=(10,10), \
                                                         title="Participation Distributed by Class Color",\
                                                         color=["green", "purple", "red", "yellow"],\
                                                        )

#Takes a CSV file, and renders a bar graph of the student participation as function of class year
def class_distrib(csv_file):
    frame = pd.DataFrame(csv_file)
    allyears = u', '.join(frame["Student_Year"].values.tolist()).split(", ")
    
    counter=collections.Counter(allyears)
    distrib = dict(counter)
    
    pd.DataFrame(distrib, index=["Students"]).T.plot.bar(rot=0, \
                                                         figsize=(10,10), \
                                                         title="Student Participation Distributed by Class",\
                                                         color="red")

