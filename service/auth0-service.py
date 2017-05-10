import json
import os

from flask import Flask, request
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

domain = os.environ["DOMAIN"]
non_interactive_client_id = os.environ["NON_INTERACTIVE_CLIENT_ID"]
non_interactive_client_secret = os.environ["NON_INTERACTIVE_CLIENT_SECRET"]

app = Flask(__name__)


def _auth0():
    get_token = GetToken(domain)
    token = get_token.client_credentials(non_interactive_client_id, non_interactive_client_secret, 'https://%s/api/v2/' % domain)
    mgmt_api_token = token['access_token']
    return Auth0(domain, mgmt_api_token)


@app.route('/users', methods=['GET'])
def get():
    since = request.args.get('since')
    batch_size = request.args.get('batch_size', 100)
    if since:
        q = "updated_at:{%s TO *}" % since
    else:
        q = None
    auth0 = _auth0()
    entities = []
    # TODO use streaming

    results = auth0.users.list(search_engine="v2", sort="updated_at:1", q=q, per_page=batch_size)
    for user in results["users"]:
        entity = {"_id": user["user_id"]}
        entity["_updated"] = user["updated_at"]
        for key, value in user.items():
            entity[key] = value
        entities.append(entity)
    return json.dumps(entities)


@app.route('/users', methods=['POST'])
def post():
    entities = request.get_json()
    if isinstance(entities, dict):
        entities = [entities]

    auth0 = _auth0()

    for entity in entities:
        if entity.get("_id", None) is not None:
            # we have the auth0 id, so this allows us to delete and also update the email, phonenumber or username in case they changed for some reason
            id = entity["_id"]
            if entity.get("_deleted", False):
                auth0.users.delete(id)
            else:
                filtered_entity = {k: v for k, v in entity.items() if not k.startswith('_')}
                auth0.users.update(id, filtered_entity)
        else:
            # no _id, so we'll create the user, the user will not be created but updated if the email, phonenumber or username (depends on the connection) exists
            filtered_entity = {k: v for k, v in entity.items() if not k.startswith('_')}
            auth0.users.create(filtered_entity)
    return "Done!"


if __name__ == '__main__':
    app.run(threaded=False, debug=True, host='0.0.0.0')
