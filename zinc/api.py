import os
import subprocess
from flask import Blueprint
from flask.wrappers import Response

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/status")
def status():
    zrepl = os.environ["ZREPL"]
    out = subprocess.run(
        [zrepl, "status", "--mode=raw"], capture_output=True, text=True
    )
    return Response(out.stdout, mimetype="application/json")
