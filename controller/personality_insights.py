from flask import Blueprint, render_template, session,abort
from db import *
import random
import json

app_personalityInsights = Blueprint('app_personalityInsights',__name__)


@app_personalityInsights.route("/personalityInsights", methods=['GET'])
def personalityInsights():
    return render_template('personality_insights.html')