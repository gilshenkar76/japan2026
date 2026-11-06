"""Export every itinerary day, time, and attraction from index.html."""
from __future__ import annotations

import csv
import json
import pathlib
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.table import Table, TableStyleInfo


SOURCE = pathlib.Path("index.html")
CSV_OUTPUT = pathlib.Path("trip_itinerary.csv")
XLSX_OUTPUT = pathlib.Path("trip_itinerary.xlsx")
EXPECTED_DAYS = ["12-13", *[str(day) for day in range(14, 29)]]

DAY_PATTERN = re.compile(r"^\s*'(?P<day>12-13|1[4-9]|2[0-8])':\s*\{.*events:\[$")
EVENT_PATTERN = re.compile(
    r'^\s*\[\s*(?P<time>"(?:\\.|[^"\\])*")\s*,\s*'
    r'(?P<attraction>"(?:\\.|[^"\\])*")\s*,'
)


def trip_date(day: str) -> str:
    if day == "12-13":
        return "12-13.11.2026"
    return f"{int(day):02d}.11.2026"


def extract_rows(source: str) -> list[list[str]]:
    data_start = source.index("const data = {")
    data_end = source.index("\nconst transfersByDay", data_start)
    rows: list[list[str]] = []
    current_day: str | None = None
    found_days: list[str] = []

    for line in source[data_start:data_end].splitlines():
        day_match = DAY_PATTERN.match(line)
        if day_match:
            current_day = day_match.group("day")
            found_days.append(current_day)
            continue

        event_match = EVENT_PATTERN.match(line)
        if not event_match or current_day is None:
            continue

        time = json.loads(event_match.group("time")).replace("<br>", " - ")
        attraction = json.loads(event_match.group("attraction"))
        rows.append([current_day, trip_date(current_day), time, attraction])

    if found_days != EXPECTED_DAYS:
        raise ValueError(f"Expected days {EXPECTED_DAYS}, found {found_days}")
    if any(not any(row[0] == day for row in rows) for day in EXPECTED_DAYS):
        raise ValueError("Every trip day must contain at least one event")
    return rows


def write_csv(rows: list[list[str]]) -> None:
    with CSV_OUTPUT.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["Day", "Date", "Time", "Attraction"])
        writer.writerows(rows)


def write_excel(rows: list[list[str]]) -> None:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Trip itinerary"
    sheet.sheet_view.rightToLeft = True
    sheet.append(["Day", "Date", "Time", "Attraction"])
    for row in rows:
        sheet.append(row)

    header_fill = PatternFill("solid", fgColor="1F4E78")
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = Font(color="FFFFFF", bold=True)
        cell.alignment = Alignment(horizontal="center")

    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    sheet.column_dimensions["A"].width = 11
    sheet.column_dimensions["B"].width = 17
    sheet.column_dimensions["C"].width = 22
    sheet.column_dimensions["D"].width = 55
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    table = Table(displayName="TripItinerary", ref=sheet.dimensions)
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    sheet.add_table(table)
    workbook.save(XLSX_OUTPUT)


if __name__ == "__main__":
    itinerary_rows = extract_rows(SOURCE.read_text(encoding="utf-8"))
    write_csv(itinerary_rows)
    write_excel(itinerary_rows)
    print(f"Exported {len(itinerary_rows)} rows across {len(EXPECTED_DAYS)} trip days")
    print(CSV_OUTPUT)
    print(XLSX_OUTPUT)