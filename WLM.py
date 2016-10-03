import os
import uuid

import datetime

import Storage
import Term
from json import dumps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.routing import BaseConverter, ValidationError

class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError()

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')

app = Flask(__name__)
app.config.from_object(__name__)
app.url_map.converters['date'] = DateConverter
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

@app.route('/Map/Countries')
def by_countries():
    terms = storage.GetTerms()
    termId = request.args.get('termId')
    if termId is None:
        termId = terms[0].Id
    startDate  = request.args.get('startDate')
    if startDate is None:
        startDate = (datetime.datetime.now().date() - datetime.timedelta(6*365/12))
    endDate = request.args.get('endDate')
    if endDate is None:
        endDate = (datetime.datetime.now().date())
    storageResult = storage.GetGroupAnalyzedUpdatesByCountry(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCountries"})

@app.route('/Map/States')
def by_states():
    terms = storage.GetTerms()
    termId = request.args.get('termId')
    if termId is None:
        termId = terms[0].Id
    startDate  = request.args.get('startDate')
    if startDate is None:
        startDate = (datetime.datetime.now().date() - datetime.timedelta(6*365/12))
    endDate = request.args.get('endDate')
    if endDate is None:
        endDate = (datetime.datetime.now().date())
    storageResult = storage.GetGroupAnalyzedUpdatesByState(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCountries"})

@app.route('/Map/City')
def by_cities():
    terms = storage.GetTerms()
    termId = request.args.get('termId')
    if termId is None:
        termId = terms[0].Id
    startDate  = request.args.get('startDate')
    if startDate is None:
        startDate = (datetime.datetime.now().date() - datetime.timedelta(6*365/12))
    endDate = request.args.get('endDate')
    if endDate is None:
        endDate = (datetime.datetime.now().date())
    storageResult = storage.GetGroupAnalyzedUpdatesByCity(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCountries"})



if __name__ == '__main__':
    app.run()