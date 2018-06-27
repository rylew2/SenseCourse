from flask import Blueprint, render_template, session, abort, logging
import json
from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3



testwatson = Blueprint('app_testwatson',__name__)

@app_testwatson.route("/register", methods = ['GET'])
def testwatson():
    personality_insights = PersonalityInsightsV3(
        version='2016-10-20',
        username='9b99a405-7a49-43c5-8d0f-060a97569845',
        password='3zN4alZSTs13')

    with open(join(dirname(__file__), '../resources/personality-v3.json')) as \
            profile_json:
        profile = personality_insights.profile(
            profile_json.read(), content_type='application/json',
            raw_scores=True, consumption_preferences=True)

    logging.warning(json.dumps(profile, indent=2) )


    return render_template('testwatson.html')
