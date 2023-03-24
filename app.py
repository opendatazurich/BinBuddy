from flask import Flask, jsonify, request
from flask_cors import CORS


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/data/waste_types', methods=['GET'])
def get_waste_types():
    waste_types = {
        'bulky_goods': {
            'de': 'Sperrgut',
            'en': 'Bulky goods',
        },
        'cardboard': {
            'de': 'Karton',
            'en': 'Cardboard',
        },
        'cargotram': {
            'de': 'Cargotram',
            'en': 'Cargotram',
        },
        'chipping_service': {
            'de': 'Häkseldienst',
            'en': 'Chipping service',
        },
        'etram': {
            'de': 'eTram',
            'en': 'eTram',
        },
        'incombustibles': {
            'de': 'Unbrennbares',
            'en': 'Incombustibles',
        },
        'metal': {
            'de': 'Metall',
            'en': 'Metal',
        },
        'organic': {
            'de': 'Grüngut',
            'en': 'Organic waste',
        },
        'paper': {
            'de': 'Altpapier',
            'en': 'Paper',
        },
        'special': {
            'de': 'Sondermüll',
            'en': 'Special waste',
        },
        'textile': {
            'de': 'Textilien',
            'en': 'Textiles',
        },
        'waste': {
            'de': 'Abfall',
            'en': 'Waste',
        },
    }
    return jsonify(waste_types)


@app.route('/submit_calendar', methods=['POST'])
def submit_calendar():
    response = {"status": "success"}
    post_data = request.get_json()
    print(post_data)
    return jsonify(response)


# function to create new branch (wiring to app still missing)
def create_branch(github_pat, new_branch_name):

    REPO_NAME = 'BinBuddy'
    OWNER_NAME = 'opendatazurich'

    # Authenticate with GitHub using PyGitHub
    g = Github(github_pat)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the default branch name
    default_branch = repo.default_branch

    # Create a new branch based on the default branch
    new_branch = repo.create_git_ref(
        f"refs/heads/{new_branch_name}",
        repo.get_branch(default_branch).commit.sha
    )

    # Print the URL of the new branch
    print(f"New branch created: {new_branch.url}")

if __name__ == '__main__':
    app.run()

