import os
import zipfile
import tarfile
import gzip
import shutil
import tempfile
import mimetypes

from django.utils.timezone import now
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import * 
from users.server_core import *  # Import your function
from users.database import *  # Import your function
from django.db import connection
from users.function import *  # Import your function
from django.contrib.auth.hashers import make_password
from .function_file import *
from django.http import JsonResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from urllib.parse import urlparse, unquote
from whm.decorators import * 
from django.core.exceptions import SuspiciousFileOperation
import secrets
from django.http import Http404
from django.urls import reverse
from urllib.parse import urlencode


@login_required
def home(request):
    user_settings = UserSettings.objects.filter(userid=request.user.id).first()
    
    # Prepare settings dictionary (handle case if user_settings is None)
    settings_data = {
        'font_size': user_settings.font_size if user_settings else '14',
        'hide_hiden_file': user_settings.hide_hiden_file if user_settings else 0,
        'hide_folder_size': user_settings.hide_folder_size if user_settings else 0,
        'two_step': user_settings.two_step if user_settings else 0,
        'api': user_settings.api if user_settings else 0,
    }
    
    return render(request, 'file_manager/file_manager.html', {'my_settings': settings_data})

    
    
@login_required
def php_editor(request):
    user_settings = UserSettings.objects.filter(userid=request.user.id).first()

    settings_data = {
        'font_size': user_settings.font_size if user_settings else '13',
        'hide_hiden_file': user_settings.hide_hiden_file if user_settings else 0,
        'two_step': user_settings.two_step if user_settings else 0,
        'api': user_settings.api if user_settings else 0,
    }

    username_string = request.user.username
    raw_file = (
        request.GET.get('file')
        or request.POST.get('file', '')
    ).strip()

    if not raw_file:
        return JsonResponse(
            {'status': 'error', 'message': 'No file specified.'},
            status=400,
        )

    try:
        base_dir = (Path('/home') / username_string).resolve(strict=True)

        # Compatibility for the file manager's absolute URI format.
        # Only an absolute path inside this user's home is accepted.
        if Path(raw_file).is_absolute():
            absolute_candidate = Path(raw_file).resolve(strict=False)
            try:
                relative_file = absolute_candidate.relative_to(base_dir)
            except ValueError as exc:
                raise SuspiciousFileOperation(
                    'path is outside the user home'
                ) from exc
        else:
            relative_file = raw_file

        # Final canonical, symlink-aware confinement check.
        file_path = confined_user_path(username_string, relative_file)

    except (SuspiciousFileOperation, OSError):
        return JsonResponse(
            {'status': 'error', 'message': 'Access denied.'},
            status=403,
        )

    if not file_path.is_file():
        return JsonResponse(
            {'status': 'error', 'message': 'File not found.'},
            status=404,
        )

    file_name = file_path.name
    ext = file_path.suffix.lower().lstrip('.')
    if ext == 'js':
        ext = 'javascript'
    elif file_name == '.htaccess':
        ext = 'apache_conf'
    elif ext == 'py':
        ext = 'python'

    base_url = f'{request.scheme}://{request.get_host()}'

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        new_content = request.POST.get('content')
        if new_content is None:
            return JsonResponse(
                {'status': 'error', 'message': 'No content provided.'},
                status=400,
            )

        try:
            file_path.write_text(new_content, encoding='utf-8')

            if file_name == '.htaccess':
                auto_restart_litespeed = int(
                    AppSettings.objects.filter(
                        setting_key='auto_restart_litespeed'
                    ).values_list('setting_value', flat=True).first() or 0
                )
                SERVER_TYPE = get_server_type()
                if auto_restart_litespeed == 1 and SERVER_TYPE == 'openlitespeed':
                    restart_openlitespeed()

            return JsonResponse({
                'status': 'success',
                'message': 'File saved successfully.',
            })
        except OSError:
            return JsonResponse(
                {'status': 'error', 'message': 'Unable to save file.'},
                status=500,
            )

    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        messages.error(request, 'Unable to read this file.')
        return redirect('/')

    return render(request, 'file_manager/code_editor.html', {
        'ext': ext,
        'file': str(file_path),
        'name': file_name,
        'base_url': base_url,
        'content': content,
        'my_settings': settings_data,
    })




