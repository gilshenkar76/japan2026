from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


OUTPUT_PATH = Path("תוכנית קיוטו - 17-19 בנובמבר 2026.xlsx")
HEADERS = ["שעה", "סוג", "אמצעי", "תחנה או פעילות", "פרטים"]

DAY_17_COMMON = [
    ("07:00–07:30", "אוכל", "—", "ארוחת בוקר במלון", "ארוחה קלה"),
    ("07:30–08:00", "מעבר", "רכבת", "אל Fushimi Inari Taisha", "יציאה לפני עיקר העומס"),
    ("08:00–09:30", "ביקור", "רגלי", "Fushimi Inari Taisha", "המקדש הראשי, שערי Senbon Torii ועלייה חלקית לכיוון Yotsutsuji"),
    ("09:30–09:50", "מעבר", "JR ורגלי", "אל Tofuku-ji", "תחנת רכבת אחת והליכה"),
    ("09:50–11:35", "ביקור", "רגלי", "Tofuku-ji", "גשר Tsutenkyo, שלכת וגני Hojo"),
    ("11:35–12:00", "מעבר", "Keihan ורגלי", "אל Sanjusangendo", "רכבת ל־Shichijo והליכה"),
    ("12:00–12:50", "ביקור", "רגלי", "Sanjusangendo", "האולם הארוך ו־1,001 פסלי Kannon"),
]

DAY_17_NO_SHOW = DAY_17_COMMON + [
    ("12:50–13:15", "מעבר", "הליכה או אוטובוס", "אל אזור תחנת קיוטו", "כ־20–25 דקות ברגל; אוטובוס אם עייפים"),
    ("13:15–14:25", "אוכל", "—", "ארוחת צהריים באזור תחנת קיוטו", "סובה, טמפורה או אוכל יפני; חשוב: להזמין לשישה"),
    ("14:25–14:45", "מעבר", "רגלי", "אל To-ji", "עדיף לבחור מסעדה בצד הדרומי של התחנה"),
    ("14:45–15:40", "ביקור", "רגלי", "To-ji", "הפגודה, אולמות Kondo ו־Kodo ובית האוצר"),
    ("15:40–16:15", "מעבר", "רכבת", "אל Nishiki Market", "Kintetsu לתחנת קיוטו, רכבת תחתית ל־Shijo והליכה"),
    ("16:15–17:20", "אוכל ושוק", "רגלי", "Nishiki Market", "ביקור ממוקד עם 4–5 טעימות; להתחיל בחנויות החשובות"),
    ("17:20–18:45", "שיטוט וקניות", "רגלי", "Teramachi ו־Shinkyogoku", "רחובות מקורים, תה, סכינים, מלאכת יד ומזכרות"),
    ("18:45–19:20", "הפסקה", "—", "קפה או משקה", "מנוחה במרכז העיר"),
    ("19:20–20:00", "שיטוט ערב", "רגלי", "נהר Kamo ו־Pontocho", "הליכה רגועה ואווירת ערב"),
    ("20:00–21:45", "אוכל", "—", "ארוחת ערב יפנית", "Obanzai או izakaya באזור Pontocho/Kawaramachi; חשוב: להזמין לשישה"),
    ("21:45 ואילך", "ערב", "רגלי, רכבת או מונית", "משקה או חזרה למלון", "החלטה לפי רמת העייפות"),
]

DAY_17_GEAR = DAY_17_COMMON + [
    ("12:50–13:10", "מעבר", "מונית", "אל ART COMPLEX 1928", "מונית עדיפה כדי להגן על שעת המופע"),
    ("13:10–13:40", "אוכל", "—", "ארוחת צהריים מהירה", "סובה או מסעדה מהירה באזור Sanjo; חשוב: להזמין מראש"),
    ("13:40–14:00", "התארגנות", "רגלי", "כניסה ל־GEAR Kyoto", "להגיע למושב לפחות חמש דקות לפני ההתחלה"),
    ("14:00–15:30", "מופע", "—", "GEAR Kyoto", "מופע חזותי ללא דיבור; חשוב: להזמין כרטיסים לשישה"),
    ("15:30–15:40", "מעבר", "רגלי", "אל Nishiki Market", "הליכה קצרה"),
    ("15:40–16:50", "אוכל ושוק", "רגלי", "Nishiki Market", "להתחיל בחנויות החשובות לפני הסגירה"),
    ("16:50–17:45", "שיטוט וקניות", "רגלי", "Teramachi ו־Shinkyogoku", "שיטוט ממוקד ברחובות המקורים"),
    ("17:45–18:20", "מעבר", "מונית או רכבת", "אל To-ji", "מונית נוחה יותר לקבוצה של שישה"),
    ("18:20–19:40", "ביקור לילה", "רגלי", "To-ji והשלכת המוארת", "תאורת סתיו וביקור לילי ב־Kondo וב־Kodo; בית האוצר ופנים הפגודה סגורים בלילה"),
    ("19:40–20:00", "מעבר", "מונית", "אל אזור תחנת קיוטו", "נסיעה קצרה"),
    ("20:00–21:30", "אוכל", "—", "ארוחת ערב יפנית", "Obanzai, טמפורה או izakaya; חשוב: להזמין לשישה"),
    ("21:30 ואילך", "חזרה", "רכבת או מונית", "למלון", "לפי רמת העייפות"),
]

