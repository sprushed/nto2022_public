from flask import Flask, request, render_template_string, render_template
from os import environ

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = environ.get('flag')


@app.route('/', methods=["GET"])
def index():
    # get ip
    if 'X-Forwarded-For' in request.headers:
        proxy_data = request.headers['X-Forwarded-For']
        ip_list = proxy_data.split(',')
        user_ip = ip_list[-1]
        if "{" in ip_list[0]:
            user_ip = "No SSTI on Ryan Gosling fan page"
    else:
        user_ip = request.remote_addr
    rendered_ip = render_template_string(user_ip)
    return render_template("gosling.html", ip=rendered_ip)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
