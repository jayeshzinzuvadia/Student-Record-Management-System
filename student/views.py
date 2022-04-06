import os
import xlrd
import datetime
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.urls import reverse
from student.models import Student, Skill, Achievements
from django.core.paginator import Paginator

# Create your views here.
def studentsList(request):
    """
    Returns the list of all students from the database
    """
    students = Student.objects.all().order_by('-batch_year', 'name')
    paginator = Paginator(students, 10)
    pageNumber = request.GET.get('page')
    pageObject = paginator.get_page(pageNumber)
    return render(request=request, template_name = "student/view_student_list.html", context={'student_list':pageObject, 'totalStudents' : len(students)})

# For search student
class SearchStudentView(generic.ListView):
    context_object_name = 'search_results'
    template_name = 'student/view_student_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q == "":
            return HttpResponseRedirect(reverse('student:allstudentslist'))
        
        # Search by ID, Name, Company 
        query = Student.objects.filter(
            Q(id_no__icontains = q) |
            Q(name__icontains =  q) |
            Q(internship__icontains = q) |
            Q(placement__icontains = q)
        )
        return {'searchFlag' : True, 'students': query, 'totalSearchResults': len(query)}

# For filter students view only
def viewFilterStudent(request):
    # Returns the view only
    return render(request,"student/filter_student_records.html")

# Do filter work here
class ViewFilterResults(generic.ListView):
    context_object_name = 'filter_results'
    template_name = 'student/filter_student_records.html'

    def get_queryset(self):
        q_career_preference = self.request.GET.get('career_preference')
        q_company_name = self.request.GET.get('company_name')
        q_batch_year = self.request.GET.get('batch_year') if self.request.GET.get('batch_year') != '' else date.today().year
        q_cpi = self.request.GET.get('cpi') if self.request.GET.get('cpi') != '' else 0
        q_branch = self.request.GET.get('branch')
        q_admission_category = self.request.GET.get('admission_category')
        q_gender = self.request.GET.get('gender')
        q_cast_category = self.request.GET.get('cast_category')

        if q_admission_category == '' and self.request.GET.get('batch_year') == '' and q_branch == '' and q_career_preference == '' and q_cast_category == '' and q_company_name == '' and self.request.GET.get('cpi') == '' and q_gender == '':
            return {'filterFlag' : False, 'errMsg': 'Provide some filters first'}

        filteredQueryObj = Q(
            batch_year = q_batch_year,
            career_preference__icontains = q_career_preference,
            cpi__gte = q_cpi,
            branch__icontains = q_branch,
            admission_category__icontains = q_admission_category,
            gender__icontains = q_gender,
            cast_category__icontains = q_cast_category,
            placement__icontains = q_company_name
        ) | Q(
            batch_year = q_batch_year,
            career_preference__icontains = q_career_preference,
            cpi__gte = q_cpi,
            branch__icontains = q_branch,
            admission_category__icontains = q_admission_category,
            gender__icontains = q_gender,
            cast_category__icontains = q_cast_category,
            internship__icontains = q_company_name
        )
        # Search by ID, Name, Company
        query = Student.objects.filter(filteredQueryObj)
        if len(query) == 0:
            print('Empty filter results')
            return {'filterFlag' : False, 'errMsg': 'No student records found by applying filters'}
        return {'filterFlag' : True, 'students': query, 'totalFilterResults': len(query)}

# For get request
def viewAddStudent(request):
    return render(request,"student/add_student_record.html")

