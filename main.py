import requests
import os
checkIPv4 = True
checkIPv6 = False

# First, we need to get the data from the API
# We can use the requests library to do this
# get data from cloudflare.com/ips-v4
ipv4 = 'https://www.cloudflare.com/ips-v4'
ipv6 = 'https://www.cloudflare.com/ips-v6'

if checkIPv4:
    # if the file does not exist, then run the code below
    if not os.path.exists('cloudflare-ipsv4.txt'):
        response = requests.get(ipv4)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        ips = response.text.strip().split('\n')
        # write the data to a file named cloudflare-ipsv4.txt
        with open('cloudflare-ipsv4.txt', 'w') as f:
            f.write('\n'.join(ips))
    # otherwise, compare the data in the file with the data from the API to see if there are any changes
    else:
        # read the data from the file
        with open('cloudflare-ipsv4.txt', 'r') as f:
            beforeips = f.read().strip().split('\n')
        # get the data from the API
        response = requests.get(ipv4)
        response.raise_for_status()
        afterips = response.text.strip().split('\n')
        # compare the data
        if beforeips != afterips:
            # find the difference between the two lists
            diff = list(set(beforeips) - set(afterips))
            # add the difference to the file
            with open('cloudflare-ipsv4.txt', 'a') as f:
                f.write('\n'.join(diff))

if checkIPv6:
    # if the file does not exist, then run the code below
    if not os.path.exists('cloudflare-ipsv6.txt'):
        response = requests.get(ipv6)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        ips = response.text.strip().split('\n')
        # write the data to a file named cloudflare-ipsv6.txt
        with open('cloudflare-ipsv6.txt', 'w') as f:
            f.write('\n'.join(ips))
    # otherwise, compare the data in the file with the data from the API to see if there are any changes
    else:
        # read the data from the file
        with open('cloudflare-ipsv6.txt', 'r') as f:
            beforeips = f.read().strip().split('\n')
        # get the data from the API
        response = requests.get(ipv6)
        response.raise_for_status()
        afterips = response.text.strip().split('\n')
        # compare the data
        if beforeips != afterips:
            # find the difference between the two lists
            diff = list(set(beforeips) - set(afterips))
            # add the difference to the file
            with open('cloudflare-ipsv6.txt', 'a') as f:
                f.write('\n'.join(diff))