import os
import Storage
import Term
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
storage = Storage.Storage()

# Load default config and override config from an environment variable
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/Terms/Add',methods=['GET'])
def add_term():
    return render_template('CreateTerm.html')

@app.route('/Terms/Add',methods=['POST'])
def add_term_post():
    if request.form["description"]:
        storage.SaveTerm(Term.Term( request.form["description"]))
    return redirect(url_for('terms'))

@app.route('/Terms',methods=['GET'])
def terms():
    terms = storage.GetTerms()
    return render_template('Terms.html',terms = terms)






if __name__ == '__main__':
    app.run()