from flask import Flask, render_template, request
import DatabaseRepository as repo

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/GeneralGet', methods=['GET'])
def GeneralGet():
    qn = request.args.get('qn')
    return repo.GetData(qn)

@app.route('/GetLedger', methods=['GET'])
def GetLedger():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    account_name = request.args.get('accountname')
    costcenter = request.args.get('cc')
    project = request.args.get('project')
    branch = request.args.get('branch')
    return repo.GetLedger(start_date, finish_date, account_name, costcenter, project, branch)

@app.route('/GetInvoiceHeadByGuide', methods=['Get'])
def GetInvoiceHeadByGuide():
    invoiceGuide = request.args.get('invoiceguide')
    return repo.GetInvoiceHeadByGuide(invoiceGuide)

@app.route('/GetInvoiceHead', methods=['GET'])
def GetInvoiceHead():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    agent_name = request.args.get('agentname')
    return repo.GetInvoiceHead(start_date, finish_date, agent_name)

@app.route('/GetInvoiceDetails', methods=['GET'])
def GetInvoiceDetails():
    invoiceGuide = request.args.get('invoiceguide')
    return repo.GetInvoiceDetails(invoiceGuide)

@app.route('/GetDailyVouchers', methods=['GET'])
def GetDailyVouchers():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    return repo.GetDailyVouchers(start_date, finish_date)

@app.route('/GetVouchersByType', methods=['GET'])
def GetVouchersByType():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    type = request.args.get('type')
    return repo.GetVouchersByType(start_date, finish_date, type)

@app.route('/GetVoucherDetails', methods=['GET'])
def GetVoucherDetails():
    guide = request.args.get('guide')
    return repo.GetVoucherDetails(guide)

@app.route('/GetDailyInvoices', methods=['GET'])
def GetDailyInvoices():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    return repo.GetDailyInvoices(start_date, finish_date)

@app.route('/GetDailyInvoicesByType', methods=['GET'])
def GetDailyInvoicesByType():
    start_date = request.args.get('d1')
    finish_date = request.args.get('d2')
    invoice_type = request.args.get('invoicetype')
    return repo.GetDailyInvoicesByType(start_date, finish_date, invoice_type)

@app.route('/AddUser', methods=['POST'])
def AddUser():
    response = request.json
    usguide = response['usguide']
    username = response['username']
    password = response['password']

    repo.AddUser(usguide, username, password)
    return response

@app.route('/AddReceiptVoucher', methods=['POST'])
def AddReceiptVoucher():
    response = request.json
    cardguide = response['cardguide']
    mainguide = response['mainguide']
    date = response['date']
    currencyguide = response['currencyguide']
    debitaccount = response['debitaccount']
    creditaccount = response['creditaccount']

    value = response['value']
    rate = response['rate']
    notes = response['notes']

    repo.AddReceiptVoucher(cardguide, mainguide, date, currencyguide, debitaccount,
                    creditaccount, value, rate, notes)
    return response

@app.route('/AddPaymentVoucher', methods=['POST'])
def AddPaymentVoucher():
    response = request.json
    cardguide = response['cardguide']
    mainguide = response['mainguide']
    date = response['date']
    currencyguide = response['currencyguide']
    debitaccount = response['debitaccount']
    creditaccount = response['creditaccount']

    value = response['value']
    rate = response['rate']
    notes = response['notes']

    repo.AddPaymentVoucher(cardguide, mainguide, date, currencyguide, debitaccount,
                    creditaccount, value, rate, notes)
    return response


if(__name__ == '__main__'):
    app.run('0.0.0.0', port=8084)