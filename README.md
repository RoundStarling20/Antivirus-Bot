A Bot created by me to help with bots spamming free Nitro links

This bot utilizes the VirusTotal API to scan link sent in the discord server.

I have added a URL Database of commonly sent URL's.
When a message is sent in a discord channel, the bot checks to see if the message has a url in it. It then checks this URL against the databse of commonly sent URL's
and pre-approved URL's before utilizing the API.

If a message contains a URL flagged as malicious, it will remove all roles from the member and give them a muted role.
