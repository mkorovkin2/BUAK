from django.shortcuts import render
from django.http import HttpResponse
from dns_backend import upload
from dns_backend import download
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper
from .models import Filename

import simplejson
import time
import os
from os import walk
import magic

def index(request):
	objs = Filename.objects.filter(username="TEST_USER").values()
	print(objs)
	return render(request, 'index.html', {'objs':objs})

def load404(request):
	return render(request, '404.html', {})

def home(request):
	return render(request, 'home.html', {})

def run_backend_code(request):
	print("Calling \"run_backend_code\"...")
	if request.method == 'GET':
		print("Successful GET request to \"run_backend_code\". Executing contents.")
		path = request.GET['run_backend_code']

		# DO SOMETHING HERE
		uploader = upload.Upload()
		uploader.save(path)
		# time.sleep(3)

		results = [{'backend_response': 'SUCCESSFUL RESPONSE IN COA+ALLING THE BACKEND'}]
		json_response = simplejson.dumps(results)

		return HttpResponse(json_response)
	else:
		print("Failed request to \"run_backend_code\". Exiting.")
		return HttpResponse("Request method is not a GET")

def get_list_of_cached_files(request):
	print("Calling \"run_backend_code\"...")
	if request.method == 'GET':
		server_input = request.GET['run_backend_code']

		# DO SOMETHING HERE - START
		time.sleep(2)
		fs = FileSystemStorage()

		f = []
		for (dirpath, dirnames, filenames) in walk(fs.location):
			f.extend(filenames)
			break
		file_list_return = "* " + ("\n* ".join(f))
		# DO SOMETHING HERE - END

		results = [{'backend_response': file_list_return}]
		json_response = simplejson.dumps(results)

		return HttpResponse(json_response)
	else:
		return HttpResponse("Request method is not a GET")

def simple_file_upload_with_drag_and_drop(request):
	if request.method == 'POST' and request.FILES['file']:
		file = request.FILES['file'];
		print('got a file', file.name)
		fs = FileSystemStorage()
		filename = fs.save(file.name, file)
		uploaded_file_url = fs.url(filename)
		return HttpResponse("File upload successful (file.name=\"" + file.name + "\")")

	return HttpResponse("ERROR")

def filter_file_name(filename):
	return filename.replace(" ", "_")

def simple_file_upload(request):
	if request.method == 'POST' and request.FILES['file']:
		file = request.FILES['file'];
		filename = filter_file_name(file.name)
		print('got a file', filename)
		uploader = upload.Upload()
		record_count = uploader.saveFromFile(file.file, filename)
		filename_record = Filename(username="TEST_USER", filename=filename, record_count = record_count)
		filename_record.save()
		return HttpResponse(status=205)
	return HttpResponse("ERROR")

def simple_file_download(request):
	try:
		downloader = download.Download()
		filename = filter_file_name(request.POST.get('textfield', None))
		file = downloader.downloadFromFile(filename)
		if file == None:
			raise Exception("No file found")
		chunk_size = 8192
		response = HttpResponse(FileWrapper(file, chunk_size), content_type=magic.from_file(file.name, mime=True))
		response['Content-Length'] = os.stat(filename).st_size
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response
	except Exception as e:
		print(e)
		return load404(request)
