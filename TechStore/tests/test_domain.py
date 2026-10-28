import pytest
from decimal import Decimal
from app.domain import Money, InvalidOrderData, InvalidOrderTransition, OrderItemLimitExceeded
from cargar_csv import load_fixture

def test_money_negativo():
    with pytest.raises(InvalidOrderData):
        Money(Decimal("-1"))

def test_pedido_o001_inicia_draft():
    orders = load_fixture()
    assert orders["O001"].status.value == "DRAFT"
    assert orders["O001"].units == 4
    assert orders["O001"].total.amount == Decimal("2100.00")

def test_confirmacion_doble_falla():
    orders = load_fixture()
    order = orders["O013"]
    order.confirm() # Primera vez funciona
    
    with pytest.raises(InvalidOrderTransition):
        order.confirm() # Segunda vez debe lanzar error

def test_limite_de_20_articulos():
    orders = load_fixture()
    order = orders["O008"] # Este pedido ya tiene 20 artículos
    from app.domain import OrderItem
    
    # Intentamos agregar un artículo extra
    item_extra = OrderItem(sku="SKU999", quantity=1, unit_price=Money(Decimal("100.00")))
    
    with pytest.raises(OrderItemLimitExceeded):
        order.add_item(item_extra)