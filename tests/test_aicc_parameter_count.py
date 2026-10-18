import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from cunw_calibration.models import aicc

def test_aicc_includes_estimated_variance():
    y = np.arange(9, dtype=float)
    predicted = y + 1
    total_parameters = 4  # Three mean coefficients plus residual variance
    expected = 2 * total_parameters + 2 * total_parameters * (total_parameters + 1) / (9 - total_parameters - 1)
    assert np.isclose(aicc(y, predicted, 3), expected)

def test_aicc_undefined_small_sample():
    assert np.isinf(aicc(np.arange(5.), np.arange(5.) + 1, 3))
