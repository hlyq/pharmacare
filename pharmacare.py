# Pharmacare Drug Cost/Coverage Calculator
# Written by Henry Liang
# Last updated 25/5/2013

print "\nThis program will help calculate Pharmacare coverage."

# Define Possible Yes/No Answers

yes = set(['yes', 'y', 'ye', 'Yes', 'Ye', 'Y'])
nope = set(['no', 'n', 'No', 'N'])

# Input

# -- Drug Name
print "\nWhat is the drug name and strength?"
drug_name = raw_input("> ")

# -- Quantity Patient is Receiving
print "\nHow many tablets (in total) is the patient receiving?"
drug_quantity = int(raw_input("> "))

# -- LCA price
print "\nWhat is the LCA price of the drug?"
LCA_price = float(raw_input("> $"))

# -- Reference Drug Program
print "\nIs %s in the Reference Drug Program? (yes/no)" % drug_name
RDP_status = raw_input("> ")

if RDP_status in yes:

    print "\nIs %s a Reference Drug? (yes/no)" % drug_name
    refdrug_status = raw_input("> ")

    if refdrug_status in nope:

        print "\nWhat is the price for 30 days?"
        RDP_price = float(raw_input("> "))

        print "\nHow many days is this prescription for?"
        days_supply = float(raw_input("> "))

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
    print "\nWas the patient born prior to 1939? (yes/no)"
    pt_iselderly = raw_input("> ")

    if pt_iselderly in yes:
        elig_coeff = 0.75
    else:
        elig_coeff = 0.70

    # -- Family Maximum Status
    print "\nHas the family maximum been reached? (yes/no)"
    fammax_status = raw_input("> ")
    if fammax_status in yes:
        elig_coeff = 1.00

# Final Calculation

if RDP_status in yes and refdrug_status in nope:
    elig_cost = ((RDP_price * days_supply) / 30) + pcare_elig_disp_fee
else:
    elig_cost = LCA_price * drug_quantity + pcare_elig_disp_fee

total_pcare = elig_cost * elig_coeff
pt_pays = ((AAC * drug_quantity) + disp_fee) - total_pcare

if pt_pays < 0:
    pt_pays = 0

# Display Results

def display(a, b, c, d):
    print '-' * 20
    print '\nResults:\n'
    print "The eligible cost for Pharmacare coverage is $%.3f" % a,
    print "based\non the maximum eligible $%.3f dispensing fee." % b

    print "\nPharmacare will pay $%.3f towards this transaction." % c

    print "\nPatient pays $%.3f.\n" % d

display(elig_cost, pcare_elig_disp_fee, total_pcare, pt_pays)

# Change Variable types (you can only write strings)

drug_quantity_str = str(drug_quantity)
elig_cost_str = str(elig_cost)
pcare_elig_str = str(pcare_elig_disp_fee)
total_pcare_str = str(total_pcare)
pt_pays_str = str(pt_pays)
if refdrug_status in nope:
    days_supply_str = str(days_supply)
    RDP_price_str = str(RDP_price)

# Write Results to File

resultfile_name = "%sTABS %s.txt" % (drug_quantity, drug_name)

resultfile = open(resultfile_name, 'w')

resultfile.write(drug_name)
resultfile.write("\n")
resultfile.write(drug_quantity_str)
resultfile.write(" Tablets\n")
if RDP_status in yes and refdrug_status in nope:
    resultfile.write("Prescription for ")
    resultfile.write(days_supply_str)
    resultfile.write(" days at ")
    resultfile.write(RDP_price_str)
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
