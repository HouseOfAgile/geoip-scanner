
import ipinfo
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Fetch IP geolocation data.')
parser.add_argument('--file', type=str,
                    help='File containing a list of IP addresses.')
parser.add_argument('--ip', type=str, help='Single IP address.')
args = parser.parse_args()

with open('token.txt', 'r') as file:
    access_token = file.read().strip()

handler = ipinfo.getHandler(access_token)

ip_addresses = []

if args.file:
    with open(args.file, 'r') as f:
        ip_addresses = [line.strip() for line in f.readlines()]

if args.ip:
    ip_addresses.append(args.ip)

ip_info = []
for ip in ip_addresses:
    details = handler.getDetails(ip)
    ip_info.append({
        "IP": ip,
        "City": details.city,
        "Region": details.region,
        "Country": details.country_name,
        "Latitude": details.latitude,
        "Longitude": details.longitude
    })

ip_info_df = pd.DataFrame(ip_info)

print(ip_info_df)

ip_info_df.to_csv('geoip_scanner_info.csv', index=False)