@login_required
def view(request):
    user_settings = UserSettings.objects.filter(userid=request.user.id).first()
    settings_data = {
        'font_size': user_settings.font_size if user_settings else '13',
        'hide_hiden_file': user_settings.hide_hiden_file if user_settings else 0,
        'two_step': user_settings.two_step if user_settings else 0,
        'api': user_settings.api if user_settings else 0,
    }

    username_string = request.user.username
    raw_file = (request.GET.get('file') or request.POST.get('file', '')).strip()
    if not raw_file:
        return JsonResponse(
            {'status': 'error', 'message': 'No file specified.'},
            status=400,
        )

    try:
        base_dir = (Path('/home') / username_string).resolve(strict=True)

        # Compatibility with the file manager's absolute path format.
        # Absolute paths are accepted only when they resolve below this user's home.
        if Path(raw_file).is_absolute():
            absolute_candidate = Path(raw_file).resolve(strict=False)
            relative_file = absolute_candidate.relative_to(base_dir)
        else:
            relative_file = raw_file

        file_path = confined_user_path(username_string, relative_file)
    except (SuspiciousFileOperation, ValueError, OSError):
        return JsonResponse(
            {'status': 'error', 'message': 'Access denied.'},
            status=403,
        )

    if not file_path.is_file():
        return JsonResponse(
            {'status': 'error', 'message': 'File not found.'},
            status=404,
        )

    relative_path = file_path.relative_to(base_dir).as_posix()
    file_name = file_path.name
    extension = file_path.suffix.lower().lstrip('.')
    mime_type = mimetypes.guess_type(file_name)[0] or 'application/octet-stream'

    # Images must be served as media, not decoded as UTF-8 source text.
    if mime_type.startswith('image/'):
        file_url = reverse('media_viewer') + '?' + urlencode({
            'path': relative_path,
        })
        return render(request, 'file_manager/image_view.html', {
            'file_url': file_url,
            'name': file_name,
            'ext': extension,
        })

    try:
        raw_content = file_path.read_bytes()
    except OSError:
        return JsonResponse(
            {'status': 'error', 'message': 'Unable to read file.'},
            status=500,
        )

    # NUL bytes or invalid UTF-8 indicate a binary/non-source file.
    is_binary = b'\x00' in raw_content[:8192]
    try:
        content = raw_content.decode('utf-8')
    except UnicodeDecodeError:
        is_binary = True
        content = ''

    download_url = reverse('download') + '?' + urlencode({
        'file': relative_path,
    })

    if is_binary:
        return render(request, 'file_manager/binary_file.html', {
            'name': file_name,
            'size': len(raw_content),
            'mime_type': mime_type,
            'download_url': download_url,
        })

    if extension == 'js':
        editor_ext = 'javascript'
    elif extension == 'htaccess' or file_name == '.htaccess':
        editor_ext = 'apache_conf'
    else:
        editor_ext = extension

    # Optional editing is allowed only for valid UTF-8 text.
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        new_content = request.POST.get('content')
        if new_content is None:
            return JsonResponse(
                {'status': 'error', 'message': 'No content provided.'},
                status=400,
            )

        has_permission, message = check_file_permission(str(file_path), username_string)
        if not has_permission:
            return JsonResponse(
                {'status': 'error', 'message': message},
                status=403,
            )

        try:
            file_path.write_text(new_content, encoding='utf-8')
        except OSError:
            return JsonResponse(
                {'status': 'error', 'message': 'Unable to save file.'},
                status=500,
            )

        return JsonResponse({'status': 'success', 'message': 'File saved.'})

    return render(request, 'file_manager/view.html', {
        'ext': editor_ext,
        # Use a user-relative path; do not disclose the absolute server path.
        'file': relative_path,
        'base_url': f'{request.scheme}://{request.get_host()}',
        'name': file_name,
        'content': content,
        'my_settings': settings_data,
    })

    

@login_required
def file_folder_list(request):
    user_settings = UserSettings.objects.filter(userid=request.user.id).first()
    folder_zise_hide = user_settings.hide_folder_size if user_settings else 0
    hiden_file = user_settings.hide_hiden_file if user_settings else 0

    directory = request.GET.get('directory', '')
    username_string = request.user.username

    # Preserve the old UI behavior: '/' means the current user's home.
    # Only the exact root value is normalized; traversal values are untouched
    # and are still rejected by confined_user_path().
    if directory in ('', '/', '.'):
        directory = ''

    try:
        requested_path = confined_user_path(username_string, directory)
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Access denied.'},
            status=403,
        )

    if not requested_path.exists() or not requested_path.is_dir():
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Directory does not exist or is not accessible.',
            },
            status=404,
        )

    base_dir = Path('/home') / username_string

    # Keep the rest of your existing extension_icons and listing code here.


    extension_icons = {
        'php': '/media/icon/phpcode.svg', 'html': '/media/icon/html.svg', 'txt': '/media/icon/text.svg',
        'text': '/media/icon/text.svg', 'zip': '/media/icon/zip.svg', 'tar': '/media/icon/zip.svg',
        'gz': '/media/icon/zip.svg', 'rar': '/media/icon/zip.svg', '7z': '/media/icon/zip.svg',
        'jpg': '/media/icon/image.svg', 'jpeg': '/media/icon/image.svg', 'png': '/media/icon/image.svg',
        'gif': '/media/icon/image.svg', 'bmp': '/media/icon/image.svg', 'webp': '/media/icon/image.svg',
        'tiff': '/media/icon/image.svg', 'ico': '/media/icon/image.svg', 'svg': '/media/icon/image.svg',
        'mp3': '/media/icon/audio.svg', 'wav': '/media/icon/audio.svg', 'flac': '/media/icon/audio.svg',
        'mp4': '/media/icon/video.svg', 'avi': '/media/icon/video.svg', 'mov': '/media/icon/video.svg',
        'mkv': '/media/icon/video.svg', 'webm': '/media/icon/video.svg',
    }
    default_file_icon = '/media/icon/other.svg'
    folder_icon = '/media/icon/folder-file.svg'
    public_html_icon = '/media/icon/public.svg'

    try:
        entries = []
        with os.scandir(requested_path) as it:
            for entry in it:
                # Do not follow links while listing or calculating folder sizes.
                if entry.is_symlink():
                    continue

                if hiden_file == 1 and entry.name.startswith('.'):
                    continue

                if entry.is_dir(follow_symlinks=False):
                    icon = public_html_icon if entry.name == 'public_html' else folder_icon
                    if folder_zise_hide == 0:
                        size_display_value = size_display(get_folder_size(entry.path))
                    else:
                        size_display_value = size_display(entry.stat(follow_symlinks=False).st_size)
                    file_extension = 'folder'
                else:
                    file_extension = entry.name.split('.')[-1].lower()
                    icon = extension_icons.get(file_extension, default_file_icon)
                    size_display_value = size_display(entry.stat(follow_symlinks=False).st_size)

                entry_path = Path(entry.path)
                entries.append({
                    'name': entry.name,
                    'is_dir': entry.is_dir(follow_symlinks=False),
                    'path': os.path.relpath(str(entry_path), str(base_dir)),
                    'size': size_display_value,
                    'modified_time': datetime.fromtimestamp(
                        entry.stat(follow_symlinks=False).st_mtime
                    ).isoformat(),
                    'permissions': oct(entry.stat(follow_symlinks=False).st_mode)[-3:],
                    'icon': icon,
                    'extension': file_extension,
                })

        entries.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
        return JsonResponse({'status': 'success', 'entries': entries})
    except (OSError, SuspiciousFileOperation) as exc:
        return JsonResponse(
            {'status': 'error', 'message': f'Error listing directory: {exc}'},
            status=500,
        )
       
