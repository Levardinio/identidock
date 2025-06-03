from flask import Flask, Response, request
import requests 
import hashlib
import redis

app = Flask(__name__)
# ❌ Было: StirictRedis, prort
# ✅ Стало: StrictRedis, port
cache = redis.StrictRedis(host='redis', port=6379, db=0)

default_name = "Specter Center"
salt = "UNIQUE_SALT_123"  # можно любое слово, главное — стабильное

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    name = default_name
    if request.method == 'POST':
        name = request.form.get('name', default_name)

    salted_name = salt + name
    name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    header = "<html><head><title>Identidock</title></head><body>"
    body = f'''
        <form method="POST">
            Hello <input type="text" name="name" value="{name}">
            <input type="submit" value="submit">
        </form>
        <p>You look like a:
        <img src="/avatar/{name_hash}"/>
    '''
    footer = '</body></html>'

    return header + body + footer

@app.route('/avatar/<name>')
def get_identicon(name):
    image = cache.get(name)
    if image is None:
        print("cache miss", flush=True)
        r = requests.get(f'http://dnmonster:8080/monster/{name}?size=80')
        image = r.content
        cache.set(name, image)

    return Response(image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


