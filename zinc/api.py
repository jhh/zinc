import os
import subprocess
from flask import Blueprint
from flask.wrappers import Response

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/status")
def status():
    zrepl = os.environ["ZREPL"]
    sudo = os.environ["SUDO"]
    try:
        out = subprocess.run(
            [sudo, zrepl, "status", "--mode=raw"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Response(out.stdout, mimetype="application/json")
    except subprocess.CalledProcessError as err:
        return f"{ err }\n{err.stdout}\n{err.stderr}", 500