@login_required
def folder_list(request):
    directory = request.GET.get('directory', '')
    username_string = request.user.username

    if directory in ('', '/', '.'):
        directory = ''
    
    
    try:
        requested_path = confined_user_path(username_string, directory)
    except SuspiciousFileOperation:
        return JsonResponse({'status': 'error', 'message': 'Access denied.'}, status=403)

    if not requested_path.exists() or not requested_path.is_dir():
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Directory does not exist or is not accessible.',
            },
            status=404,
        )

    base_dir = Path('/home') / username_string

    try:
        entries = []
        with os.scandir(requested_path) as it:
            for entry in it:
                # Do not follow symlinked directories outside the user home.
                if entry.is_symlink():
                    continue

                if entry.is_dir(follow_symlinks=False):
                    entries.append({
                        'name': entry.name,
                        'is_dir': True,
                        'path': os.path.relpath(entry.path, str(base_dir)),
                    })

        entries.sort(key=lambda x: x['name'].lower())
        return JsonResponse({'status': 'success', 'entries': entries})
    except OSError as exc:
        return JsonResponse(
            {'status': 'error', 'message': f'Error listing directory: {exc}'},
            status=500,
        )

        
        
@login_required
def file_action(request):
    action = request.POST.get('action', '').strip().lower()
    file_name = request.POST.get('file_name', '').strip()
    target_name = request.POST.get('target_name', '').strip()
    permissions = request.POST.get('permission', '000').strip()
    selected_items = request.POST.getlist('selected_items[]')
    parent = request.POST.get('base', '').strip()
    username_string = request.user.username
    base_dir = Path('/home') / username_string

    allowed_actions = {
        'rename', 'delete', 'fix-permission', 'permission',
        'new_file', 'new_folder', 'copy', 'move', 'trash',
        'unzip', 'compress',
    }
    
    
    if action not in allowed_actions:
        return JsonResponse({'status': 'error', 'message': 'Invalid action.'}, status=400)

    home_prefix = f'/home/{username_string}'
    
    if target_name in ('', '/', '//'):
        target_path = base_dir
    else:
        if target_name == home_prefix:
            target_name = ''

        elif target_name.startswith(home_prefix + '/'):
            target_name = target_name[len(home_prefix):].lstrip('/')

        elif target_name.startswith('/'):
            target_name = target_name.lstrip('/')

        if target_name in ('', '.', '/'):
            target_path = base_dir
        else:
            try:
                target_path = confined_user_path(
                    username_string,
                    target_name
                )
            except (SuspiciousFileOperation, OSError, ValueError):
                return JsonResponse(
                    {
                        'status': 'error',
                        'message': 'Invalid target path.'
                    },
                    status=400
                )

    def relative_name(path):
        """Return a normalized relative name for legacy helper functions."""
        relative = os.path.relpath(str(path), str(base_dir))
        return '' if relative == '.' else relative

    def validate_path(value, allow_home=False):
        value = str(value or '').strip()

        # '/' and '//' represent the user's home directory.
        if value in ('/', '//'):
            return base_dir

        # Empty value is only valid when the caller explicitly allows home.
        if value == '':
            if allow_home:
                return base_dir
            raise SuspiciousFileOperation('file path is required')

        # Convert the authenticated user's absolute home path into
        # a relative path before calling the canonical security helper.
        if value == home_prefix:
            value = ''

        elif value.startswith(home_prefix + '/'):
            value = value[len(home_prefix):].lstrip('/')

        elif value.startswith('/'):
            # Legacy UI paths such as /folder/file.
            value = value.lstrip('/')

        if value in ('', '.', '/'):
            if allow_home:
                return base_dir
            raise SuspiciousFileOperation('file path is required')

        return confined_user_path(username_string, value)

    try:
        # Validate every selected source before any mutation occurs.
        selected_paths = []
        for selected in selected_items:
            selected_path = validate_path(selected)
            selected_paths.append((selected, selected_path))

        file_path = None
        if file_name:
            file_path = validate_path(file_name)

        # Check the panel's existing account-level permission policy first.
        has_permission, message = check_file_folder_permission(
            str(base_dir), username_string
        )
        if not has_permission:
            return JsonResponse({'status': 'error', 'message': message}, status=403)

        # The legacy helpers receive normalized relative names, not raw paths.
        target_relative = relative_name(target_path)
        file_relative = relative_name(file_path) if file_path else ''

        if action == 'rename':
            if file_path is None or not file_path.exists():
                return JsonResponse({'status': 'error', 'message': 'File or folder does not exist.'}, status=404)
            if target_path == base_dir or target_path.exists():
                return JsonResponse({'status': 'error', 'message': 'Target name already exists.'}, status=400)
            if file_path.is_symlink() or target_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Symlinks are not allowed.'}, status=400)
            os.rename(str(file_path), str(target_path))
            return JsonResponse({'status': 'success', 'message': 'Renamed successfully.'})

        if action == 'delete':
            sources = selected_paths or ([(file_name, file_path)] if file_path else [])
            if not sources:
                return JsonResponse({'status': 'error', 'message': 'No file specified.'}, status=400)
            for _, source_path in sources:
                if source_path == base_dir or source_path.is_symlink():
                    return JsonResponse({'status': 'error', 'message': 'Invalid delete target.'}, status=400)
                if not source_path.exists():
                    return JsonResponse({'status': 'error', 'message': 'File or folder does not exist.'}, status=404)
                message = f_delete(username_string, relative_name(source_path))
                if isinstance(message, str) and message.startswith('Error'):
                    return JsonResponse({'status': 'error', 'message': message}, status=400)
            return JsonResponse({'status': 'success', 'message': 'Deleted successfully.'})

        if action == 'fix-permission':
            sources = selected_paths or ([(file_name, file_path)] if file_path else [])
            if not sources:
                return JsonResponse({'status': 'error', 'message': 'No file specified.'}, status=400)
            for _, source_path in sources:
                if source_path == base_dir or source_path.is_symlink():
                    continue
                if not source_path.exists():
                    return JsonResponse({'status': 'error', 'message': 'File or folder does not exist.'}, status=404)
                set_permissions_and_ownership(str(source_path), username_string)
            return JsonResponse({'status': 'success', 'message': 'Permission set successfully.'})

        if action == 'permission':
            if file_path is None or file_path == base_dir or not file_path.exists() or file_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Invalid permission target.'}, status=400)
            if len(permissions) != 3 or any(ch not in '01234567' for ch in permissions):
                return JsonResponse({'status': 'error', 'message': 'Invalid permission value.'}, status=400)
            os.chmod(str(file_path), int(permissions, 8))
            return JsonResponse({'status': 'success', 'message': 'Permissions set successfully.'})

        if action in ('new_file', 'new_folder'):
            if target_path == base_dir or not is_valid_filename(target_path.name):
                return JsonResponse({'status': 'error', 'message': 'Invalid name.'}, status=400)
            if target_path.exists() or target_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'The target already exists.'}, status=400)
            if action == 'new_file':
                target_path.touch(exist_ok=False)
            else:
                target_path.mkdir(parents=False, exist_ok=False)
            set_permissions_and_ownership(str(target_path), username_string)
            return JsonResponse({'status': 'success', 'message': 'Created successfully.'})

        if action in ('copy', 'move'):
            sources = selected_paths or ([(file_name, file_path)] if file_path else [])
            if not sources:
                return JsonResponse({'status': 'error', 'message': 'No file specified.'}, status=400)
                
                
            if target_path.is_symlink():
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid target directory.'
                }, status=400)
            # Automatically create target directory if it does not exist.
            if not target_path.exists():
                try:
                    target_path.mkdir(
                        parents=True,
                        exist_ok=True
                    )

                    # Set correct ownership and permissions.
                    set_permissions_and_ownership(
                        str(target_path),
                        username_string
                    )

                except (OSError, ValueError) as exc:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Unable to create target directory: {exc}'
                    }, status=400)

                    
            if not target_path.is_dir():
                return JsonResponse({'status': 'error', 'message': 'Invalid target directory.'}, status=400)
                
            for _, source_path in sources:
                if source_path.is_symlink() or not source_path.exists():
                    return JsonResponse({'status': 'error', 'message': 'Invalid source path.'}, status=400)
                helper = f_copy if action == 'copy' else f_move
                message = helper(username_string, relative_name(source_path), target_relative)
                if isinstance(message, str) and message.startswith('Error'):
                    return JsonResponse({'status': 'error', 'message': message}, status=400)
            return JsonResponse({'status': 'success', 'message': 'Copied successfully.' if action == 'copy' else 'Moved successfully.'})

        if action == 'trash':
            sources = selected_paths or ([(file_name, file_path)] if file_path else [])
            if not sources:
                return JsonResponse({'status': 'error', 'message': 'No file specified.'}, status=400)
            trash_path = base_dir / '.trash'
            trash_path.mkdir(mode=0o700, exist_ok=True)
            if trash_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Invalid trash directory.'}, status=400)
            for _, source_path in sources:
                if source_path == base_dir or source_path.is_symlink() or not source_path.exists():
                    return JsonResponse({'status': 'error', 'message': 'Invalid trash source.'}, status=400)
                message = f_move(username_string, relative_name(source_path), '.trash')
                if isinstance(message, str) and message.startswith('Error'):
                    return JsonResponse({'status': 'error', 'message': message}, status=400)
            return JsonResponse({'status': 'success', 'message': 'Trash successfully.'})

        if action == 'unzip':
            if file_path is None or not file_path.is_file() or file_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Archive not found.'}, status=404)
            target_path.mkdir(parents=True, exist_ok=True)
            if target_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Invalid extraction directory.'}, status=400)
                
            extracted_items = []
            
            def validate_member(member_name):
                # Reuse the canonical helper for every archive member.
                member_target = target_path.relative_to(base_dir) / member_name
                return confined_user_path(username_string, str(member_target))

            if file_name.lower().endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as archive:
                    for info in archive.infolist():
                        validate_member(info.filename)
                    archive.extractall(str(target_path))
                    extracted_items = archive.namelist()
            elif file_name.lower().endswith(('.tar.gz', '.tgz')):
                with tarfile.open(file_path, 'r:gz') as archive:
                    for member in archive.getmembers():
                        if member.issym() or member.islnk():
                            raise SuspiciousFileOperation('archive links are not allowed')
                        validate_member(member.name)
                    archive.extractall(str(target_path))
                    extracted_items = archive.getnames()
            elif file_name.lower().endswith('.gz'):
                output_name = Path(file_path.name[:-3]).name
                output_path = confined_user_path(
                    username_string,
                    str(target_path.relative_to(base_dir) / output_name),
                )
                with gzip.open(file_path, 'rb') as source, output_path.open('wb') as dest:
                    shutil.copyfileobj(source, dest)
                    
                extracted_items = [output_name]    
            else:
                return JsonResponse({'status': 'error', 'message': 'Unsupported archive type.'}, status=400)
                
                
            # ---------------------------------------------------------
            # Apply ownership + permissions to extracted items.
            # Uses your NEW recursive function.
            # ---------------------------------------------------------
            for item in extracted_items:

                extracted_path = target_path / item

                try:
                    # Make sure extracted path is still inside
                    # authenticated user's home directory.
                    extracted_path = confined_user_path(
                        username_string,
                        str(extracted_path.relative_to(base_dir))
                    )
                except (SuspiciousFileOperation, OSError, ValueError):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid extracted path.'
                    }, status=400)

                if not extracted_path.exists():
                    continue

                # Do not operate on symlinks.
                if extracted_path.is_symlink():
                    continue

                # Your new recursive ownership/permission function.
                success = set_permissions_and_ownership(
                    str(extracted_path),
                    username_string
                )

                if not success:
                    return JsonResponse({
                        'status': 'error',
                        'message': (
                            'Archive extracted, but failed to set '
                            'ownership or permissions.'
                        )
                    }, status=500)    

            return JsonResponse({'status': 'success', 'message': 'Archive extracted successfully.'})

        if action == 'compress':
            parent_path = validate_path(parent, allow_home=True)
            if parent_path.is_symlink():
                return JsonResponse({'status': 'error', 'message': 'Invalid parent path.'}, status=400)
            sources = selected_paths or ([(file_name, file_path)] if file_path else [])
            if not sources:
                return JsonResponse({'status': 'error', 'message': 'No file specified.'}, status=400)
            message = f_compress(
                username_string,
                relative_name(parent_path),
                relative_name(sources[0][1]),
                target_relative,
                [relative_name(path) for _, path in sources],
            )
            if isinstance(message, str) and message.startswith('Error'):
                return JsonResponse({'status': 'error', 'message': message}, status=400)
            return JsonResponse({'status': 'success', 'message': 'Compress successfully.'})

    except (SuspiciousFileOperation, OSError, ValueError) as exc:
        return JsonResponse({'status': 'error', 'message': f'Invalid or inaccessible path: {exc}{target_path}'}, status=400)
    except Exception as exc:
        return JsonResponse({'status': 'error', 'message': f'Error performing action: {exc}'}, status=500)
         
        
