from flask import Blueprint
from watson_developer_cloud import PersonalityInsightsV3

import credentials
from db import *

app_admin_ibm = Blueprint('app_admin_ibm', __name__)


@app_admin_ibm.route("/app_admin_ibm", methods=['GET', 'POST'])
def admin_ibm():
    log = "<pre>"
    temp_insights = []
    our_insights = {}

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()


    with open('reviews.json') as f:
        data = json.load(f)


    personality_insights = PersonalityInsightsV3(
        version='2016-10-20',
        username= credentials.username,
        password= credentials.password)

    # personality_insights.set_url('https://gateway-fra.watsonplatform.net/personality-insights/api')
    # personalityInsights.set_detailed_response(True)



    for key, value in data.iteritems():

        ## -run personality insight on review on value
        profile = personality_insights.profile( value, content_type="text/plain;charset=utf-8")
        for category in ['needs', 'personality', 'values']:
        # for category in ['needs']:
            for trait in profile[category]:
                temp_insights.append( {trait['name']:trait['percentile']} )

        our_insights[key] = temp_insights
        temp_insights = []

    ## Write all insight results to json file
    with open('insights.json', 'w+') as outfile:
        json.dump(our_insights, outfile, indent=4, sort_keys=True)

    return log






