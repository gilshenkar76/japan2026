from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


OUTPUT_PATH = Path("תוכנית קיוטו ונארה - 17-20 בנובמבר 2026.xlsx")
HEADERS = ["שעה", "פעילות", "תחבורה / משך", "חלופה", "פרטים והסבר", "עדיפות"]


DAY_17 = [
    ("07:30-08:10", "ארוחת בוקר ב-Hotel Monterey Kyoto", "-", "-", "ארוחת בוקר רגילה לפני יום ההליכה.", "חיוני"),
    ("08:10-08:45", "המלון אל Nijo Castle", "הליכה, 25 דקות + מרווח הגעה", "2 מוניות רק למי שרוצה לחסוך הליכה", "הליכה היא האפשרות המועדפת.", "מעבר"),
    ("08:45-10:45", "Nijo Castle", "ביקור של שעתיים", "-", "להתמקד ב-Ninomaru Palace ובגנים. Honmaru Palace אינו חלק מהתוכנית. חשוב: לרכוש כרטיסים מראש.", "חובה"),
    ("10:45-11:20", "Nijo Castle אל Nishiki Market", "הליכה, 35 דקות", "-", "להיכנס לשוק מהצד המערבי ולהתקדם מזרחה.", "מעבר"),
    ("11:20-13:00", "Nishiki Market וארוחת טעימות", "הליכה, 100 דקות", "-", "טעימות, שיטוט וקניות כלי מטבח. זו ארוחת הצהריים ולא נשנוש לפני ארוחה נוספת.", "חובה"),
    ("13:00-13:50", "Nishiki Market אל Nanzen-ji", "הליכה + רכבת תחתית, 50 דקות", "Kyoto Shiyakusho-mae אל Keage בקו Tozai", "מהתחנה יש כ-5-10 דקות הליכה למקדש.", "מעבר"),
    ("13:50-15:05", "Nanzen-ji והאקוודוקט", "הליכה, 75 דקות", "-", "לתעדף את המתחם, שער Sanmon והאקוודוקט. להוסיף את Hojo רק אם נשאר זמן.", "מומלץ"),
    ("15:05-16:00", "חזרה למרכז העיר", "הליכה + רכבת תחתית, 55 דקות", "Keage אל Kyoto Shiyakusho-mae", "הקצאה נדיבה כדי להימנע מחיבור צפוף.", "מעבר"),
    ("16:00-17:00", "שיטוט או קפה מאוחר", "הליכה, גמיש", "-", "מרווח הביטחון המרכזי במקרה של עיכוב בארוחה, במקדש או בתחבורה.", "רשות"),
    ("17:00-17:30", "הליכה אל Hulic Hall Kyoto", "הליכה, עד 30 דקות", "-", "Rissei Garden Hulic Kyoto 1F, 310-2 Bizenjima-cho.", "מעבר"),
    ("17:30-18:00", "כניסה והתיישבות באולם", "-", "-", "הדלתות נפתחות 30 דקות לפני המופע. להגיע יחד עם ההזמנה מוכנה.", "חיוני"),
    ("18:00-18:45", "EN - MIYABI drum show", "מופע ישיבה, כ-45 דקות", "-", "מופע 18:00 אומת על ידי המשתמש. חשוב: להזמין שישה כרטיסים.", "מופע מרכזי"),
    ("18:45-19:15", "יציאה והליכה לארוחת ערב", "הליכה, עד 30 דקות", "-", "לבחור מסעדה קרובה; הזמן כולל יציאה מהאולם.", "מעבר"),
    ("19:15-20:45", "ארוחת ערב יפנית", "-", "-", "חשוב: להזמין לשישה במסעדה במרכז העיר לכיוון המלון, ולא ב-Pontocho.", "חיוני"),
    ("אחרי 20:45", "חזרה למלון", "הליכה, כ-15-25 דקות", "-", "משך ההליכה תלוי במסעדה שתיבחר.", "מעבר"),
]

