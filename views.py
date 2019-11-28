from flask import Flask,request,session,redirect,url_for,abort,flash,render_template
#from flask_restful import Resource,Api
from neo4jrestclient.client import GraphDatabase
from py2neo import Graph,Node,Relationship
from flask_cors import CORS
import os
import mysql.connector
from collections import defaultdict
import numpy as np
url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username='neo4j'
password='alawini'
graph = Graph(url + '/db/data/', username=username, password=password)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Zakimsjhs2017"
)
mycursor=mydb.cursor()

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

		return graph.run(query,name=self.Name,sentinel=-1,ost=self.OST,ist=self.IST,score=scores,admissionrate=self.OAR,location=self.State)

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
		query="MATCH (c:College)-[r:Admitted]->(a:Applicant) WHERE  a.User={id} DELETE r"
		return graph.run(query,id=idtodelete)
	def delete(idtodelete):
		query="MATCH (a:Applicant) WHERE a.User={id} DELETE a"
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
		print("College updated!")
		return "Updated college!"
@app.route('/deleteApplicant',methods=['GET','POST'])
def deleteApplicant():
	if request.method=='POST':
		ids=request.json['ApplicantID']
		Applicant.findRelationship(ids)
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
@app.route('/matchColleges',methods=["GET",'POST'])
def matchColleges():
	reach=[]
	match=[]
	safety=[]
	master=defaultdict(list)
	
	
	if request.method=="POST":
		gpa=request.json['GPA']
		act=int(request.json['actScore'])
		sat=int(request.json['satScore'])
		tuition=int(request.json['maximumTuition'])
		major=request.json['majorCategory']
		region=request.json['region']
		state=request.json['state']
		mycursor.execute("USE project")
		
		if sat!=0:
				mycursor.execute("SELECT ACT FROM conversion where SAT=%s",(sat,))
				myresult = mycursor.fetchall()
				convert=myresult[0][0]
				maxscore=max(int(convert),int(act))
		else:
			maxscore=act
		indexapp=(maxscore*10)+(200*float(gpa))
		
		query="MATCH (c:College)-[Admitted]->(a:Applicant) WHERE a.Major={majors} and a.TestType={test} RETURN toFloat(a.GPA)*toInt(200)+(toInt(a.Score)*10) as idx,a.School as School"
		results=graph.run(query,majors=major,test="ACT")
		allcolleges=College.findAll()
		names=[]
		for c in allcolleges:
			val=c.get('c')
			name=val.get('Name')
			names.append(name)
		

			

		for a in results:
			index=a[0]
			college=a[1]
			master[college].append(index)
		query="MATCH (c:College)-[Admitted]->(a:Applicant) WHERE a.Major={majors} and a.TestType={test} RETURN a.School as School,a.GPA,a.Score"
		satapps=graph.run(query,majors=major,test="SAT")

		for b in satapps:
			name=b[0]
			gpa=b[1]
			score=b[2]
			mycursor.execute("SELECT ACT FROM conversion where SAT=%s",(score,))
			myresult = mycursor.fetchall()
			convert=myresult[0][0]
			idx=(float(gpa)*200)+(10*int(convert))
			master[name].append(idx)
		

	keys=master.keys()
	for a in keys:
		vals=np.array(master[a])
		sd=np.std(vals)
		avg=np.mean(vals)
		if indexapp>=sd+avg:
			safety.append(a)
		elif indexapp>=avg and indexapp<avg+sd:
			match.append(a)
		elif indexapp>=avg-sd:
			reach.append(a)
	#print(reach,safety,match)
	matches=defaultdict(list)


	
	query="MATCH (c:College) WHERE c.State={state} and toInt(c.IST)<={max} RETURN c.Name"
	result=graph.run(query,state=state,max=tuition)
	afford=[]
	for a in result:
		afford.append(a[0])
	print(afford)
	
	query="MATCH (c:College) WHERE c.State<>{state} and c.OST<={max} RETURN c.Name"
	results=graph.run(query,state=state,max=tuition)
	for c in results:
		afford.append(c[0])
	matchafford=[item for item in match if item in afford]
	reachafford=[item for item in reach if item in afford]
	safetyafford=[item for item in safety if item in afford]



	if region!='No Preference':
			mycursor.execute("SELECT State FROM state WHERE region=%s ",(region,))
			results=mycursor.fetchall()
			regions=[]
			for a in results:
				regions.append(a[0])
	
			schoolsinregion=[]
			for c in regions:
				query="MATCH (c:College) WHERE c.State={state} RETURN c.Name"
				answer=graph.run(query,state=c)
				for b in answer:
					schoolsinregion.append(b[0])
			reachaffordregion=[item for item in reachafford if item in schoolsinregion]
			matchaffordregion=[item for item in matchafford if item in schoolsinregion]
			safetyaffordregion=[item for item in safetyafford if item in schoolsinregion]
			for a in reachaffordregion:
				matches['Reach'].append(a)
			for b in matchaffordregion:
				matches['Safety'].append(b)
			for c in safetyaffordregion:
				matches['Match'].append(c)
	else:

			for a in reachafford:
				matches['Reach'].append(a)

			for b in matchafford:
				matches['Match'].append(b)
			for c in safetyafford:
				matches['Safety'].append(c)

	matches['Reach']
	matches['Safety']
	matches['Match']
	return matches
@app.route('/competitive',methods=['GET','POST'])
def mostLeastCompetitive():
	colleges=[]
	ans={}
	if request.method=='GET':
		mycursor.execute("USE project")
		major=str(request.json['majorCategory'])
		region=request.json['region']
		mycursor.execute("DROP TABLE canattend") 
		mycursor.execute("CREATE TABLE canattend AS SELECT * FROM Colleges c NATURAL JOIN state r WHERE r.Region=%s",(region,))
		mycursor.execute("SELECT * from canattend")
		results=mycursor.fetchall()
		for a in results:
			colleges.append(a[2])
		print(colleges)
		mycursor.execute("DROP TABLE IF EXISTS sat")
		mycursor.execute(" CREATE TABLE sat AS SELECT * FROM Applicants a JOIN conversion c ON a.TestScore=c.SAT")
		mycursor.execute("DROP TABLE IF EXISTS master")
		mycursor.execute("CREATE TABLE master AS SELECT * FROM Applicants NATURAL join sat")
		mycursor.execute("UPDATE Applicants a NATURAL JOIN sat s SET a.TestScore=s.ACT WHERE a.User=s.User")
		mycursor.execute("DROP TABLE IF EXISTS final")
		mycursor.execute(" CREATE TABLE final AS SELECT *, ((TestScore*10)+(GPA*200)) as idx FROM Applicants")
		#mycursor.execute("SELECT * FROM final")
		mycursor.execute("SELECT School,AVG(idx) as AVGINDEX FROM final  WHERE Major=%s GROUP BY School ORDER BY AVGINDEX DESC",(major,))
		result=mycursor.fetchall()
		for a in result:
			if a[0] in colleges:
				ans['Most Competitive']=a[0]
				break
		mycursor.execute("SELECT School,AVG(idx) as AVGINDEX FROM final  WHERE Major=%s GROUP BY School ORDER BY AVGINDEX ASC",(major,))
		res=mycursor.fetchall()
		for a in res:
			if a[0] in colleges:
				ans['Least Competitive']=a[0]
				break
		ans['Most Competitive']
		ans['Least Competitive']


	return ans

		

		

		
		#print(master)

	





if __name__ == '__main__':
    app.run()




