# Needs: python -m pip install requests
import requests, secrets
import json
import webbrowser

"""
        *************************MANDATORY ARGUMENTS REQUIRED*********************************
        LINKEDIN_CLIENT_ID
        LINKEDIN_CLIENT_SECRET
        LINKEDIN_REDIRECT_URI
    """
def get_auth_link(LINKEDIN_CLIENT_ID,LINKEDIN_REDIRECT_URI):
    url = requests.Request(
        'GET',
        'https://www.linkedin.com/oauth/v2/authorization?',
        params = {
            'response_type': 'code', # Always should equal to fixed string "code"

            # ClientID of your created application
            'client_id': LINKEDIN_CLIENT_ID,

            # The URI your users are sent back to after authorization.
            # This value must match one of the OAuth 2.0 Authorized Redirect
            # URLs defined in your application configuration.
            # This is basically URL of your server that processes authorized requests like:
            #     https://your.server.com/linkedin_authorized_callback
            'redirect_uri': LINKEDIN_REDIRECT_URI, # Replace this with your value

            # state, any unique non-secret randomly generated string like DCEeFWf45A53sdfKef424
            # that identifies current authorization request on server side.
            # One way of generating such state is by using standard "secrets" module like below.
            # Store generated state string on your server for further identifying this authorization session.
            'state': secrets.token_hex(8).upper(),

            # Requested permissions, below is just example, change them to what you need.
            # List of possible permissions is here:
            #     https://learn.microsoft.com/en-us/linkedin/shared/references/migrations/default-scopes-migration#scope-to-consent-message-mapping
            'scope': ' '.join(['profile', 'email', 'w_member_social']),
        },
    ).prepare().url
    return url
# You may now send this url from server to user
# Or if code runs locally just open browser like below


def get_access_token(url,LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET,LINKEDIN_REDIRECT_URI):
    result = requests.get(url)
    if result.status_code == 200:
        webbrowser.open(url)
    auth_code=''
    access_token = requests.post(
        'https://www.linkedin.com/oauth/v2/accessToken',
        params = {
            'grant_type': 'authorization_code',
            # This is code obtained on previous step by Python script.
            'code': auth_code,
            # This should be same as 'redirect_uri' field value of previous Python script.
            'redirect_uri': LINKEDIN_REDIRECT_URI,
            # Client ID of your created application
            'client_id': LINKEDIN_CLIENT_ID,
            # Client Secret of your created application
            'client_secret': LINKEDIN_CLIENT_SECRET,
        },
    ).json()
    return access_token

def extract_data(access_token):
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
                'Authorization': f'Bearer {access_token}'
            }
    response = requests.request("GET", url, headers=headers)

    webbrowser.open(url, new=0, autoraise=True)
    jsonData = json.loads(response.text)
    print (jsonData)

def execute(LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET,LINKEDIN_REDIRECT_URI):
    """
        *************************MANDATORY ARGUMENTS REQUIRED*********************************
        LINKEDIN_CLIENT_ID
        LINKEDIN_CLIENT_SECRET
        LINKEDIN_REDIRECT_URI
    """
    url=get_auth_link(LINKEDIN_CLIENT_ID,LINKEDIN_REDIRECT_URI)

    access_token=get_access_token(url,LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET,LINKEDIN_REDIRECT_URI)

    extract_data(access_token)

    return

LINKEDIN_CLIENT_ID = ''  # todo - fill this field up
LINKEDIN_CLIENT_SECRET = ''  # todo - fill this field up
LINKEDIN_REDIRECT_URI = ''  # todo - fill this field up

execute(LINKEDIN_CLIENT_ID,LINKEDIN_CLIENT_SECRET,LINKEDIN_REDIRECT_URI)
