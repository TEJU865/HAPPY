"""
File Manager Tool for HAPPY
Advanced file operations with safety confirmations
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """Safe file operations for HAPPY"""

    # Dangerous operations that need confirmation
    DANGEROUS_OPERATIONS = ["delete", "overwrite", "move", "copy"]

    def __init__(self, base_path: str = "."):
        """Initialize with base working directory"""
        self.base_path = Path(base_path).resolve()
        self.confirmation_required = True

    def _is_safe_path(self, path: str) -> bool:
        """Check if path is within safe boundaries"""
        try:
            full_path = Path(path).resolve()
            # Don't allow access to system directories
            system_dirs = [
                "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
                "C:\\System32", "C:\\Users", "C:\\ProgramData"
            ]
            for sys_dir in system_dirs:
                if str(full_path).startswith(sys_dir):
                    return False
            return True
        except:
            return False

    def create_folder(self, folder_name: str) -> Dict[str, Any]:
        """Create a new folder"""
        try:
            if not self._is_safe_path(folder_name):
                return {
                    "success": False,
                    "message": "Cannot create folder in system directory",
                    "error": "Unsafe path"
                }

            path = Path(folder_name)
            path.mkdir(parents=True, exist_ok=True)

            return {
                "success": True,
                "message": f"Created folder '{folder_name}'",
                "path": str(path.resolve())
            }
        except Exception as e:
            logger.error(f"Failed to create folder {folder_name}: {e}")
            return {
                "success": False,
                "message": f"Failed to create folder '{folder_name}'",
                "error": str(e)
            }

    def delete_file(self, file_path: str, confirmed: bool = False) -> Dict[str, Any]:
        """Delete a file (requires confirmation)"""
        try:
            path = Path(file_path)

            if not path.exists():
                return {
                    "success": False,
                    "message": f"File '{file_path}' does not exist"
                }

            if not path.is_file():
                return {
                    "success": False,
                    "message": f"'{file_path}' is not a file"
                }

            if not self._is_safe_path(file_path):
                return {
                    "success": False,
                    "message": "Cannot delete system files",
                    "error": "Unsafe path"
                }

            if self.confirmation_required and not confirmed:
                return {
                    "success": False,
                    "message": f"Are you sure you want to delete '{file_path}'? This action cannot be undone.",
                    "needs_confirmation": True,
                    "operation": "delete_file",
                    "target": file_path
                }

            # Create backup info
            size = path.stat().st_size
            path.unlink()

            return {
                "success": True,
                "message": f"Deleted file '{file_path}' ({size} bytes)",
                "deleted_file": file_path
            }
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to delete file '{file_path}'",
                "error": str(e)
            }

    def delete_folder(self, folder_path: str, confirmed: bool = False) -> Dict[str, Any]:
        """Delete a folder and its contents (requires confirmation)"""
        try:
            path = Path(folder_path)

            if not path.exists():
                return {
                    "success": False,
                    "message": f"Folder '{folder_path}' does not exist"
                }

            if not path.is_dir():
                return {
                    "success": False,
                    "message": f"'{folder_path}' is not a folder"
                }

            if not self._is_safe_path(folder_path):
                return {
                    "success": False,
                    "message": "Cannot delete system folders",
                    "error": "Unsafe path"
                }

            # Count items
            total_items = sum(1 for _ in path.rglob('*'))

            if self.confirmation_required and not confirmed:
                return {
                    "success": False,
                    "message": f"Are you sure you want to delete folder '{folder_path}' and all {total_items} items inside? This action cannot be undone.",
                    "needs_confirmation": True,
                    "operation": "delete_folder",
                    "target": folder_path,
                    "item_count": total_items
                }

            shutil.rmtree(path)

            return {
                "success": True,
                "message": f"Deleted folder '{folder_path}' and {total_items} items",
                "deleted_folder": folder_path
            }
        except Exception as e:
            logger.error(f"Failed to delete folder {folder_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to delete folder '{folder_path}'",
                "error": str(e)
            }

    def read_file(self, file_path: str) -> Dict[str, Any]:
        """Read text content from a file"""
        try:
            path = Path(file_path)

            if not path.exists():
                return {
                    "success": False,
                    "message": f"File '{file_path}' does not exist"
                }

            if not path.is_file():
                return {
                    "success": False,
                    "message": f"'{file_path}' is not a file"
                }

            if not self._is_safe_path(file_path):
                return {
                    "success": False,
                    "message": "Cannot read system files",
                    "error": "Unsafe path"
                }

            # Check file size (limit to 1MB for safety)
            size = path.stat().st_size
            if size > 1024 * 1024:
                return {
                    "success": False,
                    "message": f"File too large to read ({size} bytes). Maximum 1MB.",
                    "error": "File too large"
                }

            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "success": True,
                "message": f"Read {len(content)} characters from '{file_path}'",
                "content": content,
                "file_path": file_path,
                "size": size
            }
        except UnicodeDecodeError:
            return {
                "success": False,
                "message": f"File '{file_path}' is not a text file",
                "error": "Binary file"
            }
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to read file '{file_path}'",
                "error": str(e)
            }

    def write_file(self, file_path: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        """Write text content to a file"""
        try:
            path = Path(file_path)

            if not self._is_safe_path(file_path):
                return {
                    "success": False,
                    "message": "Cannot write to system directories",
                    "error": "Unsafe path"
                }

            # Check if file exists and needs confirmation
            if path.exists() and not overwrite and self.confirmation_required:
                return {
                    "success": False,
                    "message": f"File '{file_path}' already exists. Overwrite?",
                    "needs_confirmation": True,
                    "operation": "write_file_overwrite",
                    "target": file_path,
                    "content_preview": content[:100] + "..." if len(content) > 100 else content
                }

            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "success": True,
                "message": f"Wrote {len(content)} characters to '{file_path}'",
                "file_path": file_path
            }
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to write file '{file_path}'",
                "error": str(e)
            }

    def list_directory(self, dir_path: str = ".") -> Dict[str, Any]:
        """List contents of a directory"""
        try:
            path = Path(dir_path)

            if not path.exists():
                return {
                    "success": False,
                    "message": f"Directory '{dir_path}' does not exist"
                }

            if not path.is_dir():
                return {
                    "success": False,
                    "message": f"'{dir_path}' is not a directory"
                }

            if not self._is_safe_path(dir_path):
                return {
                    "success": False,
                    "message": "Cannot list system directories",
                    "error": "Unsafe path"
                }

            items = []
            for item in path.iterdir():
                try:
                    stat = item.stat()
                    items.append({
                        "name": item.name,
                        "type": "folder" if item.is_dir() else "file",
                        "size": stat.st_size if item.is_file() else None,
                        "modified": stat.st_mtime
                    })
                except:
                    # Skip items we can't access
                    continue

            return {
                "success": True,
                "message": f"Listed {len(items)} items in '{dir_path}'",
                "directory": str(path.resolve()),
                "items": items
            }
        except Exception as e:
            logger.error(f"Failed to list directory {dir_path}: {e}")
            return {
                "success": False,
                "message": f"Failed to list directory '{dir_path}'",
                "error": str(e)
            }

    def move_file(self, source: str, destination: str, confirmed: bool = False) -> Dict[str, Any]:
        """Move a file or folder"""
        try:
            src_path = Path(source)
            dst_path = Path(destination)

            if not src_path.exists():
                return {
                    "success": False,
                    "message": f"Source '{source}' does not exist"
                }

            if not self._is_safe_path(source) or not self._is_safe_path(destination):
                return {
                    "success": False,
                    "message": "Cannot move system files",
                    "error": "Unsafe path"
                }

            # Check if destination exists
            if dst_path.exists() and self.confirmation_required and not confirmed:
                return {
                    "success": False,
                    "message": f"Destination '{destination}' already exists. Overwrite?",
                    "needs_confirmation": True,
                    "operation": "move_overwrite",
                    "source": source,
                    "destination": destination
                }

            shutil.move(str(src_path), str(dst_path))

            return {
                "success": True,
                "message": f"Moved '{source}' to '{destination}'",
                "source": source,
                "destination": destination
            }
        except Exception as e:
            logger.error(f"Failed to move {source} to {destination}: {e}")
            return {
                "success": False,
                "message": f"Failed to move '{source}' to '{destination}'",
                "error": str(e)
            }

    def copy_file(self, source: str, destination: str, confirmed: bool = False) -> Dict[str, Any]:
        """Copy a file or folder"""
        try:
            src_path = Path(source)
            dst_path = Path(destination)

            if not src_path.exists():
                return {
                    "success": False,
                    "message": f"Source '{source}' does not exist"
                }

            if not self._is_safe_path(source) or not self._is_safe_path(destination):
                return {
                    "success": False,
                    "message": "Cannot copy system files",
                    "error": "Unsafe path"
                }

            # Check if destination exists
            if dst_path.exists() and self.confirmation_required and not confirmed:
                return {
                    "success": False,
                    "message": f"Destination '{destination}' already exists. Overwrite?",
                    "needs_confirmation": True,
                    "operation": "copy_overwrite",
                    "source": source,
                    "destination": destination
                }

            if src_path.is_file():
                shutil.copy2(str(src_path), str(dst_path))
            else:
                shutil.copytree(str(src_path), str(dst_path), dirs_exist_ok=True)

            return {
                "success": True,
                "message": f"Copied '{source}' to '{destination}'",
                "source": source,
                "destination": destination
            }
        except Exception as e:
            logger.error(f"Failed to copy {source} to {destination}: {e}")
            return {
                "success": False,
                "message": f"Failed to copy '{source}' to '{destination}'",
                "error": str(e)
            }