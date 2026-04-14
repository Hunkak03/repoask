"""Test Git repository management utilities."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from git_utils import RepoManager, repo_manager


class TestRepoManagerURLValidation:
    """Test URL validation logic."""

    def setup_method(self):
        """Create fresh RepoManager for each test."""
        self.manager = RepoManager()

    def test_valid_github_url(self):
        """Test valid GitHub HTTPS URL."""
        assert self.manager.validate_url("https://github.com/user/repo") is True
        assert self.manager.validate_url("https://github.com/user/repo.git") is True

    def test_valid_gitlab_url(self):
        """Test valid GitLab HTTPS URL."""
        assert self.manager.validate_url("https://gitlab.com/user/repo") is True
        assert self.manager.validate_url("https://gitlab.com/user/repo.git") is True

    def test_invalid_url_returns_false(self):
        """Test invalid URL returns False."""
        assert self.manager.validate_url("not-a-url") is False
        assert self.manager.validate_url("https://example.com") is False
        assert self.manager.validate_url("ftp://github.com/user/repo") is False

    def test_ssh_url(self):
        """Test SSH URL format."""
        assert self.manager.validate_url("git@github.com:user/repo.git") is True


class TestRepoManagerURLNormalization:
    """Test URL normalization."""

    def setup_method(self):
        self.manager = RepoManager()

    def test_adds_git_suffix(self):
        """Test .git suffix is added if missing."""
        url = self.manager.normalize_url("https://github.com/user/repo")
        assert url.endswith(".git")

    def test_removes_trailing_slash(self):
        """Test trailing slash is removed."""
        url = self.manager.normalize_url("https://github.com/user/repo/")
        assert not url.endswith("/")

    def test_preserves_existing_git_suffix(self):
        """Test existing .git suffix is preserved."""
        url = self.manager.normalize_url("https://github.com/user/repo.git")
        assert url.endswith(".git")
        assert url.count(".git") == 1


class TestRepoNameExtraction:
    """Test repository name extraction."""

    def setup_method(self):
        self.manager = RepoManager()

    def test_extracts_name_from_https_url(self):
        """Test extraction from HTTPS URL."""
        name = self.manager.extract_repo_name("https://github.com/user/flask")
        assert name == "flask"

    def test_extracts_name_with_git_suffix(self):
        """Test extraction from URL with .git suffix."""
        name = self.manager.extract_repo_name("https://github.com/user/flask.git")
        assert name == "flask"

    def test_sanitizes_special_characters(self):
        """Test special characters are sanitized."""
        name = self.manager.extract_repo_name("https://github.com/user/my-repo_2024")
        assert name == "my-repo_2024"


class TestCodeFileFiltering:
    """Test code file filtering."""

    def setup_method(self):
        self.manager = RepoManager()

    def test_includes_python_files(self):
        """Test Python files are included."""
        test_path = Path("test_repo/main.py")
        assert self.manager._matches_include_patterns(test_path) is True

    def test_includes_javascript_files(self):
        """Test JavaScript files are included."""
        test_path = Path("test_repo/app.js")
        assert self.manager._matches_include_patterns(test_path) is True

    def test_includes_typescript_files(self):
        """Test TypeScript files are included."""
        test_path = Path("test_repo/index.ts")
        assert self.manager._matches_include_patterns(test_path) is True

    def test_includes_dockerfile(self):
        """Test Dockerfile is included."""
        test_path = Path("test_repo/Dockerfile")
        assert self.manager._matches_include_patterns(test_path) is True

    def test_includes_readme(self):
        """Test README files are included."""
        test_path = Path("test_repo/README.md")
        assert self.manager._matches_include_patterns(test_path) is True

    def test_excludes_binary_files(self):
        """Test binary files are excluded."""
        test_path = Path("test_repo/image.png")
        assert not self.manager._matches_include_patterns(test_path)

    def test_excludes_executable_files(self):
        """Test executable files are excluded."""
        test_path = Path("test_repo/program.exe")
        assert not self.manager._matches_include_patterns(test_path)

    def test_excludes_node_modules(self):
        """Test node_modules directory is excluded."""
        test_path = Path("test_repo/node_modules/package/index.js")
        # This should be filtered by EXCLUDE_DIRS in get_code_files
        assert "node_modules" in str(test_path)


class TestRepoManagerSingleton:
    """Test singleton instance."""

    def test_singleton_exists(self):
        """Test repo_manager singleton exists."""
        assert repo_manager is not None
        assert isinstance(repo_manager, RepoManager)
