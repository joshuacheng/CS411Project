from flask import Flask,request,session,redirect,url_for,abort,flash
#from flask_restful import Resource,Api
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph,Node,Relationship
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
	


app=Flask(__name__)
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
				return "Applicant inserted"

				

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
		Applicant.delete(ids)
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




if __name__ == '__main__':
    app.run()