@login_required
def download(request):
    file_value = request.GET.get('file', '')
    if not file_value:
        return JsonResponse(
            {'status': 'error', 'message': 'No file specified.'},
            status=400,
        )

    username_string = request.user.username

    try:
        # confined_user_path() must resolve the path and ensure it remains
        # below /home/<username>. Do not rebuild this path afterward.
        file_path = confined_user_path(username_string, file_value)
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Unauthorized access.'},
            status=403,
        )

    # Use is_file(), not only exists(), so directories cannot be downloaded.
    if not file_path.is_file():
        return JsonResponse(
            {'status': 'error', 'message': 'File not found.'},
            status=404,
        )

    try:
        response = FileResponse(
            open(file_path, 'rb'),
            content_type='application/force-download',
        )
        response['Content-Disposition'] = f'attachment; filename="{file_path.name}"'
        return response
    except OSError:
        return JsonResponse(
            {'status': 'error', 'message': 'File could not be opened.'},
            status=404,
        )

 

 
@login_required
def upload(request):
    if request.method != 'POST' or 'file' not in request.FILES:
        return JsonResponse(
            {'status': 'error', 'message': 'No file uploaded.'},
            status=400,
        )

    uploaded_file = request.FILES['file']
    target_name = request.POST.get('target_name', '').strip()
    username_string = request.user.username

    try:
        base_dir = Path('/home') / username_string
        target_path = confined_user_path(username_string, target_name)
        filename = safe_upload_filename(uploaded_file.name)
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid upload path or filename.'},
            status=400,
        )

    user_data = get_user_data_by_id(request.user.id) or {}
    user_package = Package.objects.filter(id=user_data.get('pkg_id')).first()
    disk_limit = user_package.disk_space * 1024 * 1024 if user_package else 0

    database_names = get_user_database_info(username_string)
    total_size = calculate_total_database_size(database_names)
    disk = get_disk_usage(str(base_dir))
    email_disk = get_disk_usage(f'/home/vmail/{username_string}')
    total_bytes = (
        human_readable_to_bytes(disk)
        + total_size
        + human_readable_to_bytes(email_disk)
        + uploaded_file.size
    )

    if user_package and user_package.disk_space != 0 and total_bytes > disk_limit:
        return JsonResponse(
            {
                'status': 'error',
                'message': 'Disk quota exceeded. Please upgrade your package or free up space.',
            },
            status=403,
        )

    has_permission, message = check_file_folder_permission(
        str(base_dir), username_string
    )
    if not has_permission:
        return JsonResponse(
            {'status': 'error', 'message': message},
            status=403,
        )

    temporary_path = None
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        if target_path.is_symlink():
            raise SuspiciousFileOperation('upload directory is a symlink')

        final_path = confined_user_path(
            username_string,
            str(target_path.relative_to(base_dir) / filename),
        )

        # Never overwrite a directory or symlink.
        if final_path.is_dir() or final_path.is_symlink():
            raise SuspiciousFileOperation('invalid final upload path')

        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix='.olspanel-upload-',
            suffix='.part',
            dir=str(target_path),
        )
        os.close(file_descriptor)
        temporary_path = Path(temporary_name)

        with temporary_path.open('wb') as output:
            for chunk in uploaded_file.chunks():
                output.write(chunk)
        os.chmod(temporary_path, 0o600)

        # This overwrites the existing regular file with the same filename.
        os.replace(str(temporary_path), str(final_path))
        temporary_path = None
        set_permissions_and_ownership(str(final_path), username_string)

        storage = FileSystemStorage(location=str(target_path))
        return JsonResponse(
            {
                'status': 'success',
                'file_name': filename,
                'file_size': uploaded_file.size,
                'file_url': storage.url(filename),
            },
            status=200,
        )

    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid upload path or filename.'},
            status=400,
        )
    except OSError as exc:
        return JsonResponse(
            {'status': 'error', 'message': f'Upload failed: {exc}'},
            status=500,
        )
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
  


