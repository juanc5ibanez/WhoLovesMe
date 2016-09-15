import os
import uuid

import Storage
import Term
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
storage = Storage.Storage()


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

@app.route('/Terms/Delete/<termId>')
def delete_term(termId=None):
    storage.DeteTerm(Term.Term('',id = uuid.UUID(termId)))
    return redirect(url_for('terms'))




if __name__ == '__main__':
    app.run()
    storage.Initialize()