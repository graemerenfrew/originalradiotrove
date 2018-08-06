from django.shortcuts import render_to_response

def cataloghome(request):
    return render_to_response("index.html")

def directoryhome(request):
    return render_to_response("directoryindex.html")

def creativeworkhome(request):
    return render_to_response("creativeworkindex.html")