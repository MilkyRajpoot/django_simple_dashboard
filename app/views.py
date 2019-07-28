
# Create your views here.

from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context
from datetime import datetime

from django.views import View
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


import pymongo 
import urllib 

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listDocument')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {
        'form': form
    })


URL = "mongodb://iot:"+urllib.quote('@')+'maapapa19'+"@cluster0-shard-00-00-bfyv0.mongodb.net:27017,cluster0-shard-00-01-bfyv0.mongodb.net:27017,cluster0-shard-00-02-bfyv0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority"
        
def listDocument(request):
    if request.method == 'GET':
        
        client = pymongo.MongoClient(URL)
        res_db = client.get_database("smart")
        
        record = res_db.door
        count = record.count_documents({})
        
        document_qs = []
        collection = res_db.door.find()
        
        for val in collection:
            print("val", val)
            if "allow" in val:
                allow = val["allow"]
                if allow is False:
                    document_qs.append(val)

        print ("print all document_qs",document_qs.reverse())

        return render(request, 'listDocument.html', {'document_qs': document_qs,})




def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


def AllowPerson(request):
    if request.method=="GET":
        obj = request.GET.get('objID')
        print('obj', obj)
        
        client = pymongo.MongoClient(URL)
        res_db = client.get_database("smart")
        
        record = res_db.door

        myquery = { "date": obj }
        newvalues = { "$set": { "allow": True} }

        record.update_one(myquery, newvalues)

        for x in record.find():
          print("x", x)
       
        return redirect('listDocument')

        