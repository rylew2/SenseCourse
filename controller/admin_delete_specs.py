from flask import Blueprint
from db import *

app_admin_delete_specs = Blueprint('app_admin_delete_specs', __name__)

#################################################################################
# /delete
# Clears specialization and generated classes. Selected as button on admin page
###################################################################################
@app_admin_delete_specs.route("/delete", methods=['GET', 'POST'])
def admin_delete_specs():
    conn = sqlite3.connect(DATABASE)

    cur = conn.cursor()

    cur.execute("UPDATE user SET specialization = NULL,generated_classes=NULL")
    conn.commit()

    return "DONE"