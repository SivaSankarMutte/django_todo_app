from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from App1.models import Faculty,ExamDetails,Questions,StudentRegistration,StudentsResults
from App1.forms import FacultyForm,ExamDetailsForm,QuestionsForm,StudentRegistrationForm
from Test import settings
from django.core.mail import send_mail

import random
import csv,io



def home(request):
	return render(request,'ht1/home.html')
def fhome(request,id):
	return render(request,'ht1/fhome.html',{'facid':id})

def flogin(request):
	form=FacultyForm()
	context={'form':form}
	if request.method=="POST":
		email=request.POST['email']
		psw=request.POST['psw']
		# facid=Faculty.objects.get(email=email).id
		# context['facid']=facid
		try:
			facid=Faculty.objects.get(email=email).id    #COPIED HERE
			context['facid']=facid                       #COPIED HERE 
			row=Faculty.objects.get(email=email) 
		except:
			return render(request,'ht1/InvalidFlogin.html')
		if row.psw==psw:
			return render(request,'ht1/fhome.html',context)
	return render(request,'ht1/flogin.html',context)

def createtest(request,fid):
	form=ExamDetailsForm()
	qsform=QuestionsForm()
	context={'form':form,'fid':fid}
	if request.method=="POST":
		form=ExamDetailsForm(request.POST,request.FILES)
		if form.is_valid():
			n=form.save(commit=False)
			finstance=Faculty.objects.get(id=fid)
			n.fid=finstance
			# n.eid=eid
			#context['eid']=n.id 
			context['examform']=n
			messages.success(request,"{} exam is created Successfully Let us add questions to it.".format(n.examName))
			# global k
			# k=n.noOfQuestions
			n.save()
			return render(request,'ht1/studentsUpload.html',context)
			# return render(request,'ht1/AddQuestions.html',{'form':qsform})###############################
		else:
			messages.error(request,'Exam is not created')
			return redirect(request.META['HTTP_REFERER'])

	return render(request,'ht1/createtest.html',context)

def AddQuestions(request,fid,eid,k):
	qsform=QuestionsForm()
	if request.method=="POST":
		qsform=QuestionsForm(request.POST,request.FILES)
		if qsform.is_valid():
			n=qsform.save(commit=False)  
			messages.success(request,"{} Question added".format(n.Question))
			n.eid_id=eid
			n.fid_id=fid
			n.save()
			while(k-1):
				k-=1
				return render(request,'ht1/AddQuestions.html',{'form':qsform,'fid':fid,'eid':eid,'k':k})
			return render(request,'ht1/qsaddedsuccess.html')

	return render(request,'ht1/AddQuestions.html',{'form':qsform,'fid':fid,'eid':eid,'k':k})

def studentsupload(request,fid,eid):
	prompt={"pointToRemember":"The File should be CSV and consists of Header (semails)"}
	if request.method=="GET":
		return render(request,'ht1/studentsUpload.html',prompt)
	csv_file=request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request,'This is not a CSV file')

	data_set=csv_file.read().decode('latin-1') #####################################
	# data_set = csv.reader(open("csv_file", 'rU'), dialect='excel')
	io_string=io.StringIO(data_set)
	next(io_string)
	for column in csv.reader(io_string, delimiter=",", quotechar="|"):
		_,created=StudentsResults.objects.update_or_create(
			eid=ExamDetails.objects.get(id=eid),
			semail=column[0],
			)
	context={'fid':fid,'eid':eid}
	#return render(request,'ht1/studentsUpload.html',context)
	#return render(request,'ht1/AddQuestions.html',context)
	k=ExamDetails.objects.get(id=eid).noOfQuestions
	return redirect(AddQuestions,fid,eid,k)