DAY_18 = [
    ("07:30–08:00", "אוכל", "—", "ארוחת בוקר במלון", "ארוחה קלה לפני היציאה"),
    ("08:00–08:55", "מעבר", "הליכה ורכבת", "אל Arashiyama", "הליכה ל־Hankyu Karasuma, החלפה ב־Katsura והליכה דרך Togetsukyo"),
    ("09:00–09:40", "ביקור", "רגלי", "Arashiyama Bamboo Grove", "ביקור עצמאי לפני הפגישה עם המדריך"),
    ("09:40–09:45", "מעבר", "רגלי", "אל השער הראשי של Tenryu-ji", "נקודת המפגש עם המדריך"),
    ("09:45–10:50", "סיור מודרך", "רגלי", "Tenryu-ji", "מקדש וגנים; חשוב: להזמין מדריך"),
    ("10:50–11:15", "שיטוט", "רגלי", "Arashiyama", "הליכה רגועה באזור"),
    ("11:15–12:15", "אוכל", "—", "ארוחת צהריים", "טופו או yuba; חשוב: להזמין לשישה"),
    ("12:15–12:55", "מעבר", "Randen ורגלי", "אל Ryoan-ji", "החלפה ב־Katabiranotsuji והליכה מתחנת Ryoanji"),
    ("12:55–13:35", "ביקור", "רגלי", "Ryoan-ji", "גן הסלעים והמקדש"),
    ("13:35–13:55", "מעבר", "רגלי", "אל Kinkaku-ji", "כ־20 דקות הליכה"),
    ("13:55–14:40", "ביקור", "רגלי", "Kinkaku-ji", "הביתן המוזהב ומסלול הגן"),
    ("14:40–15:10", "מעבר", "אוטובוס או מונית", "אל Nijo Castle", "אוטובוס מ־Kinkakuji-michi; מוניות כחלופה"),
    ("15:10–16:30", "ביקור", "רגלי", "Nijo Castle", "Ninomaru Palace והגנים; כניסה אחרונה לארמון ב־16:00"),
    ("16:30–17:00", "מעבר", "רכבת תחתית ורגלי", "אל Higashiyama", "קו Tozai מ־Nijojo-mae והליכה"),
    ("17:00–18:15", "שיטוט ערב", "רגלי", "Yasaka, Hanamikoji ו־Gion Shirakawa", "סיור ערב בשכונות ההיסטוריות"),
    ("18:30–20:30", "אוכל", "—", "ארוחת ערב ב־Gion", "Kappo או obanzai; חשוב: להזמין לשישה"),
    ("20:30–21:00", "חזרה", "מונית או רכבת", "למלון", "סיום היום המודרך"),
]

