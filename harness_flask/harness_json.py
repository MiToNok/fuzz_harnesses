import os
import atheris
import sys

with atheris.instrument_imports():
  import flask
  from flask import Flask as _Flask
  from werkzeug.http import parse_set_header


class FuzzFlask(_Flask):
  testing = True
  secret_key = "fuzz test key"

def TestOneInput(data):
  fdp = atheris.FuzzedDataProvider(data)
  app = FuzzFlask("flask_test", root_path=os.path.dirname(__file__))
  app.config["DEBUG"] = True
  app.config["TRAP_BAD_REQUEST_ERRORS"] = False

  @app.route("/json", methods=["POST"])
  def post_json():
    flask.request.get_json()
    return None

  parse_set_header(fdp.ConsumeUnicode(fdp.ConsumeIntInRange(0, 512)))
  
  client = app.test_client()

  try:
    app.add_url_rule(
      fdp.ConsumeUnicode(fdp.ConsumeIntInRange(0, 512)),
      endpoint = "randomendpoint"
    )
  except ValueError:
    None

  try:
    client.post(
      "/json",
      data=fdp.ConsumeUnicode(fdp.ConsumeIntInRange(0, 512)),
      content_type="application/json"
    )
  except (TypeError, UnicodeEncodeError):
    None


def main():
  atheris.Setup(sys.argv, TestOneInput, enable_python_coverage=True)
  atheris.Fuzz()

if __name__ == "__main__":
  main()