import datetime
import csv
import tempfile
import os
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from github import Github

from icalendar import Calendar, Event
import recurring_ical_events
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Replace with your GitHub access token
ACCESS_TOKEN = os.getenv('GITHUB_PAT')


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


def next_weekday(date, day):
    days = (day - date.isoweekday() + 7) % 7
    return date + datetime.timedelta(days=days)


@app.route('/submit_calendar', methods=['POST'])
def submit_calendar():
    response = {"status": "success"}
    data = request.get_json()
    print(data)

    
    #[{'id': 1679647593951, 'type': 'Karton', 'isDateSeries': True, 'value': ['Montag'], 'repetition': '0', 'radioGroup': 'days', 'datePicker': '', 'timePicker': ''}]

    now = datetime.datetime.now()
    next_year = now.year + 1
    start_date = datetime.datetime(next_year, 1, 1)
    end_date = datetime.datetime(next_year, 12, 31)


    cal = Calendar()
    for entry in data['entries']:

        if entry['isDateSeries']:
            for weekday in entry['value']:
                event = Event()
                event.add('summary', entry['type'])

                first_date = next_weekday(start_date, weekday)
                event.add('dtstart', first_date)
                event.add(
                    'rrule',
                    {
                        'FREQ': entry['radioGroup'],
                        'INTERVAL': entry['repetition'],
                        'UNTIL': end_date
                    }
                )
                cal.add_component(event)

        else:
            event = Event()
            event.add('summary', entry['type'])
            start_date = datetime.datetime.fromisoformat(event['datePicker'])
            event.add('dtstart', start_date)
            cal.add_component(event)

    print(cal.to_ical().decode("utf-8")) 


    events = recurring_ical_events.of(cal).between(start_date, end_date)
    from pprint import pprint
    pprint(events)

    header = [
        'region',
        'waste_type',
        'col_date',
    ]
    with tempfile.TemporaryFile('w+') as fp:
        writer = csv.DictWriter(fp, fieldnames=header, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for event in events:
            props = {v[0]: v[1] for v in event.property_items()}
            row = {
                'region': data['municipality'],
                'waste_type': props['SUMMARY'],
                'col_date': props['DTSTART'].dt.date().isoformat(),
            }
            print(row)
            writer.writerow(row)
        fp.seek(0)
    

        filename = data['municipality'].replace(' ', '_').replace('.', '').lower()
        repo_path = f"csv/{filename}.csv"

        br_id = str(uuid.uuid4())
        branch = f"{filename}-{br_id}"

        create_branch(branch)
        add_csv_to_branch(branch, fp, repo_path)
        create_pull_request(branch, f"New data for {data['municipality']}", "Please check")

    return jsonify(response)


# function to create new branch (wiring to app still missing)
def create_branch(new_branch_name):

    REPO_NAME = 'BinBuddy'
    OWNER_NAME = 'opendatazurich'

    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

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


# function to add file to branch
def add_csv_to_branch(branch_name, csv_file, repo_path):
    # Replace with the name of your repository and the owner's username
    REPO_NAME = 'BinBuddy'
    OWNER_NAME = 'opendatazurich'

    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the branch object
    branch = repo.get_branch(branch_name)

    # Read the contents of the CSV file
    contents = csv_file.read()
    print(contents)

    # Create the new file in the repository
    repo.create_file(
        path=repo_path,
        message='Add new CSV file',
        content=contents,
        branch=branch_name
    )

    # Print a success message
    print('CSV file added to branch.')

# function to create pull request
def create_pull_request(branch_name, title, description):
    # Replace with the name of your repository and the owner's username
    REPO_NAME = 'BinBuddy'
    OWNER_NAME = 'opendatazurich'
    
    # Authenticate with GitHub using PyGitHub
    g = Github(ACCESS_TOKEN)

    # Get the repository object
    repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

    # Get the main branch object
    main_branch = repo.get_branch(repo.default_branch)

    # Create a new pull request object
    pull_request = repo.create_pull(
        title=title,
        body=description,
        head=branch_name,
        base=main_branch.name
    )

    # Print a success message with the pull request URL
    print(f"Pull request created successfully: {pull_request.html_url}")

if __name__ == '__main__':
    app.run()