def facultyupload(request):
	prompt={"pointToRemember":"The File should be CSV and consists of Header (emails)"}
	if request.method=="GET":
		return render(request,'ht1/facultyUpload.html',prompt)
	csv_file=request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request,'This is not a CSV file')

	data_set=csv_file.read().decode('latin-1') #####################################
	# data_set = csv.reader(open("csv_file", 'rU'), dialect='excel')
	io_string=io.StringIO(data_set)
	next(io_string)
	for column in csv.reader(io_string, delimiter=",", quotechar="|"):
		_,created=Faculty.objects.update_or_create(
			email=column[0],
			psw=column[1],
			)
	return render(request,'ht1/facultyUploadedSuccess.html')

def StudRegistration(request):
	form=StudentRegistrationForm()
	if request.method=="POST":
		form=StudentRegistrationForm(request.POST,request.FILES)
		if form.is_valid():
			n=form.save(commit=False)
			messages.success(request,"{} Question added".format(n.regdno))
			n.save()

		return render(request,'ht1/slogin.html')
	return render(request,'ht1/studentRegistration.html',{'form':form})

def slogin(request):
	if request.method=="POST":
		semail=request.POST['semail']
		spsw=request.POST['spsw']
		try:
			row=StudentRegistration.objects.get(semail=semail)
		except:
			return render(request,'ht1/InvalidSlogin.html')
		if row.spsw==spsw:
			return render(request,'ht1/shome.html',{'student':row})
		else:
			return render(request,'ht1/studentWrongPsw.html')
	return render(request,'ht1/slogin.html')

def studentExam(request,semail):
	scheduledExams=StudentsResults.objects.filter(semail=semail)
	studentrow=StudentRegistration.objects.get(semail=semail)
	print(scheduledExams)
	ExamObjects=[]

	for i in scheduledExams:
		print("HERERRERRR")
		print(i)
		ExamObjects.append(ExamDetails.objects.get(id=i.eid_id))

	return render(request,'ht1/scheduledExams.html',{"ExamObjects":ExamObjects,'studentrow':studentrow})

###############################################################################################
###################################################
########################





#LAST HAPPENED   Works good but displays all Questions one one web page, so examopen.html is waste without this function and also examSubmitSuccess.html

# def examopen(request,sid,eid):
	
# 	semail=StudentRegistration.objects.get(id=sid).semail
# 	resultrow=StudentsResults.objects.get(semail=semail,eid_id=eid)
# 	qs=Questions.objects.filter(eid_id=eid)
# 	marks=0

# 	if request.method=="POST":
# 		qs=Questions.objects.filter(eid_id=eid)
# 		resultrow=StudentsResults.objects.get(semail=semail,eid_id=eid)
# 		for i in qs:
# 			print("HEREEEE",i.id)
# 			print(type(i.Question))
# 			answer=request.POST[i.Question]
# 			print("ANSER",answer,"OPTION",i.opt1,"i.ans",i.ans)
# 			print(type(answer),type(i.opt1),type(i.ans))
# 			if((answer==i.opt1 and i.ans=='1') or (answer==i.opt2 and i.ans=='2') or (answer==i.opt3 and i.ans=='3') or (answer==i.opt4 and i.ans=='4')):
# 				marks+=i.qmarks
# 				print("INRCREMENTED")
# 		print(marks)
# 		resultrow.marks_scored=marks
# 		resultrow.save()
# 		return render(request,'ht1/examSubmitSuccess.html')
# 	return render(request,'ht1/examopen.html',{'sid':sid,'eid':eid,'qs':qs})

# LAST HAPPPENED



