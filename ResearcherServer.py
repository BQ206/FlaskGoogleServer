
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO,join_room
import subprocess
import FundingAgency
import Researchers
import University
import uuid

from multiprocessing import Process

import threading
app = Flask(__name__)

socketio = SocketIO(app)
ResearcherIDentifier = 2

INSTANCE_CONNECTION_NAME = f"lively-wave-340915:europe-west1:ca4006database" # i.e demo-project:us-central1:demo-instance
DB_USER = "admin"
DB_PASS = "food"
DB_NAME = "CA4006DB"


class NewCreateAcount(threading.Thread):
    def __init__(self):
        super(NewThreadedTask,self).__init__()
    def run(self):
        Researchers.createTable()
        Researchers.CreateAccount('Name','Email','Password')
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')


class NewCreateTable(threading.Thread):
    def __init__(self):
        super(NewThreadedTask,self).__init__()
    def run(self):
        FundingAgency.createTable()

@app.route('/')
def LandingPage():
    FundingAgency.createTable()
    return render_template('LandingPage.html')

@app.route('/ResearchForm')
def ResearchForm():
    data = {'ResearcherId': ResearcherIDentifier}
    return render_template('ResearchersHTML.html', data=data)

@app.route('/FundingAgency')
def Funding():
    return render_template('FundingAgencyHTML.html')

@app.route('/University')
def Universityfunction():
    return render_template('UniversityHTML.html')

@app.route('/CreateAccount')
def CreateAccountInitial():
    return render_template('CreateAccountHTML.html')

@app.route('/LoginAccount')
def LoginAccountInitial():
    return render_template('LoginAccountHTML.html')

@app.route('/ResearchProposals',methods=['GET', 'POST'])
def ResearchProposals():
    data = {'ResearcherId': ResearcherIDentifier}
    return render_template('ResearcherProposalsHTML.html', data=data)

@socketio.on("onconnect")
def oncconnect():
    UniqueID = str(uuid.uuid4())
    join_room(UniqueID)
    data = {
        "UniqueID" : UniqueID
    }
    socketio.emit('connected',data,room=UniqueID)




@socketio.on("AccountsAdded")
def AccountsAdded(data):
    UniqueID = data['UniqueID']
    ID = data['ID']
    AddedAcountsList = Researchers.getAddedAcounts(ID)
    print(AddedAcountsList)
    i = 0
    while(i < len(AddedAcountsList)):
        print(i)
        title = Researchers.getResearchAccountTitles(AddedAcountsList[i][0])
        data = {
                "Title" : title,
                "AccountID" : AddedAcountsList[i][0],
                "ResearcherId" : AddedAcountsList[i][1]
        }
        i += 1
        socketio.emit('ResearcherProposalTitlesAdd', data,room=UniqueID)


@socketio.on("ListResearchers")
def ListResearchers(data):
    print("fasf")
    ListResearcherslist = Researchers.ListResearchers()
    print(ListResearcherslist)
    i = 0
    UniqueID = data['UniqueID']
    socketio.emit('ClearElementsAccount',room=UniqueID)
    socketio.emit('ResearchSearchBar',room=UniqueID)
    while(i < len(ListResearcherslist)):
        data = {
            "Name" : ListResearcherslist[i][0],
            "ID" : ListResearcherslist[i][1],
            "HolderID" : i + 1
        }
        socketio.emit('ListResearchers', data,room=UniqueID)
        i += 1


@socketio.on("CreateAccount")
def CreateAccount(data):
    print('fsamc')
    Researchers.createTable()
    Researchers.CreateAccount(data['Name'],data['Email'],data['Password'])

@socketio.on("LoginAccount")
def LoginAccount(data):
    print('login')
    UniqueID = data['UniqueID']
    print(data['Password'])
    LoginData = Researchers.LoginAccount(data['EmailName'],data['Password'])
    print('LoginData')
    if(LoginData[0] == True):
        global ResearcherIDentifier
        ResearcherIDentifier = LoginData[1]
        socketio.emit('LoginToAccount',room=UniqueID)

@socketio.on("SubmitProposal")
def message(data):
    print("emitreceived")
    FundingAgency.ProposalSubmited(data['Title'],data['ProjectDescription'],data['FundAmount'],data['ResearcherId'])
    print("emitreceived2")

