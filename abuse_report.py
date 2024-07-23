import argparse
from common_functions import generate_abuse_report


def main(log_file, ip_to_report, email_to_report, name, exclude_resources):
    request_count, begin_datetime, end_datetime, summary_by_date, summary_by_hour, top_requests = generate_abuse_report(
        log_file, ip_to_report, exclude_resources)

    if request_count is None:
        print(f"No requests found for IP {ip_to_report}.")
        return

    print(f"To: {email_to_report}")
    print(f"Subject: Abuse Report for IP: {ip_to_report}")
    print()
    print(f"Dear Nuxt Cloud Team,")
    print()
    print(
        f"I am writing to report abusive behavior from the IP address {ip_to_report}. This IP has made {request_count} requests to our server.")
    print()
    print(f"Between {begin_datetime} and {end_datetime}, we were experiencing abusive behavior from one of your IP addresses.")
    print()
    print(f"Below is the summary of the requests by date and count:")
    print(summary_by_date.to_string(index=False))
    print()
    print(f"Below is the summary of the requests by hour and count:")
    print(summary_by_hour.to_string(index=False))
    print()
    print(f"Here are the top 50 requests sent by this IP:")
    print(top_requests[['datetime', 'method',
          'url', 'status']].to_string(index=False))
    print()
    print(f"Please take appropriate action to prevent further abuse from this IP address.")
    print()
    print(f"Thank you.")
    print()
    print(f"Best regards,")
    print(f"{name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate and display an abuse report for a specific IP.')
    parser.add_argument('--log-file', type=str,
                        required=True, help='Path to the log file.')
    parser.add_argument('--email-to-report', type=str,
                        required=True, help='Email address to report.')
    parser.add_argument('--ip-to-report', type=str,
                        required=True, help='IP address to report.')
    parser.add_argument('--name', type=str, required=True,
                        help='Your name to include in the report.')
    parser.add_argument('--exclude-resources', action='store_true',
                        help='Exclude resource URLs like JS, CSS, images.')
    args = parser.parse_args()

    main(args.log_file, args.ip_to_report, args.email_to_report,
         args.name, args.exclude_resources)
