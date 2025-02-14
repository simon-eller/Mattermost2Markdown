# Mattermost2Markdown
With this simple script it's possible to export direct and group message channels (chats) from Mattermost to single Markdown files.
The attachments will be downloaded as well.

> [!NOTE]  
> This program only works with channels in which your account is a member.
> It may work if your account has admin privileges, but I haven't tried that.

## Requirements
- Python 3.8 or higher
- Mattermost server with enabled API and user account

## Usage
### Session Token
First you need to get your personal session token.

```commandline
curl -i -d '{"login_id":"someone@nowhere.com","password":"thisisabadpassword","token":"mfa-token"}' https://urltoyourmattermostserver.com/api/v4
```

For further information look at the [Mattermost API Reference (4.0.0)](https://api.mattermost.com/#tag/authentication
).

### Channel ID
Then you need to find out the IDs of the channels you want to export.

1. Select the channel from the left sidebar.
2. Select the channel name at the top.
3. Select View Info.
4. Copy the ID of the channel from the right sidebar.

### Export
Now you have everything to begin with the export.

1. Download this program [Mattermost2Markdown.py](https://github.com/simon-eller/Mattermost2Markdown/blob/main/Mattermost2Markdown.py) to your machine with Python installed.
2. Insert the data from the previous chapters after line 99 in the code.
3. Run the program.
   - Now for every ID in the `channels` list a subfolder named like the ID will be created.
   - The attachments will be stored in this folder.
   - Every message will be saved to the file `chat.md` also stored in this folder.

Now you can view your exported file in a Markdown editor.

## Advanced
### Timezone and Time Format
The program converts the timestamps of sent messages to CET (central european timezone). You can change this to meet your timezone by changing the count of hours in the following line.
Here you can also choose a different Time Format. For further information have a look at the [Python strftime cheatsheet](https://strftime.org/).
```python
post_time_timezonecorrected = (post_time + datetime.timedelta(hours=1)).strftime('%d.%m.%Y %H:%M:%S')
```

## Donating

If you like the project, please consider making a small donation.

<a href="https://www.buymeacoffee.com/simoneller" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>