DAY_18 = [
    ("07:30-08:15", "ארוחת בוקר במלון", "-", "-", "ארוחת בוקר רגועה לפני יום הליכה ארוך.", "חיוני"),
    ("08:30-08:50", "המלון אל Mimosa Higashiyama", "2 מוניות, כ-15-20 דקות", "-", "הדרך היעילה ביותר לשישה.", "מעבר"),
    ("09:00-10:30", "הלבשת קימונו", "-", "-", "בחירה, הלבשה ועיצוב שיער אופציונלי. חשוב: להזמין לשישה ולאשר שניתן לטפל בכולם יחד.", "חיוני"),
    ("10:30-11:10", "Ichinenzaka, Yasaka Pagoda, Ninenzaka, Sannenzaka", "הליכה, 40 דקות כולל צילום", "-", "הקטע המרכזי לצילומי קימונו; אין למהר.", "חובה"),
    ("11:10-12:00", "Kiyomizu-dera", "הליכה בעלייה, כ-5-10 דקות", "-", "מקדש מרכזי עם מרפסת עץ ותצפית לעיר.", "חובה"),
    ("12:00-12:30", "Kiyomizu אל Mimosa", "הליכה בירידה, כ-25-30 דקות", "-", "חזרה דרך הרחובות ההיסטוריים עם אפשרויות צילום נוספות.", "מעבר"),
    ("12:30-13:00", "החזרת קימונו והחלפת בגדים", "-", "-", "להחליף לבגדים ולנעלי הליכה נוחות.", "חיוני"),
    ("13:00-14:10", "ארוחת צהריים יפנית", "הליכה, כ-5-10 דקות", "-", "חשוב: להזמין באזור Kodai-ji/Higashiyama כדי לשמור על רצף המסלול.", "חיוני"),
    ("14:10-15:00", "Kodai-ji", "הליכה, כ-5 דקות", "-", "מקדש זן עם גנים מטופחים ואווירה רגועה.", "מומלץ"),
    ("15:00-15:15", "Nene-no-Michi / Ishibei-koji", "הליכה, 15 דקות", "-", "סמטאות שמורות עם אדריכלות קיוטו מסורתית.", "מומלץ"),
    ("15:15-15:30", "הליכה אל Kennin-ji", "הליכה, 15 דקות", "-", "ללכת ישירות כדי להגן על שעת הכניסה האחרונה.", "מעבר"),
    ("15:30-16:25", "Kennin-ji", "-", "-", "מקדש זן חשוב עם גנים, חללים מסורתיים ואמנות.", "מומלץ"),
    ("16:25-16:50", "Hanamikoji", "הליכה רגועה, 25 דקות", "-", "מעבר בלב ההיסטורי של Gion לקראת ערב.", "מומלץ"),
    ("16:50-17:15", "Yasaka Shrine", "הליכה, כ-10-15 דקות", "-", "מקדש שינטו מרכזי באווירת ערב.", "מומלץ"),
    ("17:15-17:45", "Gion Shirakawa", "הליכה ושיטוט, כ-30 דקות", "-", "תעלה, גשרים ובתי machiya בשעת בין ערביים.", "מומלץ"),
    ("17:45-18:00", "Shijo Bridge", "-", "-", "עצירה קצרה על הגשר.", "מומלץ"),
    ("18:00-18:20", "Kamo River", "הליכה רגועה, 20 דקות", "-", "הליכה לכיוון מרכז קיוטו ו-Pontocho.", "מומלץ"),
    ("18:20-19:30", "Pontocho / זמן חופשי", "הליכה מינימלית", "-", "מרווח לקפה, משקה או עיכובים מוקדמים יותר.", "רשות"),
    ("19:30-21:15", "ארוחת ערב ב-Pontocho", "-", "-", "חשוב: להזמין מסעדה יפנית טובה לשישה.", "חיוני"),
    ("אחרי 21:15", "חזרה ל-Hotel Monterey Kyoto", "2 מוניות, כ-10 דקות", "הליכה, כ-20-25 דקות", "אחרי יום הליכה ארוך עדיף לקחת מוניות.", "מעבר"),
]

