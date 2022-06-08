from django.shortcuts import redirect, render
from .forms import RegistrationForm

# Create your views here.
def register(request):
    form = RegistrationForm(request.POST or None)

    if form.is_valid():
        form.save()

        return redirect('blog:list')

    context ={
        'form': form,
    }
    return render(request, 'users/register.html')
