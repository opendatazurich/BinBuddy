#Create new branch------------------------------
import requests
from github import Github

# Replace with your GitHub access token
ACCESS_TOKEN = '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'

# Replace with the name of your repository and the owner's username
REPO_NAME = 'BinBuddy'
OWNER_NAME = 'opendatazurich'

# Replace with the name of the new branch you want to create
NEW_BRANCH_NAME = 'test'

# Authenticate with GitHub using PyGitHub
g = Github(ACCESS_TOKEN)

# Get the repository object
repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

# Get the default branch name
default_branch = repo.default_branch

# Create a new branch based on the default branch
new_branch = repo.create_git_ref(
    f"refs/heads/{NEW_BRANCH_NAME}",
    repo.get_branch(default_branch).commit.sha
)

# Print the URL of the new branch
print(f"New branch created: {new_branch.url}")

# -----------------------------------------------------------
# Create pull request

# Define the API endpoint for creating pull requests
api_url = 'https://api.github.com/repos/opendatazurich/BinBuddy/pulls'

# Define the pull request parameters
params = {
    'title': 'Your pull request title',
    'head': 'adrian', # branch where your changes are located
    'base': 'main', # branch where you want to merge your changes
    'body': 'Your pull request description'
}

# Make a POST request to create the pull request
response = requests.post(api_url.format(owner='opendatazurich', repo='BinBuddy'), headers=headers, json=params)

print(response.status_code)
# Check the response status code
if response.status_code == 201:
    print('Pull request created successfully!')
else:
    print('Error creating pull request.')
