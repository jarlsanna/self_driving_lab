import pytest
import experiment_series as es
from unittest.mock import Mock

@pytest.fixture
def metadata():
    return {}

@pytest.fixture
def series(mock_input):
    return es.ExperimentSeries(False, '0', False)

@pytest.fixture
def mock_input(monkeypatch):
    def mocked_input(prompt):
        return 'Mocked description'
    monkeypatch.setattr('builtins.input', mocked_input)

def test_prompt_series_description(mock_input):
    
    series = es.ExperimentSeries(False, '0', False)
    series.promt_series_description()

    assert series.series_description == 'Mocked description'

def test_create_series_metadata_returns_dict_with_correct_fields(series):
    series_metadata = series.create_series_metadata()
    expected_headers = ["Series ID","Series description", "Sample produced?", "Pre-sputter?"]

    assert isinstance(series_metadata, dict)
    for header in expected_headers:
        assert header in series_metadata.keys(), f"Header '{header}' is missing in the dictionary"

def test_update_run_metadata_appended_dict_correctly(series, metadata):
    series.update_run_metadata(metadata)
    assert "Recipe_name" in metadata.keys()

def test_update_step_metadata_appended_dict_correctly(metadata):
    es.update_step_metadata(metadata, 3, [0, 0, 0, 0, 0])
    assert "Power_Ax2_setpoint_[W]", "Step_number" in metadata.keys()
