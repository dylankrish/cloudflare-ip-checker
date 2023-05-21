import requests
import time
import os
checkIPv4 = True
checkIPv6 = True
discordWebhookURL = ''
checkInterval = 60 # in seconds

def checkIPs(ipType):
    # if the file does not exist, then run the code below
    # this is for first run
    if not os.path.exists('cloudflare-' + ipType + '.txt'):
        response = requests.get('https://www.cloudflare.com/' + ipType)
        response.raise_for_status()  # raise exception for non-2xx status codes
        ips = response.text.strip().split('\n')
        # write the data to the file
        with open('cloudflare-' + ipType + '.txt', 'w') as f:
            f.write('\n'.join(ips))
    # compare the data in the file with the data from the API to see if there are any changes
    else:
        # read the data from the file
        with open('cloudflare-' + ipType + '.txt', 'r') as f:
            beforeips = f.read().strip().split('\n')
        # get the data from the API
        response = requests.get('https://www.cloudflare.com/' + ipType)
        response.raise_for_status()
        afterips = response.text.strip().split('\n')
        # compare the data
        if beforeips != afterips:
            # find the difference between the two lists
            diff = list(set(beforeips) - set(afterips))
            # print that there is a difference
            print('There is a difference in the Cloudflare ' + ipType + ' list.')
            # check to see if the difference is an addition or a removal
            if len(diff) > 0:
                print('The following IPs have been removed from the Cloudflare ' + ipType + ' list:')
                print(', '.join(diff))
                # send a discord notification
                sendDiscordNotification(', '.join(diff), '-')
            else:
                diff = list(set(afterips) - set(beforeips))
                print('The following IPs have been added to the Cloudflare ' + ipType + ' list:')
                print(', '.join(diff))
                # send a discord notification
                sendDiscordNotification(', '.join(diff), '+')
            # update the file with the new data
            with open('cloudflare-' + ipType + '.txt', 'w') as f:
                f.write('\n'.join(afterips))
        else:
            print('No difference in the Cloudflare ' + ipType + ' list.')


def sendDiscordNotification(newips, type):
    import datetime
    # timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    # send a discord notification
    data = {
        "username" : "Cloudflare IP Change Notifier",
    }
    if type == '-':
        title = "**A Cloudflare IP removal has been detected.**"
    elif type == '+':
        title = "**A Cloudflare IP addition has been detected.**"
    data["embeds"] = [
        {
            "title" : title,
            "description" : "**" + newips + "**\n\n" + str(timestamp),
            # orange cloudflare color
            "color" : 0xFFA500
        }
    ]
    requests.post(discordWebhookURL, data=data)

def main():
    while True:
        if checkIPv4:
            checkIPs('ips-v4')
        if checkIPv6:
            checkIPs('ips-v6')
        time.sleep(checkInterval)
    
if __name__ == '__main__':
    main()