DAY_19 = [
    ("07:30–08:10", "אוכל", "—", "ארוחת בוקר במלון", "יש לאשר את שעות ארוחת הבוקר במלון"),
    ("08:15–08:30", "מעבר", "שתי מוניות", "אל Mimosa Higashiyama", "יציאה בזמן לקראת ההלבשה"),
    ("08:30–10:00", "קימונו", "—", "Mimosa Higashiyama", "בחירה, הלבשה ועיצוב שיער; חשוב: להזמין לשישה ולאשר קיבולת"),
    ("10:00–10:40", "שיטוט וצילום", "רגלי", "Ichinenzaka, Yasaka Pagoda ו־Ninenzaka", "הליכה איטית בקימונו ועצירות צילום"),
    ("10:40–10:55", "מעבר", "רגלי", "Sannenzaka", "עלייה מתונה לכיוון המקדש"),
    ("10:55–11:50", "ביקור", "רגלי", "Kiyomizu-dera", "המקדש והתצפית בלבוש קימונו"),
    ("11:50–12:20", "חזרה", "רגלי", "אל Mimosa Higashiyama", "ירידה זהירה דרך הרחובות ההיסטוריים"),
    ("12:20–12:50", "החלפה", "—", "החזרת הקימונו", "החלפה לבגדים ולנעליים רגילים"),
    ("12:50–13:00", "מעבר", "רגלי", "אל המסעדה", "מסעדה באזור Higashiyama/Gion"),
    ("13:00–14:15", "אוכל", "—", "ארוחת צהריים", "אוכל יפני מקומי; חשוב: להזמין לשישה"),
    ("14:15–14:25", "מעבר", "רגלי", "אל Kodai-ji", "הליכה קצרה"),
    ("14:25–15:20", "ביקור", "רגלי", "Kodai-ji", "האולמות, הגנים, המדרון וחורשת הבמבוק"),
    ("15:20–15:32", "שיטוט", "רגלי", "Ishibei-koji", "סמטה היסטורית בדרך צפונה"),
    ("15:32–15:45", "מעבר", "רגלי", "דרך Hanamikoji אל Kennin-ji", "להגיע לפני סגירת הקבלה"),
    ("15:45–16:35", "ביקור", "רגלי", "Kennin-ji", "מקדש הזן; הקבלה נסגרת ב־16:30"),
    ("16:35–17:05", "שיטוט", "רגלי", "Gion Shirakawa", "תעלה, בתי machiya וגשרים"),
    ("17:05–17:30", "ביקור", "רגלי", "Yasaka Shrine", "ביקור קצר לקראת הערב"),
    ("17:30–19:10", "שיטוט ערב", "רגלי", "Shijo, נהר Kamo ו־Pontocho", "הליכה רגועה, קפה או משקה"),
    ("19:10–19:30", "התארגנות", "רגלי", "אל המסעדה", "איתור המסעדה והגעה בזמן"),
    ("19:30–21:15", "אוכל", "—", "ארוחת ערב ב־Pontocho", "מסעדה יפנית אותנטית; חשוב: להזמין לשישה"),
    ("21:15–21:35", "חזרה", "מונית או רכבת", "למלון", "סיום שלושת ימי קיוטו"),
]


def style_sheet(sheet, title, subtitle, rows):
    sheet.sheet_view.rightToLeft = True
    sheet.freeze_panes = "A5"
    sheet.merge_cells("A1:E1")
    sheet["A1"] = title
    sheet["A1"].font = Font(name="Arial", size=18, bold=True, color="FFFFFF")
    sheet["A1"].fill = PatternFill("solid", fgColor="243B53")
    sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
    sheet.row_dimensions[1].height = 32

    sheet.merge_cells("A2:E2")
    sheet["A2"] = subtitle
    sheet["A2"].font = Font(name="Arial", size=11, italic=True, color="334E68")
    sheet["A2"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    sheet.row_dimensions[2].height = 32

    for column, header in enumerate(HEADERS, 1):
        cell = sheet.cell(row=4, column=column, value=header)
        cell.font = Font(name="Arial", bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="007C83")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    thin = Side(style="thin", color="D9E2EC")
    booking_fill = PatternFill("solid", fgColor="FFF3BF")
    alternate_fill = PatternFill("solid", fgColor="F5F8FA")
    for row_number, values in enumerate(rows, 5):
        for column, value in enumerate(values, 1):
            cell = sheet.cell(row=row_number, column=column, value=value)
            cell.font = Font(name="Arial", size=10)
            cell.alignment = Alignment(
                horizontal="center" if column <= 3 else "right",
                vertical="top",
                wrap_text=True,
            )
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            if "חשוב:" in str(value):
                cell.fill = booking_fill
            elif row_number % 2 == 0:
                cell.fill = alternate_fill
        sheet.row_dimensions[row_number].height = 38

    widths = [18, 18, 22, 34, 66]
    for column, width in enumerate(widths, 1):
        sheet.column_dimensions[get_column_letter(column)].width = width

    last_row = 4 + len(rows)
    sheet.auto_filter.ref = f"A4:E{last_row}"
    sheet.print_title_rows = "1:4"
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0
    sheet.sheet_properties.outlinePr.summaryBelow = True


def create_summary(sheet):
    sheet.sheet_view.rightToLeft = True
    sheet.merge_cells("A1:D1")
    sheet["A1"] = "תוכנית קיוטו — 17–19 בנובמבר 2026"
    sheet["A1"].font = Font(name="Arial", size=20, bold=True, color="FFFFFF")
    sheet["A1"].fill = PatternFill("solid", fgColor="243B53")
    sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
    sheet.row_dimensions[1].height = 36

    summary_headers = ["תאריך", "נושא היום", "מסלול מרכזי", "הזמנות חשובות"]
    for column, header in enumerate(summary_headers, 1):
        cell = sheet.cell(row=3, column=column, value=header)
        cell.font = Font(name="Arial", bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="007C83")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    summary_rows = [
        ("17.11 — אפשרות א׳", "דרום ומרכז קיוטו ללא מופע", "Fushimi Inari → Tofuku-ji → Sanjusangendo → To-ji → Nishiki → Pontocho", "צהריים וערב לשישה"),
        ("17.11 — אפשרות ב׳", "דרום קיוטו, GEAR ו־To-ji בלילה", "Fushimi Inari → Tofuku-ji → Sanjusangendo → GEAR 14:00 → Nishiki → To-ji", "GEAR, צהריים וערב לשישה"),
        ("18.11", "Arashiyama וצפון־מערב קיוטו", "Bamboo Grove → Tenryu-ji → Ryoan-ji → Kinkaku-ji → Nijo → Gion", "מדריך, צהריים וערב לשישה"),
        ("19.11", "קימונו, Higashiyama ו־Gion", "Mimosa → Kiyomizu → Kodai-ji → Kennin-ji → Gion → Pontocho", "קימונו, צהריים וערב לשישה"),
    ]

    thin = Side(style="thin", color="D9E2EC")
    for row_number, values in enumerate(summary_rows, 4):
        for column, value in enumerate(values, 1):
            cell = sheet.cell(row=row_number, column=column, value=value)
            cell.font = Font(name="Arial", size=11)
            cell.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
            cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)
            if row_number % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F5F8FA")
        sheet.row_dimensions[row_number].height = 56

    sheet["A10"] = "הערות"
    sheet["A10"].font = Font(name="Arial", size=13, bold=True, color="243B53")
    notes = [
        "הקבוצה: 6 מטיילים. המלון: Hotel Monterey Kyoto.",
        "ב־17.11 מופע GEAR מתקיים בשעה 14:00 בלבד; פתיחת הדלתות ב־13:30.",
        "תאורת השלכת ב־To-ji פעילה ב־17.11 בין 18:00 ל־21:30; כניסה אחרונה ב־21:00.",
        "תאים צהובים בגיליונות מסמנים פריטים הדורשים הזמנה או אישור מראש.",
    ]
    for row_number, note in enumerate(notes, 11):
        sheet.merge_cells(start_row=row_number, start_column=1, end_row=row_number, end_column=4)
        cell = sheet.cell(row=row_number, column=1, value=f"• {note}")
        cell.font = Font(name="Arial", size=11)
        cell.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
        sheet.row_dimensions[row_number].height = 28

    for column, width in enumerate([22, 34, 76, 38], 1):
        sheet.column_dimensions[get_column_letter(column)].width = width
    sheet.freeze_panes = "A4"
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 1