DAY_19 = [
    ("07:00-07:30", "ארוחת בוקר ב-Hotel Monterey Kyoto", "-", "-", "נוסעי התחבורה הציבורית יוצאים ב-07:30; לנוסעי המוניות יש מעט יותר זמן.", "חיוני"),
    ("07:30-08:40", "המלון אל שביל הבמבוק", "הליכה + רכבת תחתית + Randen, 70 דקות", "2 מוניות: יציאה ב-07:55, כ-45 דקות", "שתי האפשרויות מכוונות להתחלת ביקור זהה. חשוב: להזמין מוניות מראש אם נבחרו.", "מעבר"),
    ("08:40-09:20", "Arashiyama Bamboo Grove", "הליכה, 40 דקות", "-", "ביקור מוקדם וצילום, ללא הבטחה לשבילים ריקים.", "חובה"),
    ("09:20-09:35", "הבמבוק אל Tenryu-ji", "הליכה, 15 דקות", "-", "כניסה דרך השער הצפוני.", "מעבר"),
    ("09:35-10:35", "Tenryu-ji", "הליכה, 60 דקות", "-", "גן נוף, בריכה ומבנים מסורתיים.", "חובה"),
    ("10:35-10:50", "המקדש אל הנהר", "הליכה, 15 דקות", "-", "להמשיך לכיוון הגשר והנהר.", "מעבר"),
    ("10:50-11:20", "Togetsukyo Bridge / גדת הנהר", "הליכה, 30 דקות", "-", "נוף הנהר וההרים.", "חובה"),
    ("11:20-12:00", "Hogon-in garden", "הליכה, 40 דקות כולל גישה", "-", "התחנה הראשונה לקיצור או ביטול במקרה של עיכוב. יש לאשר פתיחת סתיו 2026.", "רשות"),
    ("12:00-12:15", "הליכה לארוחת צהריים", "הליכה, עד 15 דקות", "-", "לבחור מסעדה ליד Randen Arashiyama Station.", "מעבר"),
    ("12:15-13:15", "ארוחת צהריים יפנית", "-", "-", "חשוב: להזמין מראש לשישה. מנוחת הישיבה המרכזית של היום.", "חיוני"),
    ("13:15-14:10", "Arashiyama אל Ryoan-ji", "Randen + הליכה, 55 דקות", "2 מוניות, כ-45 דקות", "Arashiyama אל Katabiranotsuji, החלפה ל-Ryoanji Station והליכה.", "מעבר"),
    ("14:10-14:55", "Ryoan-ji", "ביקור של 45 דקות", "-", "גן הסלעים והמתחם. לבטל במקרה של עיכוב משמעותי כדי להגן על Kinkaku-ji.", "רשות"),
    ("14:55-15:30", "Ryoan-ji אל Kinkaku-ji", "הליכה, 35 דקות", "מונית אם עייפים או מאחרים", "הליכה רגועה או מוניות לפי מצב הקבוצה.", "מעבר"),
    ("15:30-16:30", "Kinkaku-ji - Golden Pavilion", "הליכה, 60 דקות", "-", "הביתן, תצפיות הבריכה ומסלול הגן. יש להגן על הביקור.", "חובה"),
    ("16:30-17:10", "Kinkaku-ji אל Kitano Tenmangu", "הליכה, 40 דקות", "2 מוניות אם עייפים או מאחרים", "המוניות שומרות זמן לתאורה.", "מעבר"),
    ("17:10-18:10", "תאורת גן המייפל ב-Kitano Tenmangu", "הליכה, 60 דקות", "-", "ביקור עונתי אופציונלי. יש לאשר תאריכים ושעות רשמיים ל-2026.", "רשות"),
    ("18:10-19:10", "נסיעה לארוחת ערב", "אוטובוס 55 + הליכה, 60 דקות", "2 מוניות, כ-45 דקות", "לבחור מסעדה ליד המלון.", "מעבר"),
    ("19:30-21:00", "ארוחת ערב יפנית", "-", "-", "חשוב: להזמין לשישה ליד Hotel Monterey Kyoto.", "חיוני"),
    ("אחרי 21:00", "חזרה למלון", "הליכה, לפי מיקום המסעדה", "-", "להביא שכבות חמות לביקור הערב.", "מעבר"),
]

