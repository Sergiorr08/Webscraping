import pytest
from procesar import procesar_html

HTML_PRUEBA = '''
<div class="listing_item">
    <span class="location">Chapinero</span>
    <span class="price">$500,000,000</span>
    <span class="rooms">2</span>
    <span class="bathrooms">2</span>
    <span class="size">60</span>
</div>
'''

def test_procesar_html():
    datos = procesar_html(HTML_PRUEBA)
    assert len(datos) == 1
    assert datos[0][1] == "Chapinero"
    assert datos[0][2] == "$500,000,000"