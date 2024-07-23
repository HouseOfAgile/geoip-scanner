
# Geolocation IP Scanner

This project uses the IPinfo API to fetch geolocation data for a list of IP addresses.

## Setup

1. Clone the repository:

```sh
git clone https://github.com/HouseOfAgile/geoip-scanner.git
cd geoip-scanner
```

2. Install the required packages:

```sh
pip install -r requirements.txt
```

3. Create a `token.txt` file and add your IPinfo access token:

```sh
echo 'your_ipinfo_access_token' > token.txt
```

4. Run the script:

```sh
python geoip_scanner.py --file ip_list.txt
```
or

```sh
python geoip_scanner.py --ip 8.8.8.8
```

## Requirements

- Python 3.x
- `ipinfo` package

## Output

The script outputs the geolocation data to the console and saves it to `geoip_scanner_info.csv`.
