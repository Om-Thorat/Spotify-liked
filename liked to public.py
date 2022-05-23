from bottle import route, run, request
import spotipy
from spotipy import oauth2

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXX'
SPOTIPY_CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
SPOTIPY_REDIRECT_URI = 'http://localhost:8080/callback'
SCOPE = 'user-library-read playlist-modify-public'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE)

@route('/')
def index():
        return htmlForLoginButton()
@route('/callback')
def shut():
    access_token = ""



    if 3<=1:
        print("Found cached token!")
        #access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        print(results)
        user_id =results["id"]
        playlist_name = "liked public"
        username = "myusername"
        aplaylist = sp.user_playlist_create(user_id ,playlist_name)
        liked = sp.current_user_saved_tracks()
        playlistid = aplaylist["id"]
        def allofu(suck):
            for item in suck['items']:
                track = item['track']
                spotifyid =[item['track']['id']]
                sp.user_playlist_add_tracks(username, playlistid,spotifyid, position=None)
                print(track['name'])

        while liked['next']:
            allofu(liked)
            liked = sp.next(liked)
            pass
        allofu(liked)
        print("done bish")
    else:
        print("fuckyou")

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

run(host='localhost', port=8080)