# For post request
def addStudent(request):
    if request.method == "POST":
        id_no = request.POST.get('id_no', False)
        name = request.POST.get('name', False)
        branch = request.POST.get('branch', False)
        admission_category = request.POST.get('admission_category', False)
        cast_category = request.POST.get('cast_category', False)
        gender = request.POST.get('gender', False)
        dob = request.POST.get('dob', False)
        email_id = request.POST.get('email_id', False)
        contact_no_1 = request.POST.get('contact_no_1', False)
        contact_no_2 = request.POST.get('contact_no_2', False)
        ssc_result = request.POST.get('ssc_result', False)
        hsc_result = request.POST.get('hsc_result', False)
        diploma_result = request.POST.get('diploma_result', False)
        spi_sem_1 = request.POST.get('spi_sem_1', False)
        spi_sem_2 = request.POST.get('spi_sem_2', False)
        spi_sem_3 = request.POST.get('spi_sem_3', False)
        spi_sem_4 = request.POST.get('spi_sem_4', False)
        spi_sem_5 = request.POST.get('spi_sem_5', False)
        spi_sem_6 = request.POST.get('spi_sem_6', False)
        spi_sem_7 = request.POST.get('spi_sem_7', False)
        spi_sem_8 = request.POST.get('spi_sem_8', False)
        cpi = request.POST.get('cpi', False)
        address_1 = request.POST.get('address_1', False)
        address_2 = request.POST.get('address_2', False)
        address_3 = request.POST.get('address_3', False)
        city = request.POST.get('city', False)
        state = request.POST.get('state', False)
        pin_code = request.POST.get('pin_code', False)
        career_preference = request.POST.get('career_preference', False)
        internship = request.POST.get('internship', False)
        placement = request.POST.get('placement', False)
        salary = request.POST.get('salary', False)
        other_placement_1 = request.POST.get('other_placement_1', False)
        other_placement_2 = request.POST.get('other_placement_2', False)

        # Student Model object
        student_obj = Student(
            id_no = id_no, 
            name = name, 
            branch = branch, 
            admission_category = admission_category,
            cast_category = cast_category,
            gender = gender,
            dob = dob,
            email_id = email_id,
            contact_no_1 = contact_no_1,
            contact_no_2 = contact_no_2,
            ssc_result = ssc_result,
            hsc_result = hsc_result,
            diploma_result = diploma_result,
            spi_sem_1 = spi_sem_1,
            spi_sem_2 = spi_sem_2,
            spi_sem_3 = spi_sem_3,
            spi_sem_4 = spi_sem_4,
            spi_sem_5 = spi_sem_5,
            spi_sem_6 = spi_sem_6,
            spi_sem_7 = spi_sem_7,
            spi_sem_8 = spi_sem_8,
            cpi = cpi,
            address_1 = address_1,
            address_2 = address_2,
            address_3 = address_3,
            city = city,
            state = state,
            pin_code = pin_code,
            career_preference = career_preference,
            internship = internship,
            placement = placement,
            salary = salary,
            other_placement_1 = other_placement_1,
            other_placement_2 = other_placement_2)

        # Saving model object
        student_obj.save()

        # For Skills model
        total_skills = request.POST.get('total_skills', 0)
        if total_skills != '':
            total_skills = int(total_skills)
            removed_sids = request.POST.get('removed_sids', [])
            if len(removed_sids) != 0:
                removed_sids = removed_sids.split(',')
                removed_sids = removed_sids[:-1]
            # Saving model object
            for i in range(total_skills):
                if str(i) not in removed_sids:
                    s = request.POST.get('skills[' + str(i) + ']')
                    print(s)
                    if s != '':
                        skill_obj = Skill(stu_id_id = id_no, skills = s)
                        skill_obj.save()

        # For Achievements model
        total_achievements = request.POST.get('total_achievements', 0)
        if total_achievements != '':
            total_achievements = int(total_achievements)
            removed_aids = request.POST.get('removed_aids', [])
            if len(removed_aids) != 0:
                removed_aids = removed_aids.split(',')
                removed_aids = removed_aids[:-1]
                # removed_aids = list(map(int, removed_aids[:-1]))
            # Saving model object
            for i in range(total_achievements):
                if str(i) not in removed_aids:
                    a = request.POST.get('achievements[' + str(i) + ']')
                    print(a)
                    if a != '':
                        achievement_obj = Achievements(stu_id_id = id_no, achievement_details = a)
                        achievement_obj.save()

    return HttpResponseRedirect(reverse('student:allstudentslist'))

# For GET request
def viewUploadFile(request):
    return render(request, "student/upload_file.html")

