import requests

# Set up authentication using personal access token
access_token = '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'
headers = {'Authorization': f'token {access_token}'}

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
