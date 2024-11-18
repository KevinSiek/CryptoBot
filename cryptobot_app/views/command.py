from django.shortcuts import render

def command_view(request):
    command = 'Testing'

    print(command)

    if request.method == 'POST':
      command = request.POST.get('command')

    return render(request, 'command.html', {'command': command})