@login_required
def upload_db(request, db_name):
    if request.method != 'POST' or 'file' not in request.FILES:
        return JsonResponse(
            {'status': 'error', 'message': 'No file uploaded.'},
            status=400,
        )

    # Database names are later passed to import_database(); do not allow
    # paths, shell metacharacters, or arbitrary SQL identifier text here.
    if not re.fullmatch(r'[A-Za-z0-9_]+', str(db_name or '')):
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid database name.'},
            status=400,
        )

    uploaded_file = request.FILES['file']
    username_string = request.user.username
    base_dir = Path('/home') / username_string

    try:
        # The temporary directory is fixed, but still pass it through the
        # same canonical confinement control used by other file operations.
        target_path = confined_user_path(username_string, 'tmp')
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid upload directory.'},
            status=400,
        )

    has_permission, message = check_file_folder_permission(
        str(base_dir), username_string
    )
    if not has_permission:
        return JsonResponse({'status': 'error', 'message': message}, status=403)

    # Generate the stored name from a timestamp, never from the user path.
    original_name = str(uploaded_file.name or '')
    file_extension = Path(original_name).suffix.lower()
    if not re.fullmatch(r'\.[a-z0-9]{1,10}', file_extension):
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid database file type.'},
            status=400,
        )

    timestamp = now().strftime('%Y%m%d_%H%M%S_%f') + file_extension
    saved_path = None

    try:
        target_path.mkdir(parents=True, exist_ok=True)
        if target_path.is_symlink():
            raise SuspiciousFileOperation('upload directory is a symlink')

        storage = FileSystemStorage(location=str(target_path))
        saved_name = storage.save(timestamp, uploaded_file)

        # Re-check the actual storage result; storage backends may rename a
        # collision, so never assume the requested timestamp is the final name.
        saved_path = confined_user_path(
            username_string,
            str(target_path.relative_to(base_dir) / saved_name),
        )
        if saved_path.is_symlink() or not saved_path.is_file():
            raise SuspiciousFileOperation('invalid stored upload path')

        set_permissions_and_ownership(str(saved_path), username_string)

        try:
            import_database(username_string, str(saved_path), db_name)
        except Exception:
            # Do not leave an uploaded database dump behind after a failed
            # import; it may contain sensitive data.
            saved_path.unlink(missing_ok=True)
            raise

        return JsonResponse(
            {
                'status': 'success',
                'file_name': original_name,
                'file_size': uploaded_file.size,
                'file_url': storage.url(saved_name),
            },
            status=200,
        )

    except SuspiciousFileOperation:
        if saved_path is not None:
            saved_path.unlink(missing_ok=True)
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid upload path.'},
            status=400,
        )
    except OSError:
        if saved_path is not None:
            saved_path.unlink(missing_ok=True)
        return JsonResponse(
            {'status': 'error', 'message': 'Upload failed.'},
            status=500,
        )
    except Exception:
        # Keep database/import internals out of the HTTP response.
        return JsonResponse(
            {'status': 'error', 'message': 'Database import failed.'},
            status=500,
        )



