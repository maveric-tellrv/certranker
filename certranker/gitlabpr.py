import requests
from config import git_url,git_access_token

from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Personal access token for authentication

access_token = git_access_token
project_id = "51460"
mr_iid = "251"
# headers = 
# git_url = config.git_url

def gitexatract(project_id,mr_iid,headers={"Authorization": f"Bearer {access_token}"}):

# GitLab API endpoint for getting a merge request by project ID and MR IID
    gitlab_url = f"{git_url}{project_id}/merge_requests/{mr_iid}"


# Project ID and MR IID

# Construct the URL with project ID and MR IID
    url = gitlab_url.format(project_id=project_id, mr_iid=mr_iid)

# HTTP headers with the token for authentication


# Make the GET request to retrieve the MR data
    response = requests.get(url, headers=headers,verify=False)

# Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Extract the MR information from the JSON response
        mr_data = response.json()
        # print("Merge Request Title:", mr_data["title"])
        # print("Author:", mr_data["author"]["name"])
        # print("State:", mr_data["state"])
        # print("description",mr_data["description"])
        pr_info = mr_data["title"]+mr_data["description"]
        return pr_info
    # Add more fields as needed
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    # Put your code here that you want to execute when this script is run directly
    print("\n Gitlab Pr info:\n")
    info = gitexatract(project_id,mr_iid)
    print(info)
