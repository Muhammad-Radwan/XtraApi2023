from flask import Flask, request
import DatabaseRepository as repo

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to Xtra API v1'

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

@app.route('/AddUser', methods=['POST'])
def AddUser():
    response = request.json
    usguide = response['usguide']
    username = response['username']
    password = response['password']

    repo.AddUser(usguide, username, password)
    return response


if(__name__ == '__main__'):
    app.run('0.0.0.0', port=8084)