@login_required
def export_db(request, db_name):
    username_string = request.user.username

    # Keep the database name as a single safe identifier. This prevents it
    # from becoming a path, shell argument, or SQL-fragment through this view.
    if not re.fullmatch(r'[A-Za-z0-9_]+', str(db_name or '')):
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid database name.'},
            status=400,
        )

    base_dir = Path('/home') / username_string

    try:
        # The helper must return a canonical path confined to this user home.
        target_path = confined_user_path(username_string, 'tmp')
        file_path = confined_user_path(
            username_string,
            str(target_path.relative_to(base_dir) / f'{db_name}.sql'),
        )
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid export path.'},
            status=400,
        )

    has_permission, message = check_file_folder_permission(
        str(base_dir), username_string
    )
    if not has_permission:
        return JsonResponse({'status': 'error', 'message': message}, status=403)

    try:
        target_path.mkdir(parents=True, exist_ok=True)
        if target_path.is_symlink() or file_path.is_symlink():
            return JsonResponse(
                {'status': 'error', 'message': 'Invalid export path.'},
                status=400,
            )

        # export_database() must itself use shell=False/argument arrays or a
        # database API. Do not use shell=True with user-controlled values.
        export_database(username_string, str(file_path), db_name)

        if not file_path.is_file():
            return JsonResponse(
                {'status': 'error', 'message': 'Export did not create a file.'},
                status=500,
            )

        set_permissions_and_ownership(str(file_path), username_string)
        return JsonResponse(
            {'status': 'success', 'file_path': str(file_path)},
            status=200,
        )

    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid export path.'},
            status=400,
        )
    except OSError:
        return JsonResponse(
            {'status': 'error', 'message': 'Unable to create export file.'},
            status=500,
        )
    except Exception:
        # Do not expose database, credentials, or command details to clients.
        return JsonResponse(
            {'status': 'error', 'message': 'Database export failed.'},
            status=500,
        )

        



