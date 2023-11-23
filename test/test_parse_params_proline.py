import io
import json
from pathlib import Path

import pandas as pd
import pytest

import proteobench.io.params.proline as proline_params

TESTDATA_DIR = Path(__file__).parent / "params"

parameters = [
    (
        "PSM FILTER: PEP_SEQ_LENGTH; Description: peptide sequence length filter; Properties: [threshold_value=7]",
        7,
    ),
    (
        "PSM FILTER: PEP_SEQ_LENGTH; Description: peptide sequence length filter; Properties: [threshold_value=12]",
        12,
    ),
]


@pytest.mark.parametrize("string,expected_min_pep", parameters)
def test_find_pep_length(string, expected_min_pep):
    actual_min_pep = proline_params.find_min_pep_length(string)
    assert actual_min_pep == expected_min_pep


def test_extract_params():
    file = TESTDATA_DIR / "Proline_example_w_Mascot_wo_proteinSets.xlsx"
    expected = pd.read_csv(file.with_suffix(".csv"), index_col=0).squeeze("columns")
    actual = proline_params.extract_params(file)
    actual = pd.Series(actual.__dict__)
    actual = pd.read_csv(io.StringIO(actual.to_csv()), index_col=0).squeeze("columns")
    assert expected.equals(actual)