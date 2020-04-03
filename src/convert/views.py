from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import DocumentForm
from django.views.generic.edit import FormView
from .models import Document
from .htmlregexparser import htmlregexparser
import os
import time
from django.views.static import serve


#import function to handle an uploaded file.
#from somewhere import handle_uploaded_file

# Create your views here.
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        #print(request.FILES['document'].content_type)
        #print(request.POST)
        if form.is_valid():
            #print(vars(form.fields['document']))
            objall = Document.objects.all()
            index=len(objall)
            form.save()
            objall = Document.objects.all()
            objname= str(objall.get(id=index+1).document) #converst the path into a string
            editedobjname=(objname.split('/')[1]).split('.')[0]
            basedirectory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            mediadir = os.path.join(basedirectory, 'media')
            docdir = os.path.join(mediadir, 'documents')
            filepath= os.path.join(docdir, editedobjname)
            toolpath = os.path.join(basedirectory, 'convert')
            toolpath = os.path.join(toolpath, 'pdf2htmlex')
            toolpath = os.path.join(toolpath, 'pdf2htmlex.exe')
            htmlregexparser(toolpath, filepath)

            return serve(request ,os.path.basename(filepath+'.xlsx'), os.path.dirname(filepath+'.xlsx'))
            '''
            render(request, 'upload.html', {
                'form': form
            })
            '''
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })


'''
def model_convert(request):
    return HttpResponse("Here's the text of the Web page.")

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'upload.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = ModelFormWithFileField(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return render(request, 'upload.html', {'form': form})

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
'''