@login_required
def upload_from_url(request):
    if request.method != 'POST':
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid request method.'},
            status=405,
        )

    file_url = request.POST.get('file_url', '').strip()
    target_name = request.POST.get('target_name', '').strip()
    if not file_url:
        return JsonResponse(
            {'status': 'error', 'message': 'No URL provided.'},
            status=400,
        )

    username_string = request.user.username
    base_dir = Path('/home') / username_string

    try:
        # This helper must reject non-public HTTP(S) URLs, internal IPs,
        # redirects, oversized responses, and unsafe output paths.
        target_path = confined_user_path(username_string, target_name)
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid destination path.'},
            status=400,
        )

    has_permission, message = check_file_folder_permission(
        str(base_dir), username_string
    )
    if not has_permission:
        return JsonResponse({'status': 'error', 'message': message}, status=403)

    parsed_url = urlparse(file_url)
    filename = unquote(os.path.basename(parsed_url.path)) or 'downloaded_file'

    try:
        filename = safe_upload_filename(filename)
    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid remote filename.'},
            status=400,
        )

    user_data = get_user_data_by_id(request.user.id) or {}
    user_package = Package.objects.filter(id=user_data.get('pkg_id')).first()
    disk_limit = user_package.disk_space * 1024 * 1024 if user_package else 0

    temporary_path = None
    try:
        target_path.mkdir(parents=True, exist_ok=True)
        if target_path.is_symlink():
            raise SuspiciousFileOperation('destination is a symlink')

        # Do not create this file before calling the helper: the hardened
        # downloader creates it with mode 0600 and refuses existing paths.
        temporary_path = target_path / (
            f'.olspanel-download-{secrets.token_hex(16)}.part'
        )
        download_file_with_wget(file_url, str(temporary_path))
        file_size = temporary_path.stat().st_size

        database_names = get_user_database_info(username_string)
        total_size = calculate_total_database_size(database_names)
        disk = get_disk_usage(str(base_dir))
        email_disk = get_disk_usage(f'/home/vmail/{username_string}')
        total_bytes = (
            human_readable_to_bytes(disk)
            + total_size
            + human_readable_to_bytes(email_disk)
            + file_size
        )

        if user_package and user_package.disk_space != 0 and total_bytes > disk_limit:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Disk quota exceeded. Please upgrade your package or free up space.',
                },
                status=403,
            )

        storage = FileSystemStorage(location=str(target_path))

        # Keep the original remote filename. Do not call
        # get_available_name(), because that intentionally creates a
        # collision-suffixed filename instead of overwriting.
        saved_name = filename
        final_path = confined_user_path(
            username_string,
            str(target_path.relative_to(base_dir) / saved_name),
        )

        # Existing regular files may be replaced. Directories and symlink
        # paths are never valid upload targets.
        if final_path.is_symlink() or final_path.is_dir():
            raise SuspiciousFileOperation('invalid final upload path')

        # os.replace() atomically overwrites an existing regular file and
        # does not follow a symlink at the final path.
        os.replace(str(temporary_path), str(final_path))
        temporary_path = None
        set_permissions_and_ownership(str(final_path), username_string)

        return JsonResponse(
            {
                'status': 'success',
                'file_name': saved_name,
                'file_size': file_size,
                'file_url': storage.url(saved_name),
            },
            status=200,
        )

    except SuspiciousFileOperation:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid destination or filename.'},
            status=400,
        )
    except OSError:
        return JsonResponse(
            {'status': 'error', 'message': 'Remote upload failed.'},
            status=400,
        )
    except Exception:
        return JsonResponse(
            {'status': 'error', 'message': 'Remote upload failed.'},
            status=400,
        )
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
  