# For saving student records in file
def saveStudentRecordsFromFile(sheet):
    for idx in range(1, sheet.nrows):
        id_no = sheet.cell_value(idx, 0)
        if isinstance(id_no, float):
            id_no = int(id_no)
        name = sheet.cell_value(idx, 1)
        branch = sheet.cell_value(idx, 2)
        admission_category = sheet.cell_value(idx, 3)
        cast_category = sheet.cell_value(idx, 4)
        gender = sheet.cell_value(idx, 5)
        dob = sheet.cell_value(idx, 6)
        email_id = sheet.cell_value(idx, 7)
        contact_no_1 = str(sheet.cell_value(idx, 8))
        contact_no_2 = str(sheet.cell_value(idx, 9))
        ssc_result = sheet.cell_value(idx, 10) if sheet.cell_value(idx, 10) != '' else 0
        hsc_result = sheet.cell_value(idx, 11) if sheet.cell_value(idx, 11) != '' else 0
        diploma_result = sheet.cell_value(idx, 12) if sheet.cell_value(idx, 12) != '' else 0
        spi_sem_1 = sheet.cell_value(idx, 13) if sheet.cell_value(idx, 13) != '' else 0
        spi_sem_2 = sheet.cell_value(idx, 14) if sheet.cell_value(idx, 14) != '' else 0
        spi_sem_3 = sheet.cell_value(idx, 15) if sheet.cell_value(idx, 15) != '' else 0
        spi_sem_4 = sheet.cell_value(idx, 16) if sheet.cell_value(idx, 16) != '' else 0
        spi_sem_5 = sheet.cell_value(idx, 17) if sheet.cell_value(idx, 17) != '' else 0
        spi_sem_6 = sheet.cell_value(idx, 18) if sheet.cell_value(idx, 18) != '' else 0
        spi_sem_7 = sheet.cell_value(idx, 19) if sheet.cell_value(idx, 19) != '' else 0
        spi_sem_8 = sheet.cell_value(idx, 20) if sheet.cell_value(idx, 20) != '' else 0
        cpi = sheet.cell_value(idx, 21) if sheet.cell_value(idx, 21) != '' else 0
        address_1 = sheet.cell_value(idx, 22)
        address_2 = sheet.cell_value(idx, 23)
        address_3 = sheet.cell_value(idx, 24)
        city = sheet.cell_value(idx, 25)
        state = sheet.cell_value(idx, 26)
        pin_code = str(sheet.cell_value(idx, 27))
        career_preference = sheet.cell_value(idx, 28)
        internship = sheet.cell_value(idx, 29)
        placement = sheet.cell_value(idx, 30)
        salary = sheet.cell_value(idx, 31) if sheet.cell_value(idx, 31) != '' else 0
        other_placement_1 = sheet.cell_value(idx, 32)
        other_placement_2 = sheet.cell_value(idx, 33)
        batch_year = sheet.cell_value(idx, 34) if sheet.cell_value(idx, 34) != '' else 0

        if "/" in dob:
            dob = datetime.datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")

        # Student Model object
        student_obj = Student(
            id_no = id_no, 
            name = name, 
            branch = branch, 
            admission_category = admission_category,
            cast_category = cast_category,
            gender = gender,
            dob = dob,
            email_id = email_id,
            contact_no_1 = contact_no_1,
            contact_no_2 = contact_no_2,
            ssc_result = ssc_result,
            hsc_result = hsc_result,
            diploma_result = diploma_result,
            spi_sem_1 = spi_sem_1,
            spi_sem_2 = spi_sem_2,
            spi_sem_3 = spi_sem_3,
            spi_sem_4 = spi_sem_4,
            spi_sem_5 = spi_sem_5,
            spi_sem_6 = spi_sem_6,
            spi_sem_7 = spi_sem_7,
            spi_sem_8 = spi_sem_8,
            cpi = cpi,
            address_1 = address_1,
            address_2 = address_2,
            address_3 = address_3,
            city = city,
            state = state,
            pin_code = pin_code,
            career_preference = career_preference,
            internship = internship,
            placement = placement,
            salary = salary,
            other_placement_1 = other_placement_1,
            other_placement_2 = other_placement_2,
            batch_year = batch_year)

        # Saving model object
        student_obj.save()

# For POST request
def postUploadFile(request):
    if request.method == "POST":
        if request.FILES:
            fileObj = request.FILES['uploadFile']
            print('File name : ', fileObj.name)
            extension = fileObj.name[-4:]
            # Check for file extension
            if extension == ".xls":
                # Saving file in server temporarily
                fs = FileSystemStorage()
                fs.save(fileObj.name, fileObj)
                filePath = 'srms/static/tmp/' + fileObj.name
                # Read excel sheet using xlrd
                wb = xlrd.open_workbook(filePath)
                sheet = wb.sheet_by_index(0)
                # Read file and add student records
                saveStudentRecordsFromFile(sheet)
                # Delete file in server
                os.remove(os.path.join('srms/static/tmp', fileObj.name))
                return HttpResponseRedirect(reverse('student:allstudentslist'))
            else:
                return render(request, "student/upload_file.html", {"error" : "Please upload file having .xls extension"})
        else:
            print("File not uploaded")
    return render(request, "student/page_not_found.html")

