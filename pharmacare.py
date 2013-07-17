# Pharmacare Drug Cost/Coverage Calculator
# Written by Henry Liang
# Last updated 16/7/2013

# Import modules and define functions

import xlrd
import glob
import datetime
from urllib import urlretrieve
from os import remove

def locate_LCARow(DIN):

    for i in range(LCABook.nrows):
        if float(DIN) == LCABook.cell_value(i, 1):
            return i
            break


def locate_RDPRow(DIN):

    for i in range(RDPBook.nrows):
        if float(DIN) == RDPBook.cell_value(i, 1):
            return i
            break


def locate_LCAPrice(DIN):

    cur_row = drug_LCARow
    drug_LCAPrice = LCABook.cell_value(cur_row, 12)
    if drug_LCAPrice == "":
        drug_LCAPrice = LCABook.cell_value(cur_row, 11)
    return drug_LCAPrice

def display(a, b, c, d):

    print '-' * 20
    print '\nResults:\n'
    print "The eligible cost for Pharmacare coverage is $%.3f" % a,
    print "based\non the maximum eligible $%.3f dispensing fee." % b
    print "\nPharmacare will pay $%.3f towards this transaction." % c
    print "\nPatient pays $%.3f.\n" % d

# Define RDP Prices and possible yes/no answers

yes = set(['yes', 'y', 'ye', 'Yes', 'Ye', 'Y'])
nope = set(['no', 'n', 'No', 'N'])

drug_RDPPrice_table = {
    'Ace Inhibitors ': 28.206,
    'Dihdropyridines': 24.777,
    'H2 Antagonists ': 11.028,
    'NSAIDs         ': 8.748,
    'Oral Nitrates  ': 11.112,
    }

# Sets the xls file names
cur_date = datetime.date.today().strftime("%B%Y")

LCAWorkbookFN = 'books\\lca-current%s.xls' % cur_date
RDPWorkBookFN = 'books\\rdp-current%s.xls' % cur_date

# Checks each xls file and deletes files from previous dates
local_xls_files = glob.glob("books\\*.xls")
for i in local_xls_files:
    if i != LCAWorkbookFN and i != RDPWorkbookFN:
        remove(i)

# Gets xls files from health.gov.bc.ca
# urlretrieve won't replace a file if one with the same name exists
urlretrieve('http://www.health.gov.bc.ca/pharmacare/lca/lca-current.xls',
    LCAWorkbookFN)
urlretrieve('http://www.health.gov.bc.ca/pharmacare/lca/rdp-current.xls',
    RDPWorkbookFN)

# Open the xls files and establishes the sheet to work with
LCAWorkbook = xlrd.open_workbook(LCAWorkbookFN)
RDPWorkBook = xlrd.open_workbook(RDPWorkBookFN)
LCABook = LCAWorkbook.sheet_by_index(0)
RDPBook = RDPWorkBook.sheet_by_index(0)

# ---------- Begin Program ----------

print "\nThis program will help calculate Pharmacare coverage."

# Input

# -- Locate the drug and position in LCA Book
print "\nWhat is the DIN of the drug?"
drug_DIN = float(raw_input("> "))

drug_LCARow = locate_LCARow(drug_DIN)
drug_name = LCABook.cell_value((drug_LCARow), 3)
drug_genname = LCABook.cell_value((drug_LCARow), 2)

print "\nThe drug is %s (%s)" % (drug_name, drug_genname)

# -- Quantity Patient is Receiving
print "\nHow many tablets (in total) is the patient receiving?"
drug_quantity = int(raw_input("> "))

# -- LCA price
drug_LCAPrice = locate_LCAPrice(drug_DIN)

# -- Reference Drug Program
RDP_status = LCABook.cell_value((drug_LCARow), 7)

if RDP_status == 'RDP':

    # -- If drug is in RDP, check price based on drug class
    drug_RDPRow = locate_RDPRow(drug_DIN)
    drug_RDPClass = str(RDPBook.cell_value((drug_RDPRow), 0))

    drug_RDPPrice = drug_RDPPrice_table[drug_RDPClass]

    if drug_RDPPrice == "":
        print 'Error: RDP Price not defined at this point'

    # -- Check days supply
    print "\nHow many days does this prescription supply?"
    days_supply = int(raw_input("> "))

# -- Actual Acquisition Cost (AAC)
print "\nWhat is the Actual Acquisition Cost (AAC) of the drug?"
AAC = float(raw_input("> $"))

# -- Dispensing Fee
print "\nWhat is the pharmacy's dispensing fee?"
disp_fee = float(raw_input("> $"))

if disp_fee >= 10.50:
    pcare_elig_disp_fee = 10.50
else:
    pcare_elig_disp_fee = disp_fee

# -- Deductible Status
print "\nHas the deductible been reached? (yes/no)"
deduc_status = raw_input("> ")

if deduc_status in nope:
    elig_coeff = 0.00
else:
    # -- Elder Status
    print "\nIn which year was the patient born?"
    pt_birthyear = raw_input("> ")

    if pt_birthyear < 1939:
        elig_coeff = 0.75
    else:
        elig_coeff = 0.70

    # -- Family Maximum Status
    print "\nHas the family maximum been reached? (yes/no)"
    fammax_status = raw_input("> ")
    if fammax_status in yes:
        elig_coeff = 1.00

# Math

if RDP_status == 'RDP':
    elig_cost = ((drug_RDPPrice * days_supply) / 30) + pcare_elig_disp_fee
else:
    elig_cost = drug_LCAPrice * drug_quantity + pcare_elig_disp_fee

total_pcare = elig_cost * elig_coeff

pt_pays = ((AAC * drug_quantity) + disp_fee) - total_pcare

if pt_pays < 0:
    pt_pays = 0

# -- Display Results

display(elig_cost, pcare_elig_disp_fee, total_pcare, pt_pays)

# -- Change Variable types (you can only write strings)

drug_quantity_str = str(drug_quantity)
elig_cost_str = str(elig_cost)
pcare_elig_str = str(pcare_elig_disp_fee)
total_pcare_str = str(total_pcare)
pt_pays_str = str(pt_pays)
if RDP_status == 'RDP':
    days_supply_str = str(days_supply)
    drug_RDPPrice_str = str(drug_RDPPrice)

# -- Write Results to File

resultfile_name = "%sTABS %s.txt" % (drug_quantity, drug_name)

resultfile = open(resultfile_name, 'w')

resultfile.write(drug_name)
resultfile.write("\n")
resultfile.write(drug_quantity_str) 
resultfile.write(" Tablets\n")
if RDP_status == 'RDP':
    resultfile.write("Prescription for ")
    resultfile.write(days_supply_str)
    resultfile.write(" days at ")
    resultfile.write(drug_RDPPrice_str)
    resultfile.write(" per 30 days")
resultfile.write("\nThe eligible cost for Pharmacare coverage is ")
resultfile.write(elig_cost_str)
resultfile.write(" based\non the maximum eligible")
resultfile.write(pcare_elig_str)
resultfile.write("dispensing fee.\n\nPharmacare will pay ")
resultfile.write(total_pcare_str)
resultfile.write(" towards this transaction.\n\nPatient pays ")
resultfile.write(pt_pays_str)
resultfile.write(".\n\n<3")

resultfile.close()

# Display Result Filename

print '-' * 20
print '\nResults have been written to ',
print '%sTABS %s.txt' % (drug_quantity, drug_name)
print "\n<3\n"
