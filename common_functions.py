import pandas as pd
import re
from datetime import datetime


def parse_log_line(line):
    log_patterns = [
        re.compile(
            r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+) "(?P<referrer>[^\"]*)" "(?P<user_agent>[^\"]*)"'
        ),
        re.compile(
            r'(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+) "(?P<referrer>[^\"]*)" "(?P<user_agent>[^\"]*)" \S+ "\S+" "\S+" \S+'
        )
    ]

    for log_pattern in log_patterns:
        match = log_pattern.match(line)
        if match:
            return match.groupdict()
    return None


def filter_resources(df):
    resource_extensions = ['.js', '.css', '.jpg', '.jpeg', '.png',
                           '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf', '.eot']
    resource_pattern = re.compile(r'|'.join(
        [re.escape(ext) for ext in resource_extensions]) + r'$', re.IGNORECASE)
    return df[~df['url'].str.contains(resource_pattern)]


def generate_abuse_report(log_file, ip_to_report, exclude_resources):
    with open(log_file, 'r') as file:
        log_lines = file.readlines()

    logs = [parse_log_line(line) for line in log_lines]
    logs = [log for log in logs if log]

    df = pd.DataFrame(logs)

    if exclude_resources:
        df = filter_resources(df)

    df['datetime'] = pd.to_datetime(
        df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')

    ip_logs = df[df['ip'] == ip_to_report]

    if ip_logs.empty:
        return None, None, None, None, None, None

    request_count = ip_logs.shape[0]
    begin_datetime = ip_logs['datetime'].min()
    end_datetime = ip_logs['datetime'].max()
    summary_by_date = ip_logs.groupby(
        ip_logs['datetime'].dt.date).size().reset_index(name='count')
    summary_by_hour = ip_logs.groupby(
        ip_logs['datetime'].dt.hour).size().reset_index(name='count')

    # Top 50 requests, we should add parameter
    top_requests = ip_logs.head(50)

    return request_count, begin_datetime, end_datetime, summary_by_date, summary_by_hour, top_requests
