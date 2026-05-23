from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import EventRegistrationForm


def register_event(request):
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration submitted successfully.')
            return redirect('event_register')
    else:
        form = EventRegistrationForm()

    return render(request, 'events/register.html', {'form': form})
