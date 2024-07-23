import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse
import user_agents
from common_functions import parse_log_line, filter_resources


def save_legend(legend, filename):
    fig_legend = plt.figure(figsize=(10, 2))
    handles, labels = legend.legend_handles, [
        text.get_text() for text in legend.get_texts()]
    fig_legend.legend(handles=handles, labels=labels, loc='center', ncol=2)
    fig_legend.tight_layout()
    fig_legend.savefig(filename)
    plt.close(fig_legend)


def generate_user_agent_plots(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    df['datetime'] = pd.to_datetime(
        df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')
    df['date'] = df['datetime'].dt.date
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    unique_dates = df['date'].unique()

    for date in unique_dates:
        daily_df = df[df['date'] == date]
        user_agents_by_hour_minute = daily_df.groupby(
            ['hour', 'minute', 'user_agent']).size().reset_index(name='count')

        plt.figure(figsize=(14, 8))
        sns.set(style="whitegrid")
        bar_plot = sns.barplot(x='hour', y='count', hue='user_agent',
                               data=user_agents_by_hour_minute, palette='viridis')
        plt.xlabel('Hour and Minute of Day')
        plt.ylabel('Number of Requests')
        plt.title(f'Most Used User Agents by Hour and Minute for {date}')
        plt.xticks(rotation=45)

        legend = plt.legend(title='User Agent')
        save_legend(legend, os.path.join(output_dir, f'legend_{date}.png'))

        legend.remove()

        plt.tight_layout()
        plot_path = os.path.join(
            output_dir, f'user_agents_by_hour_minute_{date}.png')
        plt.savefig(plot_path)
        plt.close()

        summarized_user_agents = user_agents_by_hour_minute.groupby(
            'user_agent')['count'].sum().reset_index().sort_values(by='count', ascending=False)
        summarized_user_agents['browser_family'] = summarized_user_agents['user_agent'].apply(
            lambda x: user_agents.parse(x).browser.family)
        summarized_user_agents['os_family'] = summarized_user_agents['user_agent'].apply(
            lambda x: user_agents.parse(x).os.family)

        print(f'\nSummary for {date}:')
        print(summarized_user_agents[['browser_family', 'os_family', 'count']])

        ip_summary = daily_df['ip'].value_counts().reset_index()
        ip_summary.columns = ['ip', 'count']
        print('\nIP Summary:')
        print(ip_summary)


def main(log_file, output_dir, exclude_resources):
    with open(log_file, 'r') as file:
        log_lines = file.readlines()

    logs = [parse_log_line(line) for line in log_lines]
    logs = [log for log in logs if log]

    df = pd.DataFrame(logs)

    if exclude_resources:
        df = filter_resources(df)

    df['datetime'] = pd.to_datetime(
        df['datetime'], format='%d/%b/%Y:%H:%M:%S %z')

    errors_df = df[(df['status'].astype(int) >= 400) &
                   (df['status'].astype(int) <= 599)]

    most_errors_url = errors_df['url'].value_counts(
    ).idxmax() if not errors_df.empty else 'No errors found'

    print(f'URL with most errors: {most_errors_url}')

    generate_user_agent_plots(df, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analyze Symfony legacy logs.')
    parser.add_argument('--log-file', type=str, required=True,
                        help='Path to the Symfony legacy log file.')
    parser.add_argument('--output-dir', type=str, required=True,
                        help='Directory to save the output PNG files.')
    parser.add_argument('--exclude-resources', action='store_true',
                        help='Exclude resource URLs like JS, CSS, images.')
    args = parser.parse_args()

    main(args.log_file, args.output_dir, args.exclude_resources)