class ViewStudentRecord(generic.ListView):
    """
    View Student Information
    """
    template_name = 'student/view_student_record.html'
    context_object_name = 'student_obj'

    def get_queryset(self):
        if 'id' in self.kwargs:
            stu = Student.objects.get(id_no = self.kwargs['id'])
            stu_skills = Skill.objects.filter(stu_id_id = self.kwargs['id'])
            stu_achievements = Achievements.objects.filter(stu_id_id = self.kwargs['id'])
            return {
                "student" : stu,
                "skills" : stu_skills,
                "achievements" : stu_achievements,
            }
        return None

class UpdateStudentRecord(generic.ListView):
    """
    Update student record
    """
    template_name = 'student/update_student_record.html'
    context_object_name = 'student_obj'

    def get_queryset(self):
        if 'id' in self.kwargs:
            stu = Student.objects.get(id_no = self.kwargs['id'])
            stu_skills = Skill.objects.filter(stu_id_id = self.kwargs['id'])
            stu_achievements = Achievements.objects.filter(stu_id_id = self.kwargs['id'])
            return {
                "student" : stu,
                "skills" : stu_skills,
                "achievements" : stu_achievements,
            }
        return None

# Post request
def updateStudent(request):
    if request.method == "POST":
        id_no = request.POST.get('id_no', False)
        name = request.POST.get('name', False)
        branch = request.POST.get('branch', False)
        admission_category = request.POST.get('admission_category', False)
        cast_category = request.POST.get('cast_category', False)
        gender = request.POST.get('gender', False)
        dob = request.POST.get('dob', False)
        email_id = request.POST.get('email_id', False)
        contact_no_1 = request.POST.get('contact_no_1', False)
        contact_no_2 = request.POST.get('contact_no_2', False)
        ssc_result = request.POST.get('ssc_result', False)
        hsc_result = request.POST.get('hsc_result', False)
        diploma_result = request.POST.get('diploma_result', False)
        spi_sem_1 = request.POST.get('spi_sem_1', False)
        spi_sem_2 = request.POST.get('spi_sem_2', False)
        spi_sem_3 = request.POST.get('spi_sem_3', False)
        spi_sem_4 = request.POST.get('spi_sem_4', False)
        spi_sem_5 = request.POST.get('spi_sem_5', False)
        spi_sem_6 = request.POST.get('spi_sem_6', False)
        spi_sem_7 = request.POST.get('spi_sem_7', False)
        spi_sem_8 = request.POST.get('spi_sem_8', False)
        cpi = request.POST.get('cpi', False)
        address_1 = request.POST.get('address_1', False)
        address_2 = request.POST.get('address_2', False)
        address_3 = request.POST.get('address_3', False)
        city = request.POST.get('city', False)
        state = request.POST.get('state', False)
        pin_code = request.POST.get('pin_code', False)
        career_preference = request.POST.get('career_preference', False)
        internship = request.POST.get('internship', False)
        placement = request.POST.get('placement', False)
        salary = request.POST.get('salary', False)
        other_placement_1 = request.POST.get('other_placement_1', False)
        other_placement_2 = request.POST.get('other_placement_2', False)
        batch_year = request.POST.get('batch_year', False)

        # Student Model object
        student_obj = Student.objects.get(pk=id_no) 
        student_obj.name = name
        student_obj.branch = branch
        student_obj.admission_category = admission_category
        student_obj.cast_category = cast_category
        student_obj.gender = gender
        student_obj.dob = dob
        student_obj.email_id = email_id
        student_obj.contact_no_1 = contact_no_1
        student_obj.contact_no_2 = contact_no_2
        student_obj.ssc_result = ssc_result
        student_obj.hsc_result = hsc_result
        student_obj.diploma_result = diploma_result
        student_obj.spi_sem_1 = spi_sem_1
        student_obj.spi_sem_2 = spi_sem_2
        student_obj.spi_sem_3 = spi_sem_3
        student_obj.spi_sem_4 = spi_sem_4
        student_obj.spi_sem_5 = spi_sem_5
        student_obj.spi_sem_6 = spi_sem_6
        student_obj.spi_sem_7 = spi_sem_7
        student_obj.spi_sem_8 = spi_sem_8
        student_obj.cpi = cpi
        student_obj.address_1 = address_1
        student_obj.address_2 = address_2
        student_obj.address_3 = address_3
        student_obj.city = city
        student_obj.state = state
        student_obj.pin_code = pin_code
        student_obj.career_preference = career_preference
        student_obj.internship = internship
        student_obj.placement = placement
        student_obj.salary = salary
        student_obj.other_placement_1 = other_placement_1
        student_obj.other_placement_2 = other_placement_2
        student_obj.batch_year = batch_year

        # Updating model object
        student_obj.save()

        # Deleting previous skills
        prevSkills = Skill.objects.filter(stu_id_id = id_no)
        for skill in prevSkills:
            skill.delete()

        # Adding new Skills model
        total_skills = request.POST.get('total_skills', 0)
        if total_skills != '':
            total_skills = int(total_skills)
            removed_sids = request.POST.get('removed_sids', [])
            if len(removed_sids) != 0:
                removed_sids = removed_sids.split(',')
                removed_sids = removed_sids[:-1]
            # Saving model object
            for i in range(total_skills):
                if str(i) not in removed_sids:
                    s = request.POST.get('skills[' + str(i) + ']')
                    print(s)
                    if s != '':
                        skill_obj = Skill(stu_id_id = id_no, skills = s)
                        skill_obj.save()
        
        # Deleting previous achievements
        prevAchievements = Achievements.objects.filter(stu_id_id = id_no)
        for achievement in prevAchievements:
            achievement.delete()

        # Adding new Achievements model
        total_achievements = request.POST.get('total_achievements', 0)
        if total_achievements != '':
            total_achievements = int(total_achievements)
            removed_aids = request.POST.get('removed_aids', [])
            if len(removed_aids) != 0:
                removed_aids = removed_aids.split(',')
                removed_aids = removed_aids[:-1]
                # removed_aids = list(map(int, removed_aids[:-1]))
            # Saving model object
            for i in range(total_achievements):
                if str(i) not in removed_aids:
                    a = request.POST.get('achievements[' + str(i) + ']')
                    print(a)
                    if a != '':
                        achievement_obj = Achievements(stu_id_id = id_no, achievement_details = a)
                        achievement_obj.save()

    return HttpResponseRedirect(reverse('student:allstudentslist'))

