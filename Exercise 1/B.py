# Aggregated by partner code (Partners.Code) and partner borrower Id (Borrowers.PartnerBorrowerId) get:
# Total number of loans (Loans.Id)
# Total amount disbursed (Loans.TotalDisbursementAmount)
# Average loan size (Loans.TotalDisbursementAmount)

from pyodbc import connect
from csv import writer


ENDPOINT = 'testdb.ckv1htjmgn5s.us-east-1.rds.amazonaws.com'
PORT = '1433'
USER = 'test'
PASSWORD = 'SoftDevTest123!'
DATABASE = 'SQL Server'

cnxn = connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + \
    ENDPOINT + ',' + PORT + ';UID=' + USER + ';PWD=' + PASSWORD)
cursor = cnxn.cursor()

cols = ['[Number of loans]', '[Total amount disbursed]', '[Average loan size]']

cursor.execute( \
    "SELECT COUNT(Loan.Id) AS " + cols[0] + \
    ", SUM(Loan.TotalDisbursementAmount) AS " + cols[1] + \
    ", AVG(Loan.TotalDisbursementAmount) AS " + cols[2] + \
    " FROM Partners Part, Borrowers Borr, Loans Loan \
    WHERE Part.Id = Borr.PartnerId AND Borr.PartnerId = Loan.PartnerLoanId \
    GROUP BY Part.Code, Borr.PartnerBorrowerId;")
row = cursor.fetchone()
with open('B.csv', 'w') as output_file:
    write_line = writer(output_file , lineterminator='\n')
    write_line.writerow([col[1:-1] for col in cols])
    while row:
        write_line.writerow(row)
        row = cursor.fetchone()

# Gives the following error:
# pyodbc.ProgrammingError: ('42000', '[42000] [Microsoft][ODBC Driver 17 for \
# SQL Server][SQL Server]Conversion failed when converting from a character \
# string to uniqueidentifier. (8169) (SQLExecDirectW)')

# Comes from WHERE comparisons. Haven't been able to figure it out.