import requests
import pandas as pd

# Constants
GITHUB_API_URL = "https://api.github.com"
CITY = "Beijing"
MIN_FOLLOWERS = 500
#Used Github API Token
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_users():
    users = []
    page = 1

    while True:
        response = requests.get(f"{GITHUB_API_URL}/search/users?q=location:{CITY}+followers:>{MIN_FOLLOWERS}&page={page}", headers=headers)
        data = response.json()

        if 'items' not in data or not data['items']:
            break

        for user in data['items']:
            users.append({
                'login': user.get('login'),
                'name': user.get('name', ''),
                'company': (user.get('company', '').strip('@')).upper().strip(),
                'location': user.get('location'),
                'email': user.get('email', ''),
                'hireable': user.get('hireable', ''),
                'bio': user.get('bio', ''),
                'public_repos': user.get('public_repos'),
                'followers': user.get('followers'),
                'following': user.get('following'),
                'created_at': user.get('created_at')
            })

        page += 1

    return users

# Fetch users and save to CSV
users_data = fetch_users()
users_df = pd.DataFrame(users_data)
users_df.to_csv('users.csv', index=False)
