# <div id="main">EfiritPro Retail CashShiftModule CashReceiptAPI</div>

## <div id="content">Содержание</div>

- [CashReceiptAPI](#main)
    - [Содержание](#content)
    - [Использование](#usage)
        - [Получение чека](#usage-get)
        - [Создание чека](#usage-create)
        - [Возврат чека](#usage-return)
        - [Закрытие чека](#usage-close)
        - [Удаление чека](#usage-remove)

## <div id="usage">Использование</div>


### <div id="usage-get">Получение чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/getCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают clientId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/getCashReceipt (для работников)

#### Request

```
Query
{
    "clientId": string          | обязательное
    "organizationId": string    | обязательное
    "cashReceiptId": string     | обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Чек не найден)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "client_id": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string,
    "taxSystem": string,
    "typePayment": string,
    "status": string,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": string,
            "price": string,
            "positionNum": string
        }, ...
    ]
}
```

### <div id="usage-create">Создание чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/createCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают clientId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/createCashReceipt (для работников)

#### Request

```
Query
{
    "clientId": string          | обязательное
    "organizationId": string    | обязательное
    "checkoutShiftId": string   | обязательное
}
Body
Content-Type: "application/json"
{
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string
    "taxSystem": string
    "typePayment": string
    "positions": [
        {
            "productId": string,
            "count": string,
            "price": string,
        }, ...
    ]
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 500 (Если чек не удалось создать)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "client_id": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string,
    "taxSystem": string,
    "typePayment": string,
    "status": string,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": string,
            "price": string,
            "positionNum": string
        }, ...
    ]
}
```

### <div id="usage-return">Возврат чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/returnCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают clientId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/returnCashReceipt (для работников)

#### Request

```
Query
{
    "clientId": string,         | обязательное
    "organizationId": string,   | обязательное
    "cashReceiptId": string     | обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Если чек не удалось найти)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "client_id": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string,
    "taxSystem": string,
    "typePayment": string,
    "status": string,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": string,
            "price": string,
            "positionNum": string
        }, ...
    ]
}
```
### <div id="usage-close">Закрытие чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/closeCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают clientId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/closeCashReceipt (для работников)

#### Request

```
Query
{
    "clientId": string,         | обязательное
    "organizationId": string,   | обязательное
    "cashReceiptId": string     | обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Если чек не удалось найти)
####  Response 200

```
Body
Content-Type: "application/json"
{
    "id": string,
    "client_id": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string,
    "taxSystem": string,
    "typePayment": string,
    "status": string,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": string,
            "price": string,
            "positionNum": string
        }, ...
    ]
}
```

### <div id="usage-remove">Удаление чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/removeCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают clientId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/removeCashReceipt (для работников)

#### Request

```
Query
{
    "clientId": string,         | обязательное
    "organizationId": string,   | обязательное
    "cashReceiptId": string     | обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Если чек не удалось удалить)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "client_id": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": string,
    "taxSystem": string,
    "typePayment": string,
    "status": string,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": string,
            "price": string,
            "positionNum": string
        }, ...
    ]
}
```