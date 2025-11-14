from plan import Plan
import xlsxwriter


def gesamtPlan(plan : Plan, workbook: xlsxwriter.Workbook):
    worksheet = workbook.add_worksheet("Gesamtplan")
    bold = workbook.add_format({'bold': True})
    worksheet.write(0,0, 'Klasse', bold)
    worksheet.write(0,1, 'Schüler/Schülerin', bold)
    row = 1
    for s in range(plan.S):
        for t in range(plan.T):
            w = plan.x[s][t]
            wname = plan.workshops[w]+f".{t+1}"
            worksheet.write(row, 0, wname)
            worksheet.write(row, 1, plan.student_data[s]["Name"])
            row += 1
    worksheet.autofit()

def workshopPlan(plan: Plan, w: int, workbook: xlsxwriter.Workbook):
    wname = plan.workshops[w]
    worksheet = workbook.add_worksheet(wname)
    bold = workbook.add_format({'bold': True})
    orderedS = list(range(plan.S))
    orderedS.sort(key=lambda s:plan.student_data[s]["Name"])
    for t in range(plan.T):
        worksheet.write(0, t, f"Zeitslot {t+1}", bold)
    rows = [1 for t in range(plan.T)]
    for s in orderedS:
        for t in range(plan.T):
            if plan.x[s][t]==w:
                worksheet.write(rows[t], t, plan.student_data[s]["Name"])
                rows[t] += 1

    worksheet.autofit()


def exportXLSX(plan:Plan, pfad="zuteilung.xlsx"):
    workbook = xlsxwriter.Workbook(pfad)

    gesamtPlan(plan, workbook)

    for w in range(plan.W):
        workshopPlan(plan, w, workbook)

    workbook.close()