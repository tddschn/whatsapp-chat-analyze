#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2024-05-05
Purpose: Analyze Whatsapp Exported _chat.txt
"""

import argparse
from pathlib import Path
from whatsapp_chat_analyze import __version__


def get_args():
    """Get command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Analyze Whatsapp Exported .txt or .zip (will be automatically extracted) chat file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "file",
        type=Path,
        metavar="file",
        help="Chat file (_chat.txt or *.zip) to analyze",
    )

    parser.add_argument(
        "-n",
        "--chat-name",
        help="Name of the chat",
        metavar="name",
        type=str,
        default="Chat",
    )

    parser.add_argument(
        "-o",
        "--output-base-name",
        help="Output base name for the plots",
        metavar="base",
        type=str,
        default="whatsapp-chat",
    )

    # parser.add_argument(
    #     "-p", "--plotly", help="Use Plotly for interactive plots", action="store_true"
    # )

    parser.add_argument(
        "-d", "--by-day-only", help="Plot messages per day only", action="store_true"
    )

    parser.add_argument(
        "-E", "--extract-only", help="Extract the chat and exit", action="store_true"
    )

    parser.add_argument(
        "-c", "--to-csv-only", help="Convert chat to csv and exit", action="store_true"
    )

    parser.add_argument(
        "-a",
        "--anonymize",
        help="Anonymize the chat by replacing author names with generic names",
        action="store_true",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser.parse_args()


def parse_chat(chat_file):
    import re

    DATE_TIME = re.compile(
        r"\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2}\s+[AP]M)\]"
    )
    AUTHOR = re.compile(r"([a-zA-Z ]+?):")
    LTR = chr(8206)  # Left-to-right mark used in text formatting

    data = []
    with open(chat_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.replace(LTR, "")
            dt_match = DATE_TIME.search(line)
            if dt_match:
                date, time = dt_match.groups()
                author_match = re.search(AUTHOR, line)
                if author_match:
                    author = author_match.group(1)
                    message_start = line.find(": ") + 2
                    message = line[message_start:].replace("\n", "").strip()
                    data.append((date, time, author, message))
    return data


def plot_count_plots(
    df,
    output_base_name: str,
    plot_type: str,
    chat_name: str | None = None,
    plotly: bool = False,
):
    title_suffix = " | Made by Teddy (teddysc.me)"
    title_prefix = f"{chat_name} | " if chat_name else ""

    import matplotlib.pyplot as plt

    if plot_type == "message_count":
        print(f'Plotting "{plot_type}"')
        df["Author"].value_counts().plot(kind="bar")
        plt.title(title_prefix + "Message Counts" + title_suffix)
        plt.ylabel("Number of Messages")
        plt.xticks(rotation=45, ha="right")  # Rotate x-labels for better visibility
        plt.tight_layout()  # Adjust layout to prevent labels from being cut off
        plt.savefig(f"{output_base_name}-message-count-by-party.png")
        print(f'Plot saved as "{output_base_name}-message-count-by-party.png"')
        if plotly:
            # save to html
            import plotly.express as px

            fig = px.bar(
                df["Author"].value_counts(),
                title=title_prefix + "Message Counts" + title_suffix,
                labels={"index": "Author", "value": "Number of Messages"},
            )
            fig.write_html(f"{output_base_name}-message-count-by-party.html")
            print(f'Plot saved as "{output_base_name}-message-count-by-party.html"')
    elif plot_type == "char_count":
        print(f'Plotting "{plot_type}"')
        df["Message Length"] = df["Message"].apply(len)
        char_counts = (
            df.groupby("Author")["Message Length"].sum().sort_values(ascending=False)
        )
        char_counts.plot(kind="bar")
        plt.title(title_prefix + "Total Character Counts" + title_suffix)
        plt.ylabel("Total Characters")
        plt.xticks(rotation=45, ha="right")  # Rotate x-labels for better visibility
        plt.tight_layout()  # Adjust layout to prevent labels from being cut off
        plt.savefig(f"{output_base_name}-total-char-count-by-party.png")
        print(f'Plot saved as "{output_base_name}-total-char-count-by-party.png"')
        if plotly:
            # save to html
            import plotly.express as px

            fig = px.bar(
                char_counts,
                title=title_prefix + "Total Character Counts" + title_suffix,
                labels={"index": "Author", "value": "Total Characters"},
            )
            fig.write_html(f"{output_base_name}-total-char-count-by-party.html")
            print(f'Plot saved as "{output_base_name}-total-char-count-by-party.html"')


def plot_by_date(df, output_base_name: str, chat_name: str | None = None):
    print(f'Plotting "Messages per Day" and "Messages per Day by Author"')  # type: ignore
    title_suffix = " | Made by Teddy (teddysc.me)"
    title_prefix = f"{chat_name} |" if chat_name else ""
    import plotly.express as px
    import pandas as pd

    # Ensure the 'Date' column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Generate a Series with counts of messages per day
    message_counts = df["Date"].value_counts().sort_index()

    # Create a date range that covers all days from the minimum to the maximum date
    all_dates = pd.date_range(
        start=message_counts.index.min(), end=message_counts.index.max(), freq="D"
    )

    # Reindex the message_counts Series to include all dates in the range, filling missing values with 0
    message_counts = message_counts.reindex(all_dates, fill_value=0)

    # Create the Plotly figure using the adjusted message counts
    fig = px.bar(
        message_counts.reset_index(),
        x="index",
        y=message_counts.name,
        labels={"index": "Date", message_counts.name: "Messages"},
        title=title_prefix + "Messages per Day" + title_suffix,
    )

    # save html
    fig.write_html(f"{output_base_name}-messages-per-day.html")
    print(f'Plot saved as "{output_base_name}-messages-per-day.html"')

    # Group by Date and Author, then count messages
    grouped_data = df.groupby(["Date", "Author"]).size().reset_index(name="Messages")

    # Pivot the grouped_data DataFrame to get authors in columns, dates as index
    pivot_data = grouped_data.pivot_table(
        index="Date", columns="Author", values="Messages", fill_value=0
    )

    # Reindex the pivot table to include all dates in the range, filling missing values with 0
    pivot_data = (
        pivot_data.reindex(all_dates, fill_value=0).rename_axis("Date").reset_index()
    )

    # Melt the DataFrame back to a long form which is suitable for Plotly
    melted_data = pivot_data.melt(
        id_vars=["Date"], var_name="Author", value_name="Messages"
    )

    # Calculate total messages per day
    total_messages_per_day = melted_data.groupby("Date")["Messages"].sum()

    # Calculate percentage of each author's messages per day
    melted_data["Percentage"] = melted_data.apply(
        lambda row: row["Messages"] / total_messages_per_day[row["Date"]] * 100
        if total_messages_per_day[row["Date"]] > 0
        else 0,
        axis=1,
    )

    # Create a stacked bar chart
    fig = px.bar(
        melted_data,
        x="Date",
        y="Messages",
        color="Author",
        title=title_prefix + "Messages per Day by Author" + title_suffix,
        labels={"Date": "Date", "Messages": "Number of Messages"},
        text_auto=".2s",  # Automatically format text in bars, showing significant figures # type: ignore
        hover_data={
            "Messages": True,  # Show number of messages in hover
            "Percentage": ":.2f%",  # Show percentage with 2 decimal places in hover
            "Date": True,  # Don't repeat the date in hover
        },
    )

    # save html
    fig.write_html(f"{output_base_name}-messages-per-day-by-author.html")
    print(f'Plot saved as "{output_base_name}-messages-per-day-by-author.html"')


def plot_by_date_total_char_count(
    df, output_base_name: str, chat_name: str | None = None
):
    print(
        f'Plotting "Total Character Count per Day" and "Total Character Count per Day by Author"'
    )
    title_suffix = " | Made by Teddy (teddysc.me)"
    title_prefix = f"{chat_name} |" if chat_name else ""
    import plotly.express as px
    import pandas as pd

    # Ensure the 'Date' column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"])

    # Calculate total characters for each message
    df["TotalChars"] = df["Message"].apply(len)

    # Generate a Series with the sum of characters per day
    char_counts = df.groupby("Date")["TotalChars"].sum()

    # Create a date range that covers all days from the minimum to the maximum date
    all_dates = pd.date_range(
        start=char_counts.index.min(), end=char_counts.index.max(), freq="D"
    )

    # Reindex the char_counts Series to include all dates in the range, filling missing values with 0
    char_counts = char_counts.reindex(all_dates, fill_value=0)

    # Create the Plotly figure using the adjusted character counts
    fig = px.bar(
        char_counts.reset_index(),
        x="index",
        y="TotalChars",
        labels={"index": "Date", "TotalChars": "Total Characters"},
        title=title_prefix + "Total Character Count per Day" + title_suffix,
    )

    # save html
    fig.write_html(f"{output_base_name}-total-char-count-per-day.html")
    print(f'Plot saved as "{output_base_name}-total-char-count-per-day.html"')

    # Group by Date and Author, then sum characters
    grouped_data = (
        df.groupby(["Date", "Author"])["TotalChars"]
        .sum()
        .reset_index(name="TotalChars")
    )

    # Pivot the grouped_data DataFrame to get authors in columns, dates as index
    pivot_data = grouped_data.pivot_table(
        index="Date", columns="Author", values="TotalChars", fill_value=0
    )

    # Reindex the pivot table to include all dates in the range, filling missing values with 0
    pivot_data = (
        pivot_data.reindex(all_dates, fill_value=0).rename_axis("Date").reset_index()
    )

    # Melt the DataFrame back to a long form which is suitable for Plotly
    melted_data = pivot_data.melt(
        id_vars=["Date"], var_name="Author", value_name="TotalChars"
    )

    # Calculate total characters per day
    total_chars_per_day = melted_data.groupby("Date")["TotalChars"].sum()

    # Create a stacked bar chart
    fig = px.bar(
        melted_data,
        x="Date",
        y="TotalChars",
        color="Author",
        title=title_prefix + "Total Character Count per Day by Author" + title_suffix,
        labels={"Date": "Date", "TotalChars": "Total Characters"},
        text_auto=True,  # Automatically format text in bars
        hover_data={
            "TotalChars": True,  # Show number of characters in hover
            "Date": True,  # Don't repeat the date in hover
        },
    )

    # save html
    fig.write_html(f"{output_base_name}-total-char-count-per-day-by-author.html")
    print(f'Plot saved as "{output_base_name}-total-char-count-per-day-by-author.html"')


def main():
    args = get_args()
    # surpress warnings
    import warnings

    warnings.filterwarnings("ignore")

    # if args.file.suffix == '.zip', unzip it into a secure temp dir, and find the only .txt file in it, print its path and set it to args.file

    if args.file.suffix == ".zip":
        import zipfile
        import tempfile

        with zipfile.ZipFile(args.file, "r") as zip_ref:
            tmpdir = tempfile.mkdtemp()
            try:
                zip_ref.extractall(tmpdir)
                txt_files = list(Path(tmpdir).rglob("*.txt"))
                if len(txt_files) == 1:
                    txt_file = txt_files[0]
                    print(f"Unzipped file: {txt_file}")
                    args.file = txt_file
                else:
                    raise ValueError(
                        f"Expected 1 .txt file in the zip, found {len(txt_files)}"
                    )
                print(f'Analyzing "{args.file}"')
                if args.extract_only:
                    return

            finally:
                pass

    if args.extract_only:
        print("Input file is not a zip file, nothing to extract. Exiting.")
        return
    import pandas as pd

    data = parse_chat(args.file)
    df = pd.DataFrame(data, columns=["Date", "Time", "Author", "Message"])
    if args.to_csv_only:
        df.to_csv(args.file.with_suffix(".csv"), index=False)
        print(f'Chat saved as "{args.file.with_suffix(".csv")}"')
        return
    if args.anonymize:
        # replace every name with a, b, ... z, aa, ab, ...
        import string

        authors = df["Author"].unique()
        author_map = dict(zip(authors, string.ascii_uppercase))
        df["Author"] = df["Author"].map(author_map)

    # pcp_extra_args = {"plotly": args.plotly}
    pcp_extra_args = {"plotly": True}
    common_args = {}
    if args.chat_name:
        common_args["chat_name"] = args.chat_name
    if not args.by_day_only:
        plot_count_plots(
            df, args.output_base_name, "message_count", **common_args | pcp_extra_args
        )
        plot_count_plots(
            df, args.output_base_name, "char_count", **common_args | pcp_extra_args
        )
    plot_by_date(df, args.output_base_name, **common_args)
    plot_by_date_total_char_count(df, args.output_base_name, **common_args)


if __name__ == "__main__":
    main()
