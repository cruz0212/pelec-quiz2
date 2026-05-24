import json

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import EventRegistrationForm


def _form_errors(form):
    return {
        field: [error['message'] for error in errors]
        for field, errors in form.errors.get_json_data().items()
    }


def _with_cors_headers(request, response):
    allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', ['*'])
    request_origin = request.headers.get('Origin')

    if '*' in allowed_origins:
        response['Access-Control-Allow-Origin'] = '*'
    elif request_origin in allowed_origins:
        response['Access-Control-Allow-Origin'] = request_origin
        response['Vary'] = 'Origin'

    response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


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


@csrf_exempt
@require_http_methods(['POST', 'OPTIONS'])
def register_event_api(request):
    if request.method == 'OPTIONS':
        return _with_cors_headers(request, HttpResponse(status=204))

    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, json.JSONDecodeError):
        return _with_cors_headers(
            request,
            JsonResponse(
                {
                    'success': False,
                    'errors': {
                        'request': ['Invalid JSON payload.'],
                    },
                },
                status=400,
            ),
        )

    form = EventRegistrationForm(data=data)

    if form.is_valid():
        form.save()
        return _with_cors_headers(
            request,
            JsonResponse(
                {
                    'success': True,
                    'message': 'Registration submitted successfully.',
                },
                status=201,
            ),
        )

    return _with_cors_headers(
        request,
        JsonResponse(
            {
                'success': False,
                'errors': _form_errors(form),
            },
            status=400,
        ),
    )