###################################################################################
#####################################################
##############################














	# n=0
	# marks=0
	# semail=StudentRegistration.objects.get(id=sid).semail
	# resultrow=StudentsResults.objects.get(semail=semail,eid_id=eid)
	# qs=Questions.objects.filter(eid_id=eid)
	# print(qs)
	# questionsList=[]
	# if request.method=="GET":
	# 	for i in qs:
	# 		questionsList.append(i)
	# 	quest=questionsList[n]
	# 	print("EX")
	# 	print(quest.id)
	# if request.method=="POST": 
	# 	print("YYYYYYYYYYYYYYYYYYY")
	# 	print(request.POST.get(quest.id,False))
	# 	ans=request.POST.get(quest.id,False)
	# 	if((ans==quest.opt1 and quest.ans==1) or (ans==quest.opt2 and quest.ans==2) or (ans==quest.opt3 and quest.ans==3) or (ans==quest.opt4 and quest.ans==4)):
	# 		marks+=1
	# 	print(marks)
	# 	resultrow.marks_scored=marks
	# 	resultrow.save()
	# 	while(n<len(questionsList)):
	# 		n+=1
	# 		return render(request,'ht1/examopen.html',{'sid':sid,'eid':eid,'qs':qs,'quest':quest})
	# 	else:
	# 		return render(request,'ht1/examSubmitSuccess.html')
	# return render(request,'ht1/examopen.html',{'sid':sid,'eid':eid,'qs':qs,'quest':quest})



	# if request.method=="POST":
	# 	ans=request.POST.get(quest.id,False)
	# 	if((ans==quest.opt1 and quest.ans==1) or (ans==quest.opt2 and quest.ans==2) or (ans==quest.opt3 and quest.ans==3) or (ans==quest.opt4 and quest.ans==4)):
	# 		marks+=1
	# 	print(marks)
	# 	resultrow.marks_scored=marks
	# 	resultrow.save()
	# 	while(n<len(questionsList)):
	# 		n+=1
	# 		quest=questionsList[n]
	# 		return render(request,'ht1/examopen.html',{'sid':sid,'eid':eid,'quest':quest})
	# 	else:
	# 		return render(request,'ht1/examSubmitSuccess.html')
	# semail=StudentRegistration.objects.get(id=sid).semail
	# resultrow=StudentsResults.objects.get(semail=semail,eid_id=eid)
	# qs=Questions.objects.filter(eid_id=eid)
	# print(qs)
	# questionsList=[]
	# for i in qs:
	# 	questionsList.append(i)
	# n=0
	# quest=questionsList[n]
	# if(n<len(questionsList)):
	# 	return render(request,'ht1/examopen.html',{'sid':sid,'eid':eid,'quest':quest})
	# elif(len(questionsList)==0):
	# 	return render(request,'ht1/QNotPrepared.html')


def examopen(request,sid,eid):	
	semail=StudentRegistration.objects.get(id=sid).semail
	global resultrow
	resultrow=StudentsResults.objects.get(semail=semail,eid_id=eid)
	global qs
	qs=Questions.objects.filter(eid_id=eid)
	qs=list(qs)
	random.shuffle(qs)
	# global qlist
	# qlist=[]
	# for i in qs:
	# 	qlist.append(i)
	# random.shuffle(qlist)
	# Need to check pass just qs or list(qs) or compulsory to make qlist
	i=0

	return redirect(OneQuestion,i)


def OneQuestion(request,i):
	if request.method=="POST":
		try:
			q=qs[i]
		except:
			return render(request,'ht1/QuestionsLoadingError.html')
		marks=0
		answer=request.POST[q.Question]          #Need to change q.Question to q.id and corresponding OneQuestion.html page and if answer== logic also.. otherwise same question added gives error
		if((answer==q.opt1 and q.ans=='1') or (answer==q.opt2 and q.ans=='2') or (answer==q.opt3 and q.ans=='3') or (answer==q.opt4 and q.ans=='4')):
			marks=q.qmarks
		if i==0:
			resultrow.marks_scored=marks
		else:
			resultrow.marks_scored+=marks
		resultrow.save()
		i+=1
		if(i<len(qs)):
			return render(request,'ht1/OneQuestion.html',{'q':qs[i],'i':i})
		else:
			return render(request,'ht1/OneQuestionAllWritten.html')
	# print(resultrow)
	# print(qs)
	if(i<len(qs)):
		return render(request,'ht1/OneQuestion.html',{'q':qs[i],'i':i})
	return render(request,'ht1/QNotPrepared.html')




