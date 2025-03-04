import pytest
import requests
from unittest.mock import patch
from descarga import descargar_paginas

@patch("requests.get")
def test_descarga_exitosa(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html></html>"

    descargar_paginas()
    mock_get.assert_called()