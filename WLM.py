import os
import uuid
import traceback
import datetime

import Analizers
import Storage
import Term
from json import dumps
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from werkzeug.routing import BaseConverter, ValidationError
import thread
import TwitterFeeder
from TwitterFeeder import FeedingThread


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

def startStreaming():
    feeder = TwitterFeeder.TwitterFeeder()
    feeder.StartFeeding()



app = Flask(__name__)
app.config.from_object(__name__)
app.url_map.converters['date'] = DateConverter
storage = Storage.Storage()
feeder = FeedingThread()
isAnalizerRunning = False
#analizer = Analizers.Analizers(isAnalizerRunning)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#def runAnalizers():
#    analizer.ProcessUpdates()
#    analizer.GroupProcessedUpdates()

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

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCountry"})

@app.route('/Map/CountCountries')
def by_countries_count():
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
    storageResult = storage.GetGroupAnalyzedUpdatesByCountryCount(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('MapBars.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCountry"})



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

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byState"})

@app.route('/Map/CountStates')
def by_states_count():
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
    storageResult = storage.GetGroupAnalyzedUpdatesByStateCount(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('MapBars.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byState"})

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

    return render_template('Map.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCity"})

@app.route('/Map/CountCity')
def by_cities_count():
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
    storageResult = storage.GetGroupAnalyzedUpdatesByCityCount(startDate,endDate,termId)
    jsonData = dumps(storageResult)

    return render_template('MapBars.html', result = {'jsonData':jsonData, 'terms': terms, 'selectedTerm':termId, 'startDate':startDate, 'endDate':endDate, 'type': "byCity"})

@app.route('/Tweets/Country')
def TweetsByCountry():
    termId = request.args['termId']
    startDate = request.args['startDate']
    endDate = request.args['endDate']
    entity = request.args['entity']
    processedTweets  = storage.getProcessedTweetByCountry(entity,startDate,endDate,termId)
    return render_template('ProcessedTweets.html',tweets= processedTweets)

@app.route('/Tweets/State')
def TweetsByState():
    termId = request.args['termId']
    startDate = request.args['startDate']
    endDate = request.args['endDate']
    entity = request.args['entity']
    processedTweets  = storage.getProcessedTweetByState(entity,startDate,endDate,termId)
    return render_template('ProcessedTweets.html',tweets= processedTweets)

@app.route('/Tweets/City')
def TweetsByCity():
    termId = request.args['termId']
    startDate = request.args['startDate']
    endDate = request.args['endDate']
    entity = request.args['entity']
    processedTweets  = storage.getProcessedTweetByCity(entity,startDate,endDate,termId)
    return render_template('ProcessedTweets.html',tweets= processedTweets)

@app.route('/Utility/StopFeeder')
def StopFeeder():
    feeder.stop()
    return redirect(url_for('terms'))

@app.route('/Utility/StartFeeder')
def StartFeeder():
    try:
        feeder.start()
    except:
        tb = traceback.format_exc()
        print traceback.format_exc()
    return redirect(url_for('terms'))


#@app.route('/Utility/StartAnalizer')
#def StartAnalizer():
#    if isAnalizerRunning == False:
#        thread.start_new_thread(runAnalizers,())
#    return redirect(url_for('terms'))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)

