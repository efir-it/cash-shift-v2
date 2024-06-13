# <div id="main">EfiritPro Retail CashShiftModule - Модуль кассовых смен</div>

## <div id="content">Содержание</div>

- [CashShiftModule](#main)
    - [Содержание](#content)
    - [Предназначение](#target)
    - [Установка](#install)
    - [Использование](#usage)

## <div id="target">Предназначение</div>

Модуль ответственен за открытие, закрытие кассовых смен.

## <div id="install">Установка</div>

### Предварительные требования

- docker версии ^24.0.0

### Процесс установки

1. Создать образ модуля

```bash
docker build -t efirit-cashshift-module:0.1 .
```

2. Применить этот образ в проекте EfiritPro Retail Backend

## <div id="usage">Использование</div>

### Внешнее API

apiHost - http адрес API сервера

- [CashShift API](usageManuals/cashshift_api.md)
- [CashReceipt API](usageManuals/cashreceipt_api.md)

### RabbitMQ

#### Прослушиваемые очереди и их объекты (см. Miro)

- checkoutShift/eventAck => RabbitEvent
- checkoutShift/removeOrganization => OrganizationEvent
- checkoutShift/removeStore => StoreEvent

#### Отправляемые очереди и их объекты (см. Miro)

- prodMove/salesCashReceipt => cashReceiptEvent
- prodMove/returnCashReceipt => cashReceiptEvent

uvicorn main:app --reload
