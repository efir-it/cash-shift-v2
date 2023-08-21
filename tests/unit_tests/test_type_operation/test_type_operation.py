from type_operation.dao import TypeOperationDAO

def weer():
    assert 1 == 1

async def test_add_type_operation():
    new_type_operation = await TypeOperationDAO.add(
        name='Наличные'
    )
    assert new_type_operation == 'Наличные'
    assert new_type_operation != 'Безнал'
    assert new_type_operation is not None

