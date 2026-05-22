from unittest.mock import MagicMock
from src.main import run_twerkflow

def test_run_twerkflow():
    mock_app = MagicMock()
    mock_factory = MagicMock()
    
    # Mock task service
    mock_task_service = MagicMock()
    mock_factory.get_task_service.return_value = mock_task_service
    
    # Run
    result = run_twerkflow("1", ["twerkflow"], mock_app, mock_factory)
    
    assert mock_app.invoke.called
    assert result is not None
