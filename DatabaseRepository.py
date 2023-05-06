import pandas
import pyodbc

connString = "Driver={SQL Server}; Server=gh93st\SQLExpress; Database=XtrDB02_05_2023; UID=sa; pwd=123456"
conn = pyodbc.connect(connString)
cursor = conn.cursor()

GetItemsQuery = """select tbl007.cardguide, tbl007.cardcode, productname, tbl006.GroupName,
unit, unit2, factor2, EndUserPrice, EndUserPrice2, StanderCost
from tbl007
inner join tbl006 on tbl007.GroupGuid = tbl006.CardGuide"""

GetAccountsQuery = """select tbl004.CardGuide, tbl004.AccountName, Account.AccountName as MainAccount,
tbl002.ClosingAccountName as ClosingAccount, tbl004.CardCode
from tbl004
inner join tbl002 on tbl004.ClosingAccount = tbl002.CardGuide
inner join tbl004 Account on tbl004.MainAccount = Account.CardGuide
order by accountname asc"""

GetItemsInventoryQuery = """Select	Sum(a.InPut)+Sum(a.InPut2)+Sum(a.InPut3) As Input,
		Sum(a.OutPut)+Sum(a.OutPut2)+Sum(a.OutPut3) As Output,
		sum(a.input-a.output) + sum(a.input2-a.output2) + sum(a.InPut3-a.OutPut3) as general,
        a.ProductGuide,a.ProductName as productname ,a.latinname,a.GroupName as groupname,a.unit as unitname
        From
        (Select (CASE When TBL020.InvoiceMovementSide>0 and tbl023.unit=1 and Posted=1    and TBL023.Quantity <>0    
          Then TBL023.Quantity Else 0 End) As InPut,
                
		(CASE When TBL020.InvoiceMovementSide<0 and tbl023.unit=1 and Posted=1  and TBL023.Quantity <>0    
        Then TBL023.Quantity Else 0 End) As OutPut,
                
		(CASE When TBL020.InvoiceMovementSide>0 and tbl023.unit=2 and Posted=1   and TBL023.Quantity <>0  
        Then TBL023.Quantity*factor2 Else 0 End) As InPut2,
                
		(CASE When TBL020.InvoiceMovementSide<0 and tbl023.unit=2 and Posted=1   and TBL023.Quantity <>0    
        Then TBL023.Quantity*factor2 Else 0 End) As OutPut2,
                
		(CASE When TBL020.InvoiceMovementSide>0 and tbl023.unit=3 and Posted=1   and TBL023.Quantity <>0  
        Then TBL023.Quantity*factor3 Else 0 End) As InPut3,
                
		(CASE When TBL020.InvoiceMovementSide<0 and tbl023.unit=3 and Posted=1   and TBL023.Quantity <>0  
        Then TBL023.Quantity*factor3 Else 0 End) As OutPut3,
          
		TBL023.ProductGuide,
		tbl007.ProductName,
		tbl023.StoreID,
		tbl022.StoreGuide,
		tbl007.CardCode,
		TBL007.GroupGuid,
		tbl007.latinname,
		tbl022.CostCenter,
		tbl006.GroupName,
		tbl007.unit

        From TBL023 left Join TBL022 On TBL023.MainGuide=TBL022.CardGuide
        left Join TBL020 On TBL022.MainGuide=TBL020.CardGuide Left join tbl016 on
        tbl022.AgentGuide=tbl016.CardGuide
        Left Join tbl015 on
        tbl016.MainGroupGuide=tbl015.CardGuide
        left Join tbl007 on
        tbl023.ProductGuide=tbl007.CardGuide
        left join tbl006 on 
        tbl007.GroupGuid=tbl006.CardGuide)a
        where 1=1
		group by a.productguide,a.ProductName,a.CardCode,a.GroupGuid,a.latinname,a.GroupName,a.Unit"""

GetAgentBalanceQuery = f"""select b.AccountName as AgentName, SUM(debit) as Debit, sum(a.credit) as Credit, sum(a.debit - a.Credit) as Balance
from tbl012 a
inner join tbl004 b on b.CardGuide = a.AccountGuide
group by b.AccountName"""

GetSysInfoQuery = "select * from tbl000 where id=1"
GetCostCentersQuery = "select CardGuide, CardCode, CostCenter as CardName from tbl005"
GetItemGroupsQuery = "select CardGuide, CardCode, GroupName as CardName from tbl006"
GetProjectsQuery = "select CardGuide, CardCode, ProjectName as CardName from tbl049"
GetBranchesQuery = "select CardGuide, CardCode, BronchName as CardName from tbl050"

