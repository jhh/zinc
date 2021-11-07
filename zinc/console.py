from urllib.request import urlopen
from flask import Blueprint
from flask.templating import render_template

from zinc.status import Status

bp = Blueprint("console", __name__)


@bp.route("/")
def index():
    with urlopen("http://ceres.lan.j3ff.io:5000/api/status") as response:
        response_content = response.read()
    status = Status.from_json(response_content)
    return render_template("console.html", status=status)
