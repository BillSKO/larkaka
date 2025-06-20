from flask import Flask, request
import os

app = Flask(__name__)

AUTH_DIR = os.path.expanduser('~/NikolaWeb/deriv/oauth/auth/')
TOKEN1_FILE = os.path.join(AUTH_DIR, 'token1.txt')
TOKEN2_FILE = os.path.join(AUTH_DIR, 'token2.txt')

@app.route('/oauth/redirect')
def oauth_redirect():
    token1 = request.args.get('token1')
    token2 = request.args.get('token2')

    # Kontrollera och skapa katalogen om den saknas
    os.makedirs(AUTH_DIR, exist_ok=True)

    if token1 and token2:
        with open(TOKEN1_FILE, 'w') as f:
            f.write(token1)
        with open(TOKEN2_FILE, 'w') as f:
            f.write(token2)

        print("✅ Token1:", token1)
        print("✅ Token2:", token2)
        return '<p style="color:green;">✅ Tokens mottagna och sparade!</p>'
    else:
        print("❌ Inga tokens mottagna!")
        return '<p style="color:red;">❌ Tokens saknas i URL-parametrarna.</p>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
