"""Git repository cloning and management utilities."""

import logging
import re
from pathlib import Path
from typing import Optional
from git import Repo, InvalidGitRepositoryError, GitCommandError

from config import settings

logger = logging.getLogger(__name__)


# File patterns to include (code files)
INCLUDE_PATTERNS = [
    '*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.mjs',
    '*.java', '*.c', '*.cpp', '*.h', '*.hpp',
    '*.cs', '*.go', '*.rs', '*.rb', '*.php',
    '*.swift', '*.kt', '*.kts', '*.scala',
    '*.html', '*.css', '*.scss', '*.sass', '*.less',
    '*.vue', '*.svelte', '*.astro',
    '*.sh', '*.bash', '*.zsh', '*.fish',
    '*.yml', '*.yaml', '*.json', '*.toml', '*.ini', '*.cfg', '*.conf',
    '*.xml', '*.sql', '*.graphql', '*.md', '*.rst', '*.txt',
    '*.env.example', '*.gitignore', '*.dockerignore',
    'Dockerfile', 'Makefile', 'LICENSE', 'README*',
]

# Directories to exclude
EXCLUDE_DIRS = {
    'node_modules', 'vendor', 'dist', 'build', 'out',
    '.git', '.svn', '.hg',
    '__pycache__', '.pytest_cache', '.mypy_cache',
    '.next', '.nuxt', '.svelte-kit',
    'venv', 'env', '.venv', '.env',
    'target', 'obj', 'bin',
    '.idea', '.vscode',
    'coverage', '.nyc_output',
    '.cache', '.parcel-cache',
    'vendor', 'third_party',
}

# File extensions to exclude
EXCLUDE_EXTENSIONS = {
    '.exe', '.dll', '.so', '.dylib', '.a', '.lib',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
    '.mp3', '.mp4', '.avi', '.mov',
    '.zip', '.tar', '.gz', '.rar', '.7z',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.pyc', '.pyo', '.pyd',
    '.lock', '.sum',
}


class RepoManager:
    """Manage Git repository cloning and file extraction."""

    def __init__(self):
        self.repos_dir = settings.REPO_DIR
        self.repos_dir.mkdir(parents=True, exist_ok=True)

    def validate_url(self, url: str) -> bool:
        """Validate Git repository URL."""
        # Support HTTPS, Git, and SSH URLs
        patterns = [
            r'^https?://.*\.git$',
            r'^https?://github\.com/[\w-]+/[\w-]+/?$',
            r'^https?://gitlab\.com/[\w-]+/[\w-]+/?$',
            r'^git@github\.com:[\w-]+/[\w-]+\.git$',
            r'^git@gitlab\.com:[\w-]+/[\w-]+\.git$',
        ]
        return any(re.match(p, url, re.IGNORECASE) for p in patterns)

    def normalize_url(self, url: str) -> str:
        """Normalize repository URL to HTTPS format."""
        # Remove trailing slashes
        url = url.rstrip('/')
        
        # Convert github.com short URLs to full URLs
        if url.startswith('github.com/') and not url.startswith('http'):
            url = 'https://' + url
        
        # Add .git suffix if missing for HTTPS URLs
        if url.startswith('http') and not url.endswith('.git'):
            url += '.git'
        
        return url

    def extract_repo_name(self, url: str) -> str:
        """Extract repository name from URL."""
        # Remove .git suffix
        url = url.rstrip('/').rstrip('.git')
        
        # Get last path segment
        name = url.split('/')[-1]
        
        # Clean up name
        name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
        
        return name

    def clone_repository(self, url: str) -> dict:
        """Clone a Git repository and return info."""
        try:
            # Normalize URL
            url = self.normalize_url(url)
            
            # Validate URL
            if not self.validate_url(url):
                raise ValueError(f"Invalid repository URL: {url}")
            
            # Generate repo name and path
            repo_name = self.extract_repo_name(url)
            repo_path = self.repos_dir / repo_name
            
            # Remove existing clone if present
            if repo_path.exists():
                logger.info(f"Removing existing repository: {repo_name}")
                import shutil
                shutil.rmtree(repo_path)
            
            logger.info(f"Cloning repository: {url}")
            
            # Clone repository (shallow clone for speed)
            repo = Repo.clone_from(
                url=url,
                to_path=str(repo_path),
                depth=1,  # Shallow clone
                single_branch=True
            )
            
            # Get repository info
            repo_info = {
                'name': repo_name,
                'url': url,
                'path': str(repo_path),
                'branch': repo.active_branch.name if repo.head.is_detached is False else 'detached',
                'commit': repo.head.commit.hexsha[:8],
            }
            
            logger.info(f"Successfully cloned: {repo_name}")
            return repo_info
            
        except GitCommandError as e:
            logger.error(f"Git command failed: {e}", exc_info=True)
            raise ValueError(f"Failed to clone repository: {str(e.stderr)[:200]}")
        except Exception as e:
            logger.error(f"Clone failed: {e}", exc_info=True)
            raise

    def get_code_files(self, repo_path: str) -> list[Path]:
        """Get list of code files from repository."""
        path = Path(repo_path)
        if not path.exists():
            return []
        
        code_files = []
        
        for file_path in path.rglob('*'):
            # Skip directories
            if not file_path.is_file():
                continue
            
            # Skip excluded directories
            if any(part in EXCLUDE_DIRS for part in file_path.parts):
                continue
            
            # Skip excluded extensions
            if file_path.suffix.lower() in EXCLUDE_EXTENSIONS:
                continue
            
            # Check if file matches include patterns
            if self._matches_include_patterns(file_path):
                code_files.append(file_path)
        
        return code_files

    def _matches_include_patterns(self, file_path: Path) -> bool:
        """Check if file matches include patterns."""
        import fnmatch
        
        filename = file_path.name
        suffix = file_path.suffix.lower()
        
        # Check exact filename matches
        if filename in {'Dockerfile', 'Makefile', 'LICENSE', '.env.example', '.gitignore', '.dockerignore'}:
            return True
        
        # Check if filename starts with README
        if filename.upper().startswith('README'):
            return True
        
        # Check extension matches
        if suffix in EXCLUDE_EXTENSIONS:
            return False
        
        # Check against include patterns
        for pattern in INCLUDE_PATTERNS:
            if fnmatch.fnmatch(filename, pattern):
                return True
        
        return False

    def list_repositories(self) -> list[dict]:
        """List all cloned repositories."""
        repos = []
        if not self.repos_dir.exists():
            return repos
        
        for repo_path in self.repos_dir.iterdir():
            if repo_path.is_dir():
                try:
                    repo = Repo(str(repo_path))
                    repos.append({
                        'name': repo_path.name,
                        'path': str(repo_path),
                        'url': repo.remotes.origin.url if repo.remotes else 'unknown',
                        'branch': repo.active_branch.name if repo.head.is_detached is False else 'detached',
                    })
                except InvalidGitRepositoryError:
                    continue
        
        return repos

    def delete_repository(self, repo_name: str) -> bool:
        """Delete a cloned repository."""
        repo_path = self.repos_dir / repo_name
        if repo_path.exists():
            import shutil
            shutil.rmtree(repo_path)
            logger.info(f"Deleted repository: {repo_name}")
            return True
        return False


# Singleton instance
repo_manager = RepoManager()
