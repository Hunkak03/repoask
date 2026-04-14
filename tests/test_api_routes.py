"""Test API routes."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from fastapi.testclient import TestClient


class TestRepositoryEndpoints:
    """Test repository management routes."""

    @patch('main.repo_manager')
    @patch('main.rag_engine')
    def test_add_repository_success(self, mock_engine, mock_manager):
        """Test adding a repository successfully."""
        mock_manager.clone_repository.return_value = {
            'name': 'test-repo',
            'url': 'https://github.com/user/test-repo.git',
            'path': '/tmp/test-repo',
            'branch': 'main',
            'commit': 'abc12345'
        }
        mock_manager.get_code_files.return_value = ['main.py', 'config.py']
        mock_engine.load_repository.return_value = None

        from main import app
        client = TestClient(app)

        response = client.post(
            "/api/repository",
            json={"url": "https://github.com/user/test-repo"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'
        assert 'files_indexed' in data['repository']

    @patch('main.repo_manager')
    def test_add_repository_invalid_url(self, mock_manager):
        """Test adding repository with invalid URL."""
        mock_manager.clone_repository.side_effect = ValueError("Invalid URL")

        from main import app
        client = TestClient(app)

        response = client.post(
            "/api/repository",
            json={"url": "not-a-valid-url"}
        )

        assert response.status_code == 400

    @patch('main.repo_manager')
    def test_list_repositories_success(self, mock_manager):
        """Test listing repositories."""
        mock_manager.list_repositories.return_value = [
            {
                'name': 'repo1',
                'path': '/tmp/repo1',
                'url': 'https://github.com/user/repo1.git',
                'branch': 'main'
            }
        ]

        from main import app
        with patch('main.rag_engine'):
            client = TestClient(app)
            response = client.get("/api/repositories")

            assert response.status_code == 200
            data = response.json()
            assert 'repositories' in data

    @patch('main.repo_manager')
    def test_delete_repository_success(self, mock_manager):
        """Test deleting a repository."""
        mock_manager.delete_repository.return_value = True

        from main import app
        with patch('main.rag_engine'):
            client = TestClient(app)
            response = client.delete("/api/repository/test-repo")

            assert response.status_code == 200

    @patch('main.repo_manager')
    def test_delete_repository_not_found(self, mock_manager):
        """Test deleting non-existent repository."""
        mock_manager.delete_repository.return_value = False

        from main import app
        with patch('main.rag_engine'):
            client = TestClient(app)
            response = client.delete("/api/repository/nonexistent")

            assert response.status_code == 404


class TestRebuildIndex:
    """Test index rebuild endpoint."""

    @patch('main.rag_engine')
    def test_rebuild_index_success(self, mock_engine):
        """Test rebuilding index."""
        mock_engine.rebuild_index.return_value = None

        from main import app
        client = TestClient(app)

        response = client.post("/api/rebuild-index")

        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'success'


class TestFrontend:
    """Test frontend serving."""

    def test_root_serves_html(self):
        """Test root path serves frontend HTML."""
        from main import app
        client = TestClient(app)

        response = client.get("/")

        assert response.status_code in [200, 404]  # 404 if frontend dir missing
