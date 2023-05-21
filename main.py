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
            # check to see if the difference is an addition or a removal
            # print that there is a difference
            print('IP change detected in the' + ipType + ' list:')
            changedIPs = ', '.join(diff)
            print(changedIPs)
            # send a discord notification
            sendDiscordNotification(changedIPs)
            # update the file with the new data
            with open('cloudflare-' + ipType + '.txt', 'w') as f:
                f.write('\n'.join(afterips))
        else:
            print('No difference in the Cloudflare ' + ipType + ' list.')


def sendDiscordNotification(ipchange):
    import datetime
    # timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    # send a discord notification
    data = {
        "username" : "Cloudflare IP Change Notifier",
    }
    data["embeds"] = [
        {
            "title" : "**A Cloudflare IP change has been detected.**",
            "description" : "**" + ipchange + "**\n\n" + str(timestamp),
            # orange cloudflare color
            "color" : 0xFFA500
        }
    ]
    print(requests.post(discordWebhookURL, json=data))

def main():
    while True:
        if checkIPv4:
            checkIPs('ips-v4')
        if checkIPv6:
            checkIPs('ips-v6')
        time.sleep(checkInterval)
    
if __name__ == '__main__':
    main()