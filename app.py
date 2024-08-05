from flask import Flask, request, Response
import requests
import logging
import os


log_dir = r"C:\inetpub\wwwroot\revprox\logs"
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, "app.log"))

logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    handlers = [file_handler]
)

app = Flask(__name__)

SITE_NAME = "http://localhost"
PORT = "4567"

@app.route("/", defaults = {"path": ""})
@app.route("/<path:path>")
def proxy(path):

    user = request.environ.get("REMOTE_USER", None)

    target_url = f"{SITE_NAME}:{PORT}/{path}"

    headers = { key: value for key, value in request.headers if key != "Host"}
    
    if user:
        headers["REMOTE-USER"] = user
        app.logger.debug(f"target url: {target_url}, user: {user}")
    else:
        pass

    app.logger.debug(f"headers: {headers}")

    resp = requests.request(
        method = request.method,
        url = target_url,
        headers = headers,
        data = request.get_data(),
        cookies = request.cookies,
        allow_redirects = False
    )

    response = Response(resp.content, resp.status_code)
    
    for key, value in resp.headers.items():
        response.headers[key] = value

    return response

if __name__ == "__main__":
    app.run()
