"""
SecureBank APT Detection Engine — MySQL Database Viewer
========================================================
Utility to inspect events and alerts stored by server.py.

Run:  python db_viewer.py
      python db_viewer.py --table events
      python db_viewer.py --table alerts --limit 10
"""

import argparse
import os

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", "#akshita@148"),
    "database": os.environ.get("MYSQL_DATABASE", "securebank"),
}


def print_table(title, headers, rows):
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")
    if not rows:
        print("  (no rows)")
        return
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell) if cell is not None else ""))
    fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_widths)
    print(fmt.format(*headers))
    print("  " + "-" * (sum(col_widths) + 2 * (len(headers) - 1)))
    for row in rows:
        print(fmt.format(*[str(c) if c is not None else "" for c in row]))


def view_events(limit):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, received_at, machine_name, client_ip, username, device, "
        "event_date, event_hour, event_minute "
        "FROM events ORDER BY received_at DESC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print_table(
        f"EVENTS (last {limit})",
        ["ID", "Received", "Machine", "IP", "User", "Device", "Date", "Hr", "Min"],
        rows,
    )
    return len(rows)


def view_alerts(limit):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, created_at, machine_name, username, score, verdict, details "
        "FROM alerts ORDER BY created_at DESC LIMIT %s",
        (limit,),
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    print_table(
        f"ALERTS (last {limit})",
        ["ID", "Created", "Machine", "User", "Score", "Verdict", "Details"],
        rows,
    )
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description="SecureBank MySQL database viewer")
    parser.add_argument(
        "--table",
        choices=["events", "alerts", "all"],
        default="all",
        help="Which table to display (default: all)",
    )
    parser.add_argument("--limit", type=int, default=20, help="Max rows to show (default: 20)")
    args = parser.parse_args()

    try:
        if args.table in ("events", "all"):
            view_events(args.limit)
        if args.table in ("alerts", "all"):
            view_alerts(args.limit)
    except Error as e:
        print(f"\nDatabase error: {e}")
        print("Make sure MySQL is running and set the correct password in db_viewer.py")
        print("or via the MYSQL_PASSWORD environment variable.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
