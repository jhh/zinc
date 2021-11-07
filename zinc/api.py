import os
import subprocess
from flask import Blueprint
from flask.wrappers import Response

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/status")
def status():
    zrepl = os.environ["ZREPL"]
    try:
        out = subprocess.run(
            ["sudo", zrepl, "status", "--mode=raw"],
            check=True,
            capture_output=True,
            text=True,
        )
        return Response(out.stdout, mimetype="application/json")
    except subprocess.CalledProcessError as err:
        print(f"stdout={err.stdout}\nstderr={err.stderr}")
        return None