def build_workbook():
    workbook = Workbook()
    summary = workbook.active
    summary.title = "סיכום"
    create_summary(summary)

    sheets = [
        ("17 ללא מופע", "17 בנובמבר — ללא מופע", "יום מלא בדרום ובמרכז קיוטו, עם ערב רגוע ב־Pontocho", DAY_17_NO_SHOW),
        ("17 עם GEAR", "17 בנובמבר — GEAR ו־To-ji בלילה", "המופע הרשמי מתחיל ב־14:00; תאורת To-ji פתוחה מ־18:00", DAY_17_GEAR),
        ("18 יום מודרך", "18 בנובמבר — Arashiyama וצפון־מערב קיוטו", "יום עם מדריך ב־Tenryu-ji והמשך עצמאי עד Gion", DAY_18),
        ("19 קימונו והיגשיאמה", "19 בנובמבר — קימונו, Higashiyama ו־Gion", "יום קימונו בבוקר והמשך במקדשים וברחובות ההיסטוריים", DAY_19),
    ]
    for sheet_name, title, subtitle, rows in sheets:
        sheet = workbook.create_sheet(sheet_name)
        style_sheet(sheet, title, subtitle, rows)

    workbook.save(OUTPUT_PATH)


def validate_workbook():
    workbook = load_workbook(OUTPUT_PATH, read_only=True, data_only=True)
    expected_sheets = ["סיכום", "17 ללא מופע", "17 עם GEAR", "18 יום מודרך", "19 קימונו והיגשיאמה"]
    if workbook.sheetnames != expected_sheets:
        raise ValueError(f"Unexpected sheets: {workbook.sheetnames}")
    expected_rows = {
        "17 ללא מופע": len(DAY_17_NO_SHOW),
        "17 עם GEAR": len(DAY_17_GEAR),
        "18 יום מודרך": len(DAY_18),
        "19 קימונו והיגשיאמה": len(DAY_19),
    }
    for sheet_name, row_count in expected_rows.items():
        sheet = workbook[sheet_name]
        actual_rows = sum(1 for row in sheet.iter_rows(min_row=5, values_only=True) if any(row))
        if actual_rows != row_count:
            raise ValueError(f"{sheet_name}: expected {row_count} itinerary rows, found {actual_rows}")
    workbook.close()


if __name__ == "__main__":
    build_workbook()
    validate_workbook()
    print(OUTPUT_PATH.resolve())