def GetData(query_no):
    query = ''
    match query_no:
        case '0':
            query = GetItemsQuery
        case '1':
            query = GetAccountsQuery
        case '2':
            query = GetItemsInventoryQuery
        case '3':
           query = GetCostCentersQuery
        case '4':
            query = GetItemGroupsQuery
        case '5':
            query = GetProjectsQuery
        case '6':
            query = GetBranchesQuery
        case '7':
            query = GetSysInfoQuery
        case '8':
            query = GetAgentBalanceQuery
    df = pandas.read_sql(query, conn)
    json = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return(json)

def GetLedger(d1, d2, accountname, costcenter, project, branch):
    sql = f"""
    select AccountName, EntryDate, Debit, Credit, CurrencyName, ISNULL(InvoiceName, EntryName) as Source,
    isnull(BillNumber, EntryNumber) as MovementNumber, BillGuide, EntryNote
    from Qry013
    where Posted = 1
    and convert(date,EntryDate) >= '{d1}' and convert(date,EntryDate) <= '{d2}'"""
    
    if accountname != "":
        sql = sql + f" and AccountName = N'{accountname}'"

    if costcenter != "":
        sql = sql + f" and CostCenter = '{costcenter}'"
    
    if project != "":
        sql = sql + f" and Project = '{project}'"

    if branch != "":
        sql = sql + f" and Branch = '{branch}'"

    sql = sql + " order by EntryDate Desc"

    df = pandas.read_sql(sql, conn)
    json = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return(json)

def GetInvoiceHeadByGuide(invoiceguide):
    df = pandas.read_sql(f"""select tbl022.CardGuide, tbl020.InvoiceName, tbl008.WarehouseName, BillDate, PayMethod, tbl001.CurrencyName, BillNumber, tbl022.Rate, 
                        tbl016.AgentName, tbl004.AccountName, tbl013.UserName, sum(tbl023.TotalValue) as BillTotal
                        from tbl022
                        inner join tbl020 on tbl022.MainGuide = tbl020.CardGuide
                        inner join tbl008 on tbl022.StoreGuide = tbl008.CardGuide
                        inner join tbl001 on tbl022.CurrencyGuide = tbl001.CardGuide
                        inner join tbl016 on tbl022.AgentGuide = tbl016.CardGuide
                        inner join tbl004 on tbl022.PostToAccount = tbl004.CardGuide
                        inner join tbl013 on tbl022.ByUser = tbl013.UsGuide
                        inner join tbl023 on tbl023.MainGuide = tbl022.CardGuide
                        where tbl022.CardGuide = '{invoiceguide}'
                        group by tbl022.CardGuide, tbl020.InvoiceName, tbl008.WarehouseName, BillDate, PayMethod, tbl001.CurrencyName, BillNumber, tbl022.Rate, 
                        tbl016.AgentName, tbl004.AccountName, tbl013.UserName
                        order by BillDate""", conn)
    json = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return(json)
    
