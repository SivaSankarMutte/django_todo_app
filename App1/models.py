from django.db import models

# Create your models here.
class Faculty(models.Model):
	email=models.EmailField(max_length=100)
	psw=models.CharField(max_length=30)

class ExamDetails(models.Model):
	examName=models.CharField(max_length=100)
	#startTime=models.TimeField()
	#endTime=models.TimeField()
	noOfQuestions=models.IntegerField() 
	fid=models.ForeignKey(Faculty,on_delete=models.CASCADE) 

class Questions(models.Model):
	eid=models.ForeignKey(ExamDetails,on_delete=models.CASCADE)
	fid=models.ForeignKey(Faculty,on_delete=models.CASCADE)
	Question=models.CharField(max_length=1000)
	opt1=models.CharField(max_length=100)
	opt2=models.CharField(max_length=100)
	opt3=models.CharField(max_length=100,null=True)
	opt4=models.CharField(max_length=100,null=True)
	ans=models.CharField(max_length=100)
	qmarks=models.IntegerField(default=1)

class StudentsResults(models.Model):
	#studentid=models.ForeignKey(StudentRegistration,on_delete=models.CASCADE)
	eid=models.ForeignKey(ExamDetails,on_delete=models.CASCADE)################################
	semail=models.EmailField(max_length=100)
	marks_scored=models.IntegerField(null=True)

class StudentRegistration(models.Model):
	sname=models.CharField(max_length=100)
	regdno=models.CharField(max_length=20)
	rollno=models.IntegerField()
	semail=models.EmailField(max_length=100)
	spsw=models.CharField(max_length=30)



