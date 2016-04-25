# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
#from wtforms.validators import Required, Length
import random, json, plotly
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)

# The CS counts are real (counted them for each year), the others are randomly
# generated.
countsDct = {"CS":  [2, 4, 2, 12, 14, 10, 9, 4, 5, 2, 9, 1, 6, 5, 5, 20, 17, 9, 11, 16],
"ECON": [random.choice(range(1,31)) for i in range(20)],
"MATH": [random.choice(range(1,21)) for i in range(20)],
"ART": [random.choice(range(1,21)) for i in range(10)] + [random.choice(range(1,15)) for i in range(10)]
}

countsDct = {'Africana': [0, 1, 1, 1, 0, 0, 0, 2, 1, 2, 2, 1, 1, 0, 2, 3, 2, 0, 0],
 'Anthropology': [4, 3, 5, 2, 6, 4, 0, 3, 2, 4, 5, 4, 6, 4, 4, 6, 0, 2, 5],
 'Art': [13,17,24,18,21,12,3,11,11,5,14,10,8,12,17,10,8,11,9],
 'Astronom': [0, 1, 4, 0, 1, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 2, 0, 2, 0],
 'Athletics': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 'Biolo': [20,19,24,22,15,15,16,33,19,10,25,16,30,23,25,25,10,15,12],
 'Chemistry': [7,17,13,16,12,13,10,34,19,16,21,16,16,19,24,19,9,16,8],
 'Classic': [1, 0, 0, 2, 3, 4, 2, 3, 0, 1, 2, 2, 2, 1, 6, 5, 2, 2, 2],
 'Computer': [3, 2, 11, 11, 9, 9, 3, 5, 2, 6, 2, 5, 4, 5, 10, 6, 9, 14, 8],
 'East Asian': [0, 0, 1, 0, 0, 0, 0, 1, 3, 3, 3, 2, 5, 1, 4, 4, 0, 1, 2],
 'Economic': [15,10,10,6,11,22,4,18,14,15,15,17,30,19,28,12,11,8,18],
 'Education': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2],
 'English': [22,20,37,18,17,19,3,15,15,8,20,10,10,14,11,18,10,5,12],
 'French': [4, 7, 9, 3, 5, 6, 1, 9, 4, 5, 8, 3, 10, 6, 6, 6, 6, 3, 5],
 'Geoscience': [0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 2, 4, 2, 3, 1, 2, 4, 2],
 'German': [0, 1, 1, 1, 0, 2, 0, 2, 0, 2, 2, 0, 1, 1, 0, 0, 0, 0, 0],
 'Histor': [13,22,17,12,13,9,8,16,13,5,21,9,10,14,19,14,12,11,8],
 'International': [8, 4, 7, 7, 10, 10, 7, 12, 5, 5, 3, 2, 5, 2, 8, 0, 0, 0, 4],
 'Italian': [1, 0, 5, 0, 0, 1, 0, 1, 0, 1, 1, 2, 3, 1, 1, 3, 1, 3, 0],
 'Linguistic': [0, 0, 0, 0, 0, 0, 0, 2, 3, 5, 4, 6, 4, 5, 2, 2, 2, 3, 5],
 'Math': [4, 9, 2, 3, 4, 9, 0, 5, 4, 7, 6, 3, 3, 2, 6, 2, 8, 4, 8],
 'Music': [1, 2, 2, 4, 6, 4, 1, 4, 4, 1, 7, 3, 9, 6, 3, 3, 5, 3, 4],
 'Philoso': [3, 4, 6, 2, 2, 6, 2, 4, 2, 3, 5, 4, 2, 2, 3, 1, 1, 1, 4],
 'Physics': [0, 3, 4, 8, 1, 7, 5, 4, 3, 4, 3, 2, 0, 2, 2, 3, 5, 7, 3],
 'Politic': [12,7,10,19,9,24,7,8,14,8,13,16,16,9,15,6,8,13,12],
 'Psychology': [25,23,25,27,15,20,6,20,11,7,18,17,17,13,17,17,13,11,17],
 'Religio': [2, 3, 3, 3, 5, 5, 3, 2, 1, 1, 0, 0, 2, 2, 6, 3, 2, 2, 0],
 'Russian': [2, 2, 2, 2, 1, 1, 0, 2, 0, 3, 1, 4, 1, 0, 0, 1, 0, 0, 1],
 'Sociology': [1, 12, 7, 6, 4, 6, 2, 5, 7, 4, 4, 7, 7, 7, 5, 4, 6, 5, 9],
 'Spanish': [4, 6, 3, 0, 7, 6, 2, 8, 10, 4, 6, 6, 12, 8, 6, 3, 4, 5, 4],
 'Unspecified': [13,27,13,5,8,1,6,8,4,16,2,5,9,1,1,18,4,15,7],
 'Women': [1, 2, 9, 1, 2, 3, 1, 4, 3, 4, 9, 4, 0, 6, 3, 3, 8, 2, 8]}


