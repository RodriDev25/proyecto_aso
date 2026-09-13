import secrets
from urllib.parse import urlencode

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import PrestamoSolicitudForm, ValeSolicitudForm


ALLOWED_EMAIL_DOMAINS = ('outlook.com', 'hotmail.com', 'outlook.com.py', 'hotmail.com.py')


def _microsoft_base_url():
	return f'https://login.microsoftonline.com/{settings.MICROSOFT_TENANT}/oauth2/v2.0'


def _is_allowed_email(email):
	return email.lower().strip().endswith(tuple(f'@{domain}' for domain in ALLOWED_EMAIL_DOMAINS))


def iniciar_sesion(request):
	if request.user.is_authenticated:
		return redirect('home')
	return render(request, 'usuarios/iniciar_sesion.html', {'debug': settings.DEBUG})


def demo_home(request):
	if not settings.DEBUG:
		raise Http404
	return render(request, 'usuarios/home.html', {'modo_demo': True})


def cerrar_sesion(request):
	if request.method == 'POST':
		logout(request)
	return redirect('iniciar_sesion')


@require_GET
def microsoft_login(request):
	if not settings.MICROSOFT_CLIENT_ID or not settings.MICROSOFT_CLIENT_SECRET:
		messages.error(request, 'El inicio de sesión con Microsoft todavía no está configurado.')
		return redirect('iniciar_sesion')

	state = secrets.token_urlsafe(32)
	request.session['microsoft_oauth_state'] = state
	redirect_uri = request.build_absolute_uri(reverse('microsoft_callback'))
	query = urlencode({
		'client_id': settings.MICROSOFT_CLIENT_ID,
		'response_type': 'code',
		'redirect_uri': redirect_uri,
		'response_mode': 'query',
		'scope': 'openid profile email User.Read',
		'state': state,
	})
	return redirect(f'{_microsoft_base_url()}/authorize?{query}')


@require_GET
def microsoft_callback(request):
	if request.GET.get('error'):
		messages.error(request, 'Microsoft no autorizó el inicio de sesión.')
		return redirect('iniciar_sesion')

	state = request.GET.get('state')
	expected_state = request.session.pop('microsoft_oauth_state', None)
	if not state or state != expected_state:
		messages.error(request, 'La sesión de Microsoft expiró. Volvé a intentarlo.')
		return redirect('iniciar_sesion')

	code = request.GET.get('code')
	if not code:
		messages.error(request, 'Microsoft no devolvió un código de acceso válido.')
		return redirect('iniciar_sesion')

	redirect_uri = request.build_absolute_uri(reverse('microsoft_callback'))
	token_response = requests.post(
		f'{_microsoft_base_url()}/token',
		data={
			'client_id': settings.MICROSOFT_CLIENT_ID,
			'client_secret': settings.MICROSOFT_CLIENT_SECRET,
			'grant_type': 'authorization_code',
			'code': code,
			'redirect_uri': redirect_uri,
			'scope': 'openid profile email User.Read',
		},
		timeout=15,
	)
	if not token_response.ok:
		messages.error(request, 'No se pudo validar la respuesta de Microsoft.')
		return redirect('iniciar_sesion')

	access_token = token_response.json().get('access_token')
	profile_response = requests.get(
		'https://graph.microsoft.com/v1.0/me',
		headers={'Authorization': f'Bearer {access_token}'},
		timeout=15,
	)
	if not profile_response.ok:
		messages.error(request, 'No se pudo obtener tu perfil de Microsoft.')
		return redirect('iniciar_sesion')

	profile = profile_response.json()
	email = (profile.get('mail') or profile.get('userPrincipalName') or '').lower().strip()
	if not _is_allowed_email(email):
		messages.error(request, 'Solo se permiten cuentas Microsoft con correo Outlook o Hotmail.')
		return redirect('iniciar_sesion')

	user, created = User.objects.get_or_create(
		email=email,
		defaults={
			'username': email,
			'first_name': profile.get('givenName', ''),
			'last_name': profile.get('surname', ''),
		},
	)
	if not created:
		changed = False
		for field, value in (('first_name', profile.get('givenName', '')), ('last_name', profile.get('surname', ''))):
			if value and getattr(user, field) != value:
				setattr(user, field, value)
				changed = True
		if changed:
			user.save(update_fields=['first_name', 'last_name'])

	login(request, user, backend='django.contrib.auth.backends.ModelBackend')
	return redirect('home')


@login_required
def home(request):
	return render(request, 'usuarios/home.html')


@login_required
def generar_vale(request):
	if request.method == 'POST':
		form = ValeSolicitudForm(request.POST)
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.usuario = request.user
			solicitud.save()
			messages.success(request, 'Tu solicitud de vale fue guardada y quedó pendiente de revisión.')
			return redirect('home')
	else:
		form = ValeSolicitudForm()

	return render(request, 'usuarios/generar_vale.html', {'form': form})


@login_required
def pedir_prestamo(request):
	if request.method == 'POST':
		form = PrestamoSolicitudForm(request.POST)
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.usuario = request.user
			solicitud.save()
			messages.success(request, 'Tu pedido de préstamo fue guardado y quedó pendiente de evaluación.')
			return redirect('home')
	else:
		form = PrestamoSolicitudForm()

	return render(request, 'usuarios/pedir_prestamo.html', {'form': form})