DAY_20 = [
    ("07:00-07:45", "ארוחת בוקר ב-Hotel Monterey Kyoto", "-", "-", "לסיים אריזה מראש כדי שהצ'ק-אאוט לא יתעכב.", "חיוני"),
    ("07:45-08:00", "צ'ק-אאוט", "-", "-", "להסדיר תשלום ומטען. אין להשאיר מזוודות שיחייבו חזרה לקיוטו.", "חיוני"),
    ("08:00-08:50", "המלון אל Fushimi Inari", "הליכה + רכבת תחתית + JR, 50 דקות", "Karasuma Oike אל Kyoto Station ואז JR אל Inari", "לשמור את הקבוצה יחד במהלך ההחלפה בתחנה.", "מעבר"),
    ("08:50-10:20", "Fushimi Inari", "הליכה, 90 דקות", "-", "המקדש הראשי, מנהרות torii ועלייה קצרה. ללא עלייה לפסגה כדי לשמור זמן ואנרגיה ל-Nara.", "חובה"),
    ("10:20-11:35", "Fushimi Inari אל JR Nara Station", "הליכה + רכבת JR ישירה, 75 דקות כולל המתנה", "-", "Miyakoji Rapid משרתת את Inari; יש לבדוק יציאה מדויקת סמוך לנסיעה.", "מעבר"),
    ("11:35-12:00", "התחנה אל אזור ארוחת הצהריים", "אוטובוס מקומי + הליכה קצרה, 25 דקות", "-", "האוטובוס חוסך הליכה מ-JR Nara Station המרוחקת יותר מהפארק.", "מעבר"),
    ("12:00-13:00", "ארוחת צהריים יפנית", "-", "-", "חשוב: להזמין לשישה ליד הפארק או בדרך ל-Todai-ji.", "חיוני"),
    ("13:00-13:30", "Nara Park והאיילים", "הליכה, 30 דקות", "-", "צילום וביקור בפארק לפני המקדש המרכזי.", "חובה"),
    ("13:30-14:45", "Todai-ji: South Gate ו-Great Buddha Hall", "הליכה, 75 דקות", "-", "שער Nandaimon והבודהה הגדול. מחיר כניסה למבוגר: 800 ין; שעות נובמבר 08:00-17:00.", "חובה"),
    ("14:45-15:20", "הליכה בפארק אל Kasuga Taisha", "הליכה, 35 דקות", "-", "נקודת הגמישות העיקרית של אחר הצהריים; להמשיך רק אם הקבוצה מרגישה בנוח.", "מעבר"),
    ("15:20-16:00", "Kasuga Taisha", "ביקור של 40 דקות", "-", "להתמקד בדרך הגישה ובאזור התפילה הכללי; לא להסתמך על הביקור הפנימי בתשלום.", "רשות"),
    ("16:00-16:45", "Kasuga Taisha אל Kintetsu-Nara Station", "הליכה + אוטובוס מקומי, 45 דקות", "-", "החזרה המועדפת לאחר יום ההליכה.", "מעבר"),
    ("16:45-17:10", "שירותים, כרטיסים ומרווח עלייה", "אזור התחנה", "-", "מרווח מכוון ולא שעת רכבת קבועה.", "חיוני"),
    ("17:10-18:25", "Nara אל המלון ב-Osaka", "Kintetsu + רכבת תחתית + הליכה, 75 דקות", "Kintetsu-Nara אל Osaka-Namba, קו Midosuji אל Hommachi", "המלון נמצא כשתי דקות מיציאה 13 של Hommachi Station.", "מעבר"),
    ("18:25-19:15", "צ'ק-אין ב-Osaka Excel Hotel Tokyu", "-", "-", "לאסוף מטען שנשלח אם הגיע, להתרענן ולהתארגן.", "חיוני"),
    ("19:15-20:45", "ארוחת ערב ליד המלון", "הליכה, לפי המסעדה", "-", "חשוב: להזמין בקרבת מקום. אין להוסיף אטרקציה מרכזית באוסקה לאחר יום המעבר.", "חיוני"),
]


def apply_cell_style(cell, horizontal="right"):
    cell.font = Font(name="Arial", size=10)
    cell.alignment = Alignment(horizontal=horizontal, vertical="top", wrap_text=True)
    thin = Side(style="thin", color="D9E2EC")
    cell.border = Border(left=thin, right=thin, top=thin, bottom=thin)


