# <div id="main">EfiritPro Retail CashShiftModule CashReceiptAPI</div>

## <div id="content">Содержание</div>

- [CashReceiptAPI](#main)
    - [Содержание](#content)
    - [Предустановленные типы](#types)
    - [Использование](#usage)
        - [Получение чека](#usage-get)
        - [Создание чека](#usage-create)
        - [Возврат чека](#usage-return)
        - [Закрытие чека](#usage-close)
        - [Удаление чека](#usage-remove)

## <div id="types">Предустановленные типы</div>

### status

enum принимающий следующие значения

- Test = 0

### taxSystem

enum принимающий следующие значения

- Test = 0

### typePayment

enum принимающий следующие значения

- Test = 0

### typeOperation

enum принимающий следующие значения

- Test = 0

## <div id="usage">Использование</div>


### <div id="usage-get">Получение чека</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/getCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/getCashReceipt (для работников)

#### Request

```
Query
{
    "ownerId": string          | обязательное
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
    "ownerId": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": number,
    "taxSystem": number,
    "typePayment": number,
    "reasonId": str | null,
    "status": number,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": number,
            "price": number,
            "positionNum": number
        }, ...
    ]
}
```

### <div id="usage-create">Создание чека</div>

#### API Endpoint
HttpPost [apiHost]/checkoutShift/createCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/createCashReceipt (для работников)

#### Request

```
Query
{
    "ownerId": string          | обязательное
    "organizationId": string    | обязательное
    "checkoutShiftId": string   | обязательное
}
Body
Content-Type: "application/json"
{
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": number 
    "taxSystem": number
    "typePayment": number   
    "reasonId": str | null      | (обязательное для typeOperation - Возврат)
    "positions": [
        {
            "productId": string,
            "count": number,
            "price": number,
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
    "ownerId": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": number,
    "taxSystem": number,
    "typePayment": number,
    "status": number,
    "reasonId": str | null,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": number,
            "price": number,
            "positionNum": number
        }, ...
    ]
}
```

### <div id="usage-close">Закрытие чека</div>

#### API Endpoint
HttpPatch [apiHost]/checkoutShift/closeCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/closeCashReceipt (для работников)

#### Request

```
Query
{
    "ownerId": string,         | обязательное
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
    "ownerId": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": number,
    "taxSystem": number,
    "typePayment": number,
    "status": number,
    "reasonId": str | null,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": number,
            "price": number,
            "positionNum": number
        }, ...
    ]
}
```

### <div id="usage-remove">Удаление чека</div>

#### API Endpoint
HttpDelete [apiHost]/checkoutShift/removeCashReceipt

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/removeCashReceipt (для работников)

#### Request

```
Query
{
    "ownerId": string,         | обязательное
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
    "ownerId": string,
    "checkoutShiftId": string,
    "date": string,
    "sum": number,
    "cashRegisterCheckNumber": string,
    "fiscalDocumentNumber": string,
    "typeOperation": number,
    "taxSystem": number,
    "typePayment": number,
    "status": number,
    "reasonId": str | null,
    "positions": [
        {
            "id": string,
            "productId": string,
            "count": number,
            "price": number,
            "positionNum": number
        }, ...
    ]
}
```