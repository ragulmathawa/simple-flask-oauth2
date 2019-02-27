from flask import Flask,render_template,redirect,request
from rauth import OAuth2Service
import json
app = Flask(__name__)
googleService = OAuth2Service(
            name='google',
            client_id='<Client id>',
            client_secret='<Client Secret>',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            access_token_url='https://oauth2.googleapis.com/token',
        )
@app.route("/")
def login():
    return render_template('login.html',authUrl=googleService.get_authorize_url(
        scope='email',
        response_type='code',
        redirect_uri=get_redirect_uri()))
@app.route("/callback")
def callback():
    # Success response: https://example.com/callback#code=4/P7q7W91&token_type=Bearer&expires_in=3600
    # Failure Response: https://example.com/callback#error=access_denied

    code = request.args.get('code')
    # check for code in the response query parameter
    # if there is a "code" in query parameter, Authentication success - Allow further access
    # if there is no "code" the Authentication failed - prevent further access
    if code is None:
        return redirect("/failed")
    else:
        # use this token to get any data from the google API
        # Not neccessary just for authentication
        token = googleService.get_access_token(
            data={"code": code,
            'grant_type': 'authorization_code',
                  "redirect_uri": get_redirect_uri()},decoder=new_decoder
        )
        if token is None:
            return redirect("/failed")
        else:
            return redirect("/success")
@app.route("/failed")
def failed():
    return "Failed to Authenticate"
@app.route("/success")
def success():
    return "Sucessfully Authenticated"

def get_redirect_uri():
    return "http://localhost:5000/callback"

    # decoding to utf-8 before json parsing
def new_decoder(payload):
    return json.loads(payload.decode('utf-8'))
