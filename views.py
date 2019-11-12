from flask import Flask,request,session,redirect,url_for,abort,flash,render_template
#from flask_restful import Resource,Api
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph,Node,Relationship
from flask_cors import CORS
import os

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username='neo4j'
password='alawini'
graph = Graph(url + '/db/data/', username=username, password=password)

class College:
	def __init__(self,name,admissionrate,ist,ost,testtype,score,state):
		self.Name=name
		self.State=state
		self.OST=ost
		self.IST=ist
		self.OAR=admissionrate
		if testtype=="ACT":
			self.ACT=score
		else:
			self.SAT=score

	def find(self):
		query="MATCH (c:College) WHERE c.Name={name} RETURN c"
		
		return graph.run(query,name=self.Name)

	def updateOAR(self,admissionrate):
		query="MATCH (c:College) WHERE c.Name={name} SET c.OAR={admitrate} RETURN c"
		return graph.run(query,name=self.Name,admitrate=admissionrate)
	def updateIST(self,instatetuition):
		query="MATCH (c:College) WHERE c.Name={name}  SET c.IST={tuition} RETURN c"
		return graph.run(query,name=self.Name,tuition=instatetuition)
	def updateOST(self,outstatetuition):
		query="MATCH (c:College) WHERE c.Name={name} SET c.OST={tuition} RETURN c"
		return graph.run(query,name=self.Name,tuition=outstatetuition)
	def updatescore(self,testtype,testscore):
		if testtype=='ACT':
				query="MATCH (c:College) WHERE c.Name={name} SET c.ACT={scores} RETURN c"
				
		else:
			query= "MATCH (c:College) WHERE c.Name={name} SET c.SAT={scores} RETURN c"
		return graph.run(query,name=self.Name,scores=testscore)
	def insert(self,testtype):
		if testtype=="ACT":
			query="CREATE (c:College{Name:{name},OST:{ost},IST:{ist},OAR:{admissionrate},ACT:{score},SAT:{sentinel},State:{location}}) RETURN c "
			scores=self.ACT
		else:
			query="CREATE (c:College{Name:{name},OST:{ost},IST:{ist},OAR:{admissionrate},ACT:{sentinel},SAT:{score},State:{location}}) RETURN c "
			scores=self.SAT

		return graph.run(query,name=self.Name,sentinel=-1,ost=self.OST,ist=self.IST,score=scores,admissionrate=self.OAR,location=self.State).dump()

	def findAll():
		query="MATCH (c:College) RETURN c"
		return graph.run(query).data()
class Applicant:
	def __init__(self,gpa,testtype,score,state,school,major):
		self.GPA=gpa
		self.School=school
		self.ISOS=state
		self.Score=score
		self.TestType=testtype
		self.Major=major

	def insert(self):
		query= "CREATE (a:Applicant{GPA:{gpa},School:{school},ISOS:{state},TestType:{testtype},Score:{score},Major:{major}}) RETURN a.id"
		return graph.run(query,gpa=self.GPA,school=self.School,state=self.ISOS,score=self.Score,testtype=self.TestType,major=self.Major)
	def insertRelationship(self):
		query="MATCH (c:College),(a:Applicant) WHERE c.Name={name} AND a.School={name} CREATE UNIQUE (c)-[:Admitted]->(a) RETURN a"
		return graph.run(query,name=self.School)
	def findRelationship(idtodelete):
		query="MATCH (c:College)-[r:Admitted]->(a:Applicant) WHERE  ID(a)={id} DELETE r"
		return graph.run(query,id=idtodelete)
	def delete(idtodelete):
		query="MATCH (a:Applicant) WHERE ID(a)={id} DELETE a"
		return graph.run(query,id=idtodelete)
	


app=Flask(__name__)
CORS(app)

@app.route('/insertApplicant',methods=['GET','POST'])
def insertApplicant():
		print(request.json)
		if request.method=='POST':
				gpa=request.json['GPA']
				testtype=request.json['TestType']
				score=request.json['Score']
				state=request.json['Instate/OutofState']
				school=request.json['UniversityName']
				major=request.json['Major']
				Applicant(gpa,testtype,score,state,school,major).insert()
				Applicant(gpa,testtype,score,state,school,major).insertRelationship()
				#flash("Applicant inserted")
		return render_template('/applicantinserted.html')

				

@app.route('/updateCollege',methods=['GET','POST'])
def updateCollege():
	if request.method=='POST':
		name=request.json['UniversityName']
		state=request.json['State']
		admissionrate=request.json['AdmissionRate']
		instatetuition=request.json['TuitionIS']
		outofstatetuition=request.json['TuitionOS']
		testtype=request.json['TestType']
		testscore=request.json['Score']

		College(name,admissionrate,instatetuition,outofstatetuition,testtype,testscore,state).updateOAR(admissionrate)
		College(name,admissionrate,instatetuition,outofstatetuition,testtype,testscore,state).updateOST(outofstatetuition)
		College(name,admissionrate,instatetuition,outofstatetuition,testtype,testscore,state).updateIST(instatetuition)
		College(name,admissionrate,instatetuition,outofstatetuition,testtype,testscore,state).updatescore(testtype,testscore)
		return "Updated college!"
@app.route('/deleteApplicant',methods=['GET','POST'])
def deleteApplicant():
	if request.method=='POST':
		ids=request.json['ApplicantID']
		Applicant.findRelationship(int(ids))
		Applicant.delete(int(ids))
		return "Deleted applicant!"
@app.route('/insertCollege',methods=['GET','POST'])
def insertCollege():
	if request.method=='POST':
		name=request.json['UniversityName']
		admissionrate=request.json['AdmissionRate']
		instatetuition=request.json['TuitionIS']
		outofstatetuition=request.json['TuitionOS']
		testtype=request.json['TestType']
		testscore=request.json['Score']
		state=request.json['State']
		College(name,admissionrate,instatetuition,outofstatetuition,testtype,testscore,state).insert(testtype)
		return "Inserted college!"

@app.route('/returnColleges',methods=['GET','POST'])
def returnAllColleges():
	if request.method=='GET':
		vals=College.findAll()
		
	dictcolleges={}
	# print(len(vals))
	# for a in range(0,len(vals)):

	# 	name=vals[a].get('c').get('Name')
	# 	act=vals[a].get('c').get('ACT')
	# 	sat=vals[a].get('c').get('SAT')
	# 	state=vals[a].get('c').get('State')
	# 	acceptance=vals[a].get('c').get('OAR')
	# 	ost=vals[a].get('c').get('OST')
	# 	ist=vals[a].get('c').get('IST')

	# 	dictcolleges["Name"]=name
	# 	dictcolleges["ACT"]=act
	# 	dictcolleges["SAT"]=sat
	# 	dictcolleges["State"]=state
	# 	dictcolleges["OAR"]=acceptance
	# 	dictcolleges["OST"]=ost
	# 	dictcolleges["IST"]=ist
	dictcolleges['data'] = vals



	return dictcolleges



if __name__ == '__main__':
    app.run()




