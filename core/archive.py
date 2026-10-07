# -*- coding: utf-8 -*-
"""Archive extractor for ZIP, RAR, 7Z files containing PDF reports and DOCX templates."""
import io
import os
import shutil
import subprocess
import tempfile
import zipfile


def get_archiver_tool():
    """Find 7z or unrar on PATH or common Windows installation paths."""
    tool = shutil.which('7z') or shutil.which('7za') or shutil.which('unrar')
    if tool:
        return tool
    for p in [
        r"C:\Program Files\7-Zip\7z.exe",
        r"C:\Program Files (x86)\7-Zip\7z.exe",
        r"C:\Program Files\WinRAR\UnRAR.exe",
        r"C:\Program Files\WinRAR\WinRAR.exe",
    ]:
        if os.path.exists(p):
            return p
    return None


def is_archive(filename: str, file_bytes: bytes = b"") -> bool:
    """Check if file is a zip, rar, or 7z archive by name or magic bytes."""
    lower_fn = filename.lower()
    if lower_fn.endswith(('.zip', '.rar', '.7z', '.tar', '.gz')):
        return True
    if file_bytes.startswith(b'PK\x03\x04') or file_bytes.startswith(b'Rar!') or file_bytes.startswith(b'7z\xbc\xaf\x27\x1c'):
        return True
    return False


def extract_files_from_archive(archive_bytes: bytes, filename: str = "") -> list:
    """
    Extracts all .pdf and .docx files from a zip, rar, or 7z archive.
    Returns a list of tuples: [(sub_filename, file_bytes), ...]
    """
    lower_fn = filename.lower()
    results = []

    # 1. Try ZIP first (in-memory, fast, standard library)
    if lower_fn.endswith('.zip') or archive_bytes.startswith(b'PK\x03\x04'):
        try:
            with zipfile.ZipFile(io.BytesIO(archive_bytes), 'r') as zf:
                for info in zf.infolist():
                    if info.is_dir():
                        continue
                    fname = os.path.basename(info.filename)
                    if not fname or fname.startswith('.') or 'MACOSX' in info.filename:
                        continue
                    fl = fname.lower()
                    if fl.endswith('.pdf') or fl.endswith('.docx') or fl.endswith('.doc'):
                        data = zf.read(info.filename)
                        if data:
                            results.append((fname, data))
            if results:
                return results
        except Exception:
            pass

    # 2. Try rarfile if it is a RAR archive
    if lower_fn.endswith('.rar') or archive_bytes.startswith(b'Rar!'):
        try:
            import rarfile
            tool = get_archiver_tool()
            if tool:
                rarfile.UNRAR_TOOL = tool
            with rarfile.RarFile(io.BytesIO(archive_bytes)) as rf:
                for info in rf.infolist():
                    if info.isdir():
                        continue
                    fname = os.path.basename(info.filename)
                    if not fname or fname.startswith('.') or 'MACOSX' in info.filename:
                        continue
                    fl = fname.lower()
                    if fl.endswith('.pdf') or fl.endswith('.docx') or fl.endswith('.doc'):
                        data = rf.read(info.filename)
                        if data:
                            results.append((fname, data))
            if results:
                return results
        except Exception:
            pass

    # 3. Try 7-Zip CLI tool fallback (extracts .rar, .7z, .zip, etc.)
    tool = get_archiver_tool()
    if tool:
        tmp_dir = tempfile.mkdtemp()
        suffix = os.path.splitext(filename)[1] or '.archive'
        tmp_archive = os.path.join(tmp_dir, f"temp_upload{suffix}")
        try:
            with open(tmp_archive, 'wb') as f:
                f.write(archive_bytes)

            extract_dir = os.path.join(tmp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)

            cmd = [tool, 'x', tmp_archive, f"-o{extract_dir}", '-y']
            subprocess.run(cmd, capture_output=True, timeout=45)

            for root, dirs, files in os.walk(extract_dir):
                for f in files:
                    if f.startswith('.') or '__MACOSX' in root:
                        continue
                    fl = f.lower()
                    if fl.endswith('.pdf') or fl.endswith('.docx') or fl.endswith('.doc'):
                        fp = os.path.join(root, f)
                        try:
                            with open(fp, 'rb') as f_in:
                                results.append((f, f_in.read()))
                        except Exception:
                            pass
        except Exception as e:
            print(f"Archive extraction error: {e}")
        finally:
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass

    return results