@socketio.on("SearchForResearcher")
def SearchForResearcher(data):
    print("data['searchString']")
    print(data['searchString'])
    searchList = Researchers.SearchResearchers(data['searchString'])
    print('len(searchList)')
    print(len(searchList))
    UniqueID = data['UniqueID']
    i = 0
    socketio.emit('ClearElementsAccount',room=UniqueID)
    socketio.emit('ResearchSearchBar',room=UniqueID)
    while(i < len(searchList)):
        data = {
            "Name" : searchList[i][0],
            "ID" : searchList[i][1]
        }
        print(searchList[i][0])
        socketio.emit('ListResearchers', data,room=UniqueID)
        i += 1

@socketio.on("AddResearcher")
def AddResearcher(data):
    print("fjsak")
    print(data)
    Researchers.AddResearcher(data['ID'],data['Name'],data['ResearcherAddedID'],data['AccountID'],data['ResearcherID'])


@socketio.on("getProposalsResearcher")
def getProposalsResearcher(data):
    print("fkasl")
    print(data['ResearcherId'])
    UniqueID = data['UniqueID']
    proposalResearcherList = FundingAgency.getProposalsResearchers(data['proposal'],data['ResearcherId'])
    print("fmskm")
    print(proposalResearcherList)
    print(proposalResearcherList)
    Table = data['proposal']
    print(proposalResearcherList)
    i = 0
    UniqueID = data['UniqueID']
    print(Table)
    print(proposalResearcherList)
    if(Table == "AcceptedProposals"):
        print(proposalResearcherList)
        print(len(proposalResearcherList))
        while(i < len(proposalResearcherList)):
            print("fms")
            ProposalTitle = proposalResearcherList[i][0]
            data = {
                "Title" : ProposalTitle,
                "HolderID" : i + 1,
                "ResearcherId" : data['ResearcherId'],
                "Table" : Table
            }
            print("ID")
            print(i + 1)
            socketio.emit('ResearcherProposalTitlesAccept', data,room=UniqueID)
            i += 1
    else:
        while(i < len(proposalResearcherList)):
            ProposalTitle = proposalResearcherList[i][0]
            data = {
                "Title" : ProposalTitle,
                "ID" : i + 1,
                "ResearcherId" : data['ResearcherId'],
                "Table" : Table,
            }
            socketio.emit('ResearcherProposalTitles', data,room=UniqueID)
            i += 1

@socketio.on("ResearchAccountDetails")
def ResearchAccountDetails(data):
    print("qlsm")
    print(data['ID'])
    print(data['HolderID'])
    UniqueID = data['UniqueID']
    accountInfo = FundingAgency.researchAccountInformation(data['ID'],data['HolderID'])
    print(data['ID'])
    print(data['HolderID'])
    print(accountInfo)
    data = {
            "Title" : accountInfo[0][0],
            "Budget" : accountInfo[0][1],
            "EndDate" : accountInfo[0][2],
        }
    socketio.emit('ResearcherDetails', data,room=UniqueID)

@socketio.on("WithdrawFunds")
def WithdrawFunds(data):
    print(data['ID'])
    print(data['HolderID'])
    print(data['Funds'])
    FundingAgency.WithdrawFunds(data['ID'], data['HolderID'], data['Funds'], data['Reason'])

@socketio.on("Transactions")
def Transactions(data):
    print(data)
    UniqueID = data['UniqueID']
    Transactionsall = FundingAgency.Transactions(data['ID'],data['HolderID'])
    i = 0
    socketio.emit('ClearElementsAccount',room=UniqueID)
    while(i < len(Transactionsall)):
        data = {
                "Date" : Transactionsall[i][0],
                "Amount" : Transactionsall[i][1],
                "Reason" : Transactionsall[i][2],
                "TotalAmount" : Transactionsall[i][3],
            }
        socketio.emit('TransactionsShow', data,room=UniqueID)
        i += 1
        print(Transactionsall)

@socketio.on("RemoveResearcherList")
def RemoveResearch(data):
    UniqueID = data['UniqueID']
    ListResearchersRemove = Researchers.ListResearchersRemove(data['HolderAccountID'])
    i = 0
    socketio.emit('ClearElementsAccount',room=UniqueID)
    while(i < len(ListResearchersRemove)):
        print(ListResearchersRemove[i][0])
        data = {
                "Name" : ListResearchersRemove[i][0],
                "ID" : ListResearchersRemove[i][1]
            }
        socketio.emit('ListResearchersRemove', data,room=UniqueID)
        i += 1

@socketio.on("RemoveResearcher")
def RemoveResearcher(data):
    print(data)
    print("fas")
    Researchers.RemoveResearchers(data['ResearcherAddedID'],data['HolderAccountID'])




if __name__ == "__main__":
    socketio.run(app, debug = True,port=5002)