# For update multiple students GET request
def viewUpdateMultipleStudentRecords(request):
    return render(request, "student/update_multiple_student_records.html")

# For update multiple students POST request
def postUpdateMultipleStudentRecords(request):
    if request.method == "POST":
        id_list = request.POST.get('id_list', False)
        career_preference = request.POST.get('career_preference', False)
        internship = request.POST.get('internship', False)
        placement = request.POST.get('placement', False)
        salary = request.POST.get('salary', False)
        other_placement_1 = request.POST.get('other_placement_1', False)
        other_placement_2 = request.POST.get('other_placement_2', False)
        batch_year = request.POST.get('batch_year', False)
        branch = request.POST.get('branch', False)

        if career_preference == '' and internship == '' and placement == '' and salary == '' and other_placement_1 == '' and other_placement_2 == '' and batch_year == '' and branch == '':
            return render(request, "student/update_multiple_student_records.html", {'errMsg': 'Provide some data for the fields first'})
        
        # Student Model object
        id_list = id_list.split()
        # print(id_list)
        for id in id_list:
            try:
                student_obj = Student.objects.get(pk = id)
            except Student.DoesNotExist:
                return render(request, "student/update_multiple_student_records.html", {'errMsg': 'Record with the given id ' + str(id) + ' does not exist'})

            if branch != '':
                student_obj.branch = branch
            if career_preference != '':
                student_obj.career_preference = career_preference
            if internship != '':
                student_obj.internship = internship
            if placement != '':
                student_obj.placement = placement
            if salary != '':
                student_obj.salary = salary
            if other_placement_1 != '':
                student_obj.other_placement_1 = other_placement_1
            if other_placement_2 != '':
                student_obj.other_placement_2 = other_placement_2
            if batch_year != '':
                student_obj.batch_year = batch_year
            # Updating model object
            student_obj.save()
    return HttpResponseRedirect(reverse('student:allstudentslist'))


class DeleteStudentRecord(generic.ListView):
    """
    Delete student record
    """
    template_name = 'student/delete_student_record.html'
    context_object_name = 'student_obj'

    def get_queryset(self):
        return Student.objects.get(id_no = self.kwargs['id'])

def deleteStudent(request):
    if request.method == "POST":
        student = Student.objects.get(id_no = request.POST.get('id_no'))
        student.delete()
        return HttpResponseRedirect(reverse('student:allstudentslist'))


# Page Not Found
def pageNotFound(request):
    return render(request,"student/page_not_found.html")