# One can create more than one plot and store them in a list, which will be
# turned into JSON to be passed to the client.
def make_bar_chart(choice):
    graphs = [
              dict(
                   data=[
                         dict(
                              x = range(1997,2017), # all the years from 1997 to 2016
                              y = countsDct[choice],
                              type = 'bar'
                              ),
                         ],
                   layout=dict(
                               title = choice + " students presenting at Ruhlman"
                               )
                   )
              ]
              # Convert the figures to JSON
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    print(graphJSON)
    return graphJSON


class ChoiceForm(Form):
    #name = StringField('What is your name?', validators=[Required(), Length(1, 16)])
    
    choice = SelectField(u'Departments', choices=[("blank", "Make a choice"), ("Africana", "Africana Studies"),
                                                  ('Anthropology', 'Anthropology'),
                                                  ('Art', 'Art'),
                                                  ('Astronom', 'Astronomy'),
                                                  ('Biolo','Biology'),
                                                  ('Chemistry', 'Chemistry'),
                                                  ('Classic', 'Classics'),
                                                  ('Computer', 'Computer Science'),
                                                  ('East Asian', 'East Asian Studies'),
                                                  ('Economic', 'Economics'),
                                                  ('Education', 'Education'),
                                                  ('English', 'English'),
                                                  ('French', 'French'),
                                                  ('Geoscience', 'Geosciences'),
                                                  ('German', 'German'),
                                                  ('Histor', 'History'),
                                                  ('International','International Relations'),
                                                  ('Italian', 'Italian'),
                                                  ('Linguistic', 'Linguistics'),
                                                  ('Math', 'Mathematics'),
                                                  ('Music','Music'),
                                                  ('Philoso','Philosophy'),
                                                  ('Physics', 'Physics'),
                                                  ('Politic','Politics'),
                                                  ('Psychology', 'Psychology'),
                                                  ('Religio', 'Religion'),
                                                  ('Russian', 'Russian'),
                                                  ('Sociology', 'Sociology'),
                                                  ('Spanish', 'Spanish'),
                                                  ('Unspecified', 'Unspecified'),
                                                  ('Women', 'Women and Gender Studies')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    
    choice = None
    ids = []
    graphJSON = []
    #ruhlman_data = pd.read_excel('test.xlsx')
    form = ChoiceForm()
    if form.validate_on_submit():
        choice = form.choice.data
        if choice != "blank":
            graphJSON = make_bar_chart(choice)
            ids = ["Bar Chart for {}".format(choice)]
        form.choice.data = ''
    return render_template('index.html', form=form, choice=choice,
                           graphJSON=graphJSON,
                           ids=ids) #data = ruhlman_data.to_html())


if __name__ == '__main__':
    app.run(debug=True, port = 7000)
    #app.run(host='0.0.0.0', port = 1561, debug=True)