def GetInvoiceHead(d1, d2, agentName):
    df = pandas.read_sql(f"""select tbl022.CardGuide, tbl020.InvoiceName, tbl008.WarehouseName, BillDate, PayMethod, tbl001.CurrencyName, BillNumber, tbl022.Rate, 
                        tbl016.AgentName, tbl004.AccountName, tbl013.UserName, sum(tbl023.TotalValue) as BillTotal
                        from tbl022
                        inner join tbl020 on tbl022.MainGuide = tbl020.CardGuide
                        inner join tbl008 on tbl022.StoreGuide = tbl008.CardGuide
                        inner join tbl001 on tbl022.CurrencyGuide = tbl001.CardGuide
                        inner join tbl016 on tbl022.AgentGuide = tbl016.CardGuide
                        inner join tbl004 on tbl022.PostToAccount = tbl004.CardGuide
                        inner join tbl013 on tbl022.ByUser = tbl013.UsGuide
                        inner join tbl023 on tbl023.MainGuide = tbl022.CardGuide
                        where tbl016.AgentName like N'{agentName}'
                        and (convert(date,BillDate) >= '{d1}' and convert(date,BillDate) <= '{d2}')
                        group by tbl022.CardGuide, tbl020.InvoiceName, tbl008.WarehouseName, BillDate, PayMethod, tbl001.CurrencyName, BillNumber, tbl022.Rate, 
                        tbl016.AgentName, tbl004.AccountName, tbl013.UserName
                        order by BillDate""", conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return(dfjson)

def GetInvoiceDetails(invoiceGuide):
    df = pandas.read_sql(f"""Select ItemName, UnitName, Quantity, UnitPrice, ItemTotalValue, BillNumber, BillDate, InvoiceGuide, BillTotalValue, BillDate
                        StoreName, PayTerm, CurrencyName, ProjectName, AgentName
                        From Qry101 where InvoiceGuide = '{invoiceGuide}'""", conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return(dfjson)

def GetDailyVouchers(d1, d2):
    df = pandas.read_sql(f"""select c.EntryName, sum(debit) As Debit, sum(credit) as Credit, sum(Debit - Credit) as Balance,
    (select count(tbl010.id) from tbl010 inner join tbl009 on tbl009.CardGuide = tbl010.MainGuide where TBL009.EntryName = c.EntryName)
    as TotalEntries
    from TBL038 a
    inner join tbl010 b on b.CardGuide = a.MainGuide
    inner join tbl009 c on c.CardGuide = b.MainGuide
    where b.DoneIn between CONVERT(date, '{d1}') and CONVERT(date, '{d2}')
    group by c.EntryName""", conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjson

def GetVouchersByType(d1, d2, type):
    df = pandas.read_sql(f"""select a.CardGuide, a.DoneIn, b.CurrencyName, CurrencyShortcut, a.Rate, c.AccountName, d.CostCenter, e.UserName 
    from tbl010 a
    left join tbl001 b on b.CardGuide = a.CurrencyGuide
    left join tbl004 c on c.CardGuide = a.AccountGuide
    left join tbl005 d on d.CardGuide = a.CostCenter
    left join tbl013 e on e.UsGuide = a.ByUser
    where a.DoneIn between CONVERT(date, '{d1}') and CONVERT(date, '{d2}')
    and a.MainGuide = (select CardGuide from tbl009 where EntryName like N'{type}')""", conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjson

def GetVoucherDetails(guide):
    df = pandas.read_sql(f"""select b.AccountName, c.CurrencyName, c.CurrencyShortcut, DebitRate, CreditRate, a.Notes
    from tbl038 a
    inner join tbl004 b on b.CardGuide = a.AccountGuide
    inner join tbl001 c on c.CardGuide = a.CurrencyGuide
    where MainGuide = '{guide}'""", conn)
    dfjson = df.to_json(orient='records', date_format='iso', force_ascii=False)
    return dfjson

def AddUser(UsGuide, UserName, Password):
    cursor.execute(f"""Insert into tbl013(UsGuide, UserName, Password, Security, UserLanguage, ShowInDropDown) 
    Values('{UsGuide}', N'{UserName}', '{Password}', 1, -1, 1)""")
    cursor.commit()

def AddVoucher(cardguide, mainguide, date, currencyguide, debitaccount, creditaccount, value, rate, notes):
    cursor.execute(f"""insert into tbl010(CardGuide, BondNumber, Posted, Security, MainGuide, BondDate, DoneIn, InsertedIn,
    CurrencyGuide, AccountGuide, AccountGuide2, Value, Rate, Notes)
    Values('{cardguide}', (select ISNULL(MAX(bondnumber), 1) from TBL010 where MainGuide = '{mainguide}'), 
    1, 1, '{mainguide}', '{date}', '{date}', '{date}',
    '{currencyguide}', '{debitaccount}', '{creditaccount}', {value}, {rate}, N'{notes}')""")
    cursor.commit()
    #Debit Row
    # cursor.execute(f"""insert into tbl038(MainGuide, AccountGuide, CurrencyGuide, Debit, DebitRate, Credit, CreditRate, Notes)
    # values('{cardguide}', '{debitaccount}', '{currencyguide}', {value}, {value}, 0, 0, N'{notes}')""")
    # cursor.commit()
    #/\/\/\/\/\/\/\/\
    #Credit Row
    cursor.execute(f"""insert into tbl038(MainGuide, AccountGuide, CurrencyGuide, Debit, DebitRate, Credit, CreditRate, Notes)
    values('{cardguide}', '{creditaccount}', '{currencyguide}', 0, 0, {value}, {value}, N'{notes}')""")
    cursor.commit()
    cursor.execute(f"""exec dbo.Prc027 '{cardguide}', 0""")
    cursor.commit()