@login_required
def media_viewer(request):
    path_value = request.GET.get('path', '').strip()
    if not path_value:
        raise Http404('No file path specified.')

    username_string = request.user.username

    try:
        # This helper must canonicalize the path and keep it below
        # /home/<username>. Do not rebuild file_path afterward.
        file_path = confined_user_path(username_string, path_value)
    except SuspiciousFileOperation:
        raise Http404('File not found or access denied.')

    # Serve only regular files. Paths resolving outside the user home are
    # rejected by confined_user_path().
    if not file_path.is_file():
        raise Http404('File not found or access denied.')

    ext = file_path.suffix.lower()
    content_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
    }
    content_type = content_types.get(ext, 'application/octet-stream')

    try:
        return FileResponse(
            file_path.open('rb'),
            content_type=content_type,
        )
    except OSError:
        raise Http404('File not found or access denied.')

    
    
@alogin_required
def upload_from_url_bk(request):
    if request.method == 'POST':
        ALLOWED_EXTENSIONS = ['.gz', '.tar', '.zip']
        file_url = request.POST.get('file_url', '').strip()
        target_name = 'backup'
        
        if not file_url:
            return JsonResponse({'status': 'error', 'message': 'No URL provided.'}, status=400)

        if target_name.startswith('/'):
            target_name = target_name[1:]
        
        username_string = request.user.username
       
        # Extract filename
        parsed_url = urlparse(file_url)
        filename = unquote(os.path.basename(parsed_url.path))
        
        if not filename:
            filename = 'downloaded_file'
            
        _, file_extension = os.path.splitext(filename)
        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            return JsonResponse({'status': 'error', 'message': f'Only {", ".join(ALLOWED_EXTENSIONS)} files are allowed.'}, status=400)


        base_dir = '/home/'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        
    
    
        target_path = os.path.join(base_dir, target_name) if target_name else base_dir
       

        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # Disk quota calculation
        temp_file_path = os.path.join(target_path, filename)
        try:
            download_file_with_wget(file_url, temp_file_path)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

        file_size = os.path.getsize(temp_file_path)

        

        fs = FileSystemStorage(location=target_path)
        file_url_saved = fs.url(filename)

        return JsonResponse({
            'status': 'success',
            'file_name': filename,
            'file_size': file_size,
            'file_url': file_url_saved
        }, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
      
      
@alogin_required
def upload_bk(request):
    if request.method == 'POST' and 'file' in request.FILES:
        ALLOWED_EXTENSIONS = ['.gz', '.tar', '.zip']
        # Get the uploaded file and other request data
        uploaded_file = request.FILES['file']  # For single file uploads
        target_name = 'backup'
        filename = uploaded_file.name
        _, file_extension = os.path.splitext(filename)
        
        if file_extension.lower() not in ALLOWED_EXTENSIONS:
            return JsonResponse({'status': 'error', 'message': f'Only {", ".join(ALLOWED_EXTENSIONS)} files are allowed.'}, status=400)
   
            

        # Ensure target_name does not start with a slash
        if target_name.startswith('/'):
            target_name = target_name[1:]

        # Define base directory and construct the target path
        username_string = request.user.username
        
        
        base_dir = '/home/'
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)                    
        
        target_path = os.path.join(base_dir, target_name) if target_name else base_dir
        

        

        # Ensure target path exists
        if not os.path.exists(target_path):
            os.makedirs(target_path)

        # Save the file to the target directory
        fs = FileSystemStorage(location=target_path)
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = os.path.join(target_path, filename)
        file_url = fs.url(filename)
        

        # Respond with success and file details
        response_data = {
            'status': 'success',
            'file_name': uploaded_file.name,
            'file_size': uploaded_file.size,
            'file_url': file_url
        }
        return JsonResponse(response_data, status=200)

    # Handle error if no file is uploaded
    return JsonResponse({'status': 'error', 'message': 'No file uploaded.'}, status=400)   


@login_required
def update_user_settings(request):
    if request.method == "POST":
        try:
              # Get or create settings for user
            settings, _ = UserSettings.objects.get_or_create(userid=request.user.id)

            if request.POST.get("font_size"):
                settings.font_size =request.POST.get("font_size")
            else:              
                settings.hide_hiden_file = 0 if request.POST.get("hide_hiden_file") != "0" else 1
                settings.hide_folder_size = 0 if request.POST.get("hide_folder_size") != "0" else 1


            # Add other fields here as needed

            settings.save()

            return JsonResponse({
                "status": "success",
                "message": "Settings updated successfully."
            })

        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Error saving settings: {str(e)}"
            }, status=500)

    return JsonResponse({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)    