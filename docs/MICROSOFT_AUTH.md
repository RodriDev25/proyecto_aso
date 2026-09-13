# Inicio de sesión con Microsoft

El portal usa OAuth 2.0 y Microsoft Graph. La aplicación admite cuentas personales de Microsoft con correos `@outlook.com`, `@hotmail.com` y sus variantes `.com.py`.

## Configuración en Microsoft Entra

1. Crear un registro de aplicación en Microsoft Entra ID.
2. En **Supported account types**, seleccionar cuentas de cualquier directorio organizacional y cuentas Microsoft personales.
3. Agregar una plataforma **Web** con esta URI local:
   `http://127.0.0.1:8000/microsoft/callback/`
4. Crear un secreto de cliente y copiar su valor una sola vez.
5. En permisos de API de Microsoft Graph, habilitar permisos delegados `openid`, `profile`, `email` y `User.Read`.

## Variables de entorno

Configurar estas variables antes de iniciar Django:

```powershell
$env:MICROSOFT_CLIENT_ID = "id-de-la-aplicacion"
$env:MICROSOFT_CLIENT_SECRET = "valor-del-secreto"
$env:MICROSOFT_TENANT = "common"
python manage.py runserver 127.0.0.1:8000
```

La sesión activa del navegador puede permitir que Microsoft no vuelva a pedir credenciales. El comportamiento depende de la sesión, cookies, consentimiento y políticas de Microsoft; la aplicación no puede saltarse esas políticas.

Las tablas de `usuarios` se crean con:

```powershell
python manage.py migrate
```