def modifytest(request,fid):
	tests=ExamDetails.objects.filter(fid_id=fid)
	return render(request,'ht1/modifytest.html',{'tests':tests,'fid':fid})

def specificTestModify(request,eid):
	form=Questions.objects.filter(eid_id=eid)
	if request.method=="POST":
		form=Questions.objects.filter(eid_id=eid)
		for i in form:
			i.Question=request.POST[i.Question]
			i.opt1=request.POST[i.opt1]
			i.opt2=request.POST[i.opt2]
			i.opt3=request.POST[i.opt3]
			i.opt4=request.POST[i.opt4]
			i.ans=request.POST[i.ans]
			i.save()
		# if form.is_valid():
		# 	form.save()
			return render(request,'ht1/testModifiedSuccess.html')
		return redirect(request.META['HTTP_REFERER'])
	return render(request,'ht1/specificTestModify.html',{'form':form,'eid':eid})

def specificTestDelete(request,eid):
	examrow=ExamDetails.objects.get(id=eid)
	examrow.delete()
	return redirect(request.META['HTTP_REFERER'])



#http://128.0.0.1:8000/adminlogin use it for admin login
def adminlogin(request):
	if request.method=="POST":
		adminname=request.POST['adminname']
		adminpsw=request.POST['adminpsw']
		if adminname=="admin" and adminpsw=="admin":
			return render(request,'ht1/adminpage.html')
			#return render(request,'ht1/facultyUpload.html')
		else:
			messages.error(request,"Invalid Credentials")
			return redirect(request.META['HTTP_REFERER'])
	return render(request,'ht1/adminlogin.html')

def adminpage(request):
	return render(request,'ht1/adminpage.html')

def facultyModify(request):
	facrows=Faculty.objects.all()
	return render(request,'ht1/facultyModify.html',{'facrows':facrows})

def facrowUpdate(request,id):
	row=Faculty.objects.get(id=id)
	if request.method=="POST":
		row=Faculty.objects.get(id=id)
		row.email=request.POST['email']
		row.psw=request.POST['psw']
		row.save()
		return redirect('/facultyModify')

	return render(request,'ht1/facrowUpdate.html',{'row':row})

def facrowDelete(request,id):
	row=Faculty.objects.get(id=id)
	row.delete()
	return redirect(request.META['HTTP_REFERER'])

def viewFaculty(request):
	allrows=Faculty.objects.all()
	return render(request,'ht1/viewFaculty.html',{'allrows':allrows})


def results(request,fid):
	exams=ExamDetails.objects.filter(fid_id=fid)
	print(fid)
	return render(request,'ht1/results.html',{'exams':exams,'facid':fid})

def displayTestResult(request,eid):
	fid=ExamDetails.objects.get(id=eid).fid_id
	rows=StudentsResults.objects.filter(eid_id=eid)
	ExamRow=ExamDetails.objects.get(id=eid)
	noOfQs=ExamDetails.objects.get(id=eid).noOfQuestions
	qrows=Questions.objects.filter(eid_id=eid)
	total=0
	for i in qrows:
		total+=i.qmarks
	context={'rows':rows,'ExamRow':ExamRow,'fid':fid,'noOfQs':noOfQs,'eid':eid,'total':total}
	return render(request,'ht1/displayTestResult.html',context)

def downloadResults(request,eid):
	response=HttpResponse(content_type='text/csv')

	writer=csv.writer(response)
	writer.writerow(['Student Email','Marks_Scored'])

	for student in StudentsResults.objects.filter(eid_id=eid).values_list('semail','marks_scored'):
		writer.writerow(student)
	response['Content-Disposition']='attachment; filename="MarksSheet.csv"'

	return response