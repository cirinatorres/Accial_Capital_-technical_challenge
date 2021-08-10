# Aggregated by partner code (Partners.Code) and product code (Products.Code) get:
# Average loan size (Loans.TotalDisbursementAmount)
# Total number of loans (Loans.Id)
# Total amount disbursed (Loans.TotalDisbursementAmount)
# Total number of unique borrowers (Borrowers.Id)

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

cols = ['[Average loan size]', '[Number of loans]', '[Total amount disbursed]', '[Number of borrowers]']

cursor.execute( \
    "SELECT AVG(Loan.TotalDisbursementAmount) AS " + cols[0] + \
    ", COUNT(Loan.Id) AS " + cols[1] + \
    ", SUM(Loan.TotalDisbursementAmount) AS " + cols[2] +  \
    ", COUNT(Borr.Id) AS " + cols[3] + \
    " FROM Partners Part, Products Prod, Loans Loan, Borrowers Borr \
    WHERE Part.Id = Prod.PartnerId AND Prod.Id = Loan.ProductId AND \
    Part.Id = Borr.PartnerId \
    GROUP BY Part.Code, Prod.Code;")

row = cursor.fetchone()
with open('A.csv', 'w') as output_file:
    write_line = writer(output_file , lineterminator='\n')
    write_line.writerow([col[1:-1] for col in cols])
    while row:
        write_line.writerow(row)
        row = cursor.fetchone()