def style_day_sheet(sheet, title, subtitle, rows):
    sheet.sheet_view.rightToLeft = True
    sheet.freeze_panes = "A5"
    sheet.merge_cells("A1:F1")
    sheet["A1"] = title
    sheet["A1"].font = Font(name="Arial", size=18, bold=True, color="FFFFFF")
    sheet["A1"].fill = PatternFill("solid", fgColor="243B53")
    sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
    sheet.row_dimensions[1].height = 32

    sheet.merge_cells("A2:F2")
    sheet["A2"] = subtitle
    sheet["A2"].font = Font(name="Arial", size=11, italic=True, color="334E68")
    sheet["A2"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    sheet.row_dimensions[2].height = 32

    for column, header in enumerate(HEADERS, 1):
        cell = sheet.cell(row=4, column=column, value=header)
        cell.font = Font(name="Arial", bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="007C83")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    priority_fills = {
        "חובה": "D9EAD3",
        "חיוני": "D9EAD3",
        "מופע מרכזי": "D9EAD3",
        "מומלץ": "DDEBF7",
        "רשות": "FFF2CC",
        "מעבר": "F2F2F2",
    }
    for row_number, values in enumerate(rows, 5):
        for column, value in enumerate(values, 1):
            cell = sheet.cell(row=row_number, column=column, value=value)
            apply_cell_style(cell, "center" if column in (1, 6) else "right")
            if column == 6:
                cell.fill = PatternFill("solid", fgColor=priority_fills.get(str(value), "FFFFFF"))
            elif "חשוב:" in str(value):
                cell.fill = PatternFill("solid", fgColor="FFF3BF")
            elif row_number % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F7F9FB")
        sheet.row_dimensions[row_number].height = 48

    for column, width in enumerate([18, 34, 35, 34, 72, 16], 1):
        sheet.column_dimensions[get_column_letter(column)].width = width

    last_row = 4 + len(rows)
    sheet.auto_filter.ref = f"A4:F{last_row}"
    sheet.print_title_rows = "1:4"
    sheet.sheet_properties.pageSetUpPr.fitToPage = True
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.page_setup.fitToHeight = 0


def create_summary(sheet):
    sheet.sheet_view.rightToLeft = True
    sheet.merge_cells("A1:E1")
    sheet["A1"] = "תוכנית קיוטו ונארה - 17-20 בנובמבר 2026"
    sheet["A1"].font = Font(name="Arial", size=20, bold=True, color="FFFFFF")
    sheet["A1"].fill = PatternFill("solid", fgColor="243B53")
    sheet["A1"].alignment = Alignment(horizontal="center", vertical="center")
    sheet.row_dimensions[1].height = 36

    headers = ["תאריך", "נושא היום", "מסלול מרכזי", "הזמנות ואישורים", "גמישות"]
    for column, header in enumerate(headers, 1):
        cell = sheet.cell(row=3, column=column, value=header)
        cell.font = Font(name="Arial", bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="007C83")
        cell.alignment = Alignment(horizontal="center", vertical="center")

    rows = [
        ("17.11", "מרכז קיוטו ומופע MIYABI", "Nijo Castle → Nishiki → Nanzen-ji → MIYABI 18:00", "Nijo/Ninomaru, שישה כרטיסים למופע וארוחת ערב", "קפה/שיטוט 16:00-17:00"),
        ("18.11", "קימונו, Higashiyama ו-Gion", "Mimosa → Kiyomizu → Kodai-ji → Kennin-ji → Gion → Pontocho", "קימונו, צהריים וערב לשישה", "Pontocho 18:20-19:30"),
        ("19.11", "Arashiyama וצפון-מערב קיוטו", "Bamboo → Tenryu-ji → Togetsukyo → Ryoan-ji → Kinkaku-ji → Kitano Tenmangu", "צהריים, ערב ומוניות בוקר אם נבחרו", "Hogon-in, Ryoan-ji והתאורה אופציונליים"),
        ("20.11", "Fushimi Inari, Nara ומעבר ל-Osaka", "Fushimi Inari → Nara Park → Todai-ji → Kasuga Taisha → Osaka", "מטען, צהריים וערב לשישה", "Kasuga Taisha אופציונלי"),
    ]
    for row_number, values in enumerate(rows, 4):
        for column, value in enumerate(values, 1):
            cell = sheet.cell(row=row_number, column=column, value=value)
            apply_cell_style(cell)
            if row_number % 2 == 0:
                cell.fill = PatternFill("solid", fgColor="F5F8FA")
        sheet.row_dimensions[row_number].height = 62

    notes = [
        "הקבוצה: 6 מטיילים. מלון קיוטו: Hotel Monterey Kyoto.",
        "ב-17.11 מופע MIYABI בשעה 18:00 אומת על ידי המשתמש; Honmaru Palace אינו כלול.",
        "ב-19.11 יש לאשר את מועדי הסתיו הרשמיים של Hogon-in ושל Kitano Tenmangu.",
        "ב-20.11 יש לבדוק את רכבת JR מ-Inari ולאשר את העברת המזוודות ל-Osaka Excel Hotel Tokyu.",
        "תאים צהובים מסמנים הזמנות מראש; עמודת העדיפות מציגה מה חובה, מומלץ או רשות.",
    ]
    sheet["A10"] = "הערות תפעוליות"
    sheet["A10"].font = Font(name="Arial", size=13, bold=True, color="243B53")
    for row_number, note in enumerate(notes, 11):
        sheet.merge_cells(start_row=row_number, start_column=1, end_row=row_number, end_column=5)
        cell = sheet.cell(row=row_number, column=1, value=f"• {note}")
        cell.font = Font(name="Arial", size=11)
        cell.alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
        sheet.row_dimensions[row_number].height = 30

    for column, width in enumerate([18, 34, 72, 48, 42], 1):
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

    day_sheets = [
        ("17 קיוטו ומיאבי", "17 בנובמבר - מרכז קיוטו ומופע MIYABI", "Ninomaru Palace, Nishiki Market, Nanzen-ji ומופע בשעה 18:00", DAY_17),
        ("18 קימונו וגיון", "18 בנובמבר - קימונו, Higashiyama ו-Gion", "יום קימונו בבוקר, מקדשים ורחובות היסטוריים עד ארוחת ערב ב-Pontocho", DAY_18),
        ("19 אראשיאמה", "19 בנובמבר - Arashiyama וצפון-מערב קיוטו", "מסלול עם חלופות מונית ותחבורה ציבורית ותחנות אופציונליות", DAY_19),
        ("20 נארה ואוסקה", "20 בנובמבר - Fushimi Inari, Nara ומעבר ל-Osaka", "צ'ק-אאוט מקיוטו, יום ב-Nara וצ'ק-אין ב-Osaka", DAY_20),
    ]
    for sheet_name, title, subtitle, rows in day_sheets:
        sheet = workbook.create_sheet(sheet_name)
        style_day_sheet(sheet, title, subtitle, rows)

    workbook.save(OUTPUT_PATH)


def validate_workbook():
    workbook = load_workbook(OUTPUT_PATH, read_only=True, data_only=True)
    expected = {
        "17 קיוטו ומיאבי": len(DAY_17),
        "18 קימונו וגיון": len(DAY_18),
        "19 אראשיאמה": len(DAY_19),
        "20 נארה ואוסקה": len(DAY_20),
    }
    if workbook.sheetnames != ["סיכום", *expected]:
        raise ValueError(f"Unexpected sheets: {workbook.sheetnames}")
    for sheet_name, row_count in expected.items():
        sheet = workbook[sheet_name]
        actual_rows = sum(1 for row in sheet.iter_rows(min_row=5, values_only=True) if any(row))
        if actual_rows != row_count:
            raise ValueError(f"{sheet_name}: expected {row_count} rows, found {actual_rows}")
    if workbook["17 קיוטו ומיאבי"]["A16"].value != "18:00-18:45":
        raise ValueError("MIYABI 18:00 anchor is missing")
    if workbook["20 נארה ואוסקה"]["B8"].value != "Fushimi Inari":
        raise ValueError("Fushimi Inari anchor is missing")
    workbook.close()


if __name__ == "__main__":
    build_workbook()
    validate_workbook()
    print(OUTPUT_PATH.resolve())