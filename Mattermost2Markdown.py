"""
project:    Mattermost2Markdown
author:     Simon Eller
license:    MIT
repo:       https://github.com/simon-eller/Mattermost2Markdown
"""

import requests, json, os, time, datetime

def mattermost_channel_content_to_markdown(url, token, channel_id, output_folder):
    """
    This function exports every message including attachments of a given Mattermost channel.

    Args:
        url: the url of your Mattermost server API
        token: your personal API session token
        channel_id: the id of the channel you want to export
        output_folder: the path to store the final Markdown file and attachments
    """

    headers = {
        "Authorization": "Bearer " + token
    }

    # array of known users to translate usernames into real names
    known_users = {}

    # create the chat.md Markdown file in the given folder
    output_file = output_folder + "/chat.md"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # open the Markdown file to write into it
    with open(output_file, 'w', encoding='utf-8') as f:
        page = 0        # variable to store current page
        per_page = 50   # here ou could change the page size (count of messages in one API call)
        while True:
            # get messages from API
            response = requests.get(f"{url}/channels/{channel_id}/posts?page={page}&per_page={per_page}", headers=headers)
            posts = json.loads(response.text)   # convert into json format

            # break if there are no more messages in API response
            if not posts["order"]:
                break

            # a new entry for every message in the Markdown file; the correct order of posts is stored in a list
            for post_id in posts["order"]:
                # encapsulate the array for the current message
                post = posts["posts"][post_id]

                # convert UNIX timestamp into datetime format
                post_time = datetime.datetime.utcfromtimestamp(int(post['create_at'])/1000)
                # shift from UTC to CET -> change hours to achieve different timezone
                post_time_timezonecorrected = (post_time + datetime.timedelta(hours=1)).strftime('%d.%m.%Y %H:%M:%S')

                # if id of the user of current message is not assigned already to a real name
                if post['user_id'] not in known_users:
                    # get user information
                    response = requests.get(f"{url}/users/{post['user_id']}", headers=headers)
                    user = json.loads(response.text)
                    known_users[post['user_id']] = user["first_name"] + " " + user['last_name']

                # write message to Markdown
                f.write(f"**{known_users[post['user_id']]}** ({post_time_timezonecorrected}):\n")
                f.write(post['message'] + '\n')

                # download attachments
                if 'files' in post["metadata"]:
                    for file_info in post['metadata']["files"]:
                        file_id = file_info['id']
                        file_url = f"{url}/files/{file_id}"
                        file_extension = file_info['extension']
                        file_name = file_id + "." + file_extension
                        file_path = output_folder + "/" + file_name

                        image_extensions = ["jpg","jpeg","png","gif","heic","heif","tiff","webp"]

                        try:
                            # download attachment and save it to given folder
                            response = requests.get(file_url, headers=headers, stream=True)
                            with open(file_path, 'wb') as out_file:
                                for chunk in response.iter_content(1024):
                                    out_file.write(chunk)

                            # if the file is an image then embed it into the Markdown file with correct syntax
                            if file_extension in image_extensions:
                                f.write(f"![{file_name}]({file_name})\n")

                            # if file is not an image then link it into the Markdown file
                            else:
                                f.write(f"[{file_name}]({file_name})")

                        except requests.exceptions.RequestException as e:
                            print(f"Error while downloading {file_url}: {e}")

                f.write("\n\n")     # line break
            page += 1               # next page
            time.sleep(1)           # a little break to not overcharge the server

# INSERT YOUR DATA HERE
mattermost_server   = "https://<url to your Mattermost server>/api/v4"
session_token       = "<your personal session token>"
channels            = ["<id of channel 1>","<id of channel 2>"]

# download every channel of the list channels
for channel in channels:
    mattermost_channel_content_to_markdown(mattermost_server, session_token, channel, channel)