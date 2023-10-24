# <div id="main">EfiritPro Retail CashShiftModule CashShiftAPI</div>

## <div id="content">Содержание</div>

- [CashShiftAPI](#main)
    - [Содержание](#content)
    - [Использование](#usage)
        - [Получение списка кассовых смен](#usage-get-list)
        - [Получение информации о кассовой смене](#usage-get)
        - [Открытие кассовой смены](#usage-open)
        - [Закрытие кассовой смены](#usage-close)

## <div id="usage">Использование</div>

### <div id="usage-get-list">Получение списка кассовых смен</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/getCheckoutShifts

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/getCheckoutShifts (для работников)

#### Request

```
Query
{
    "ownerId": str             | обязательное
    "organizationId": str,      | обязательное
    "workerId": str,            | не обязательное
    "workplaceId": str,         | не обязательное
    "closed": bool,             | не обязательное
    "hidden": bool              | не обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "checkoutShifts": [
        {
            "id": string,
            "ownerId": string,
            "workerId": string,
            "organizationId": string,
            "storeId": string,
            "workplaceId": string,
            "cashRegisterId": string,
            "closed": bool,
            "hidden": bool,
            "openedTime": string,
        }, ...
    ],
}
```

### <div id="usage-get">Получение информации о кассовой смене</div>

#### API Endpoint
HttpGet [apiHost]/checkoutShift/getCheckoutShift

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- Совпадают workerId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/getCheckoutShift (для работников)

#### Request

```
Query
{
    "ownerId": string          | обязательное
    "organizationId": string    | обязательное
    "workerId": string          | обязательное
    "checkoutShiftId": string   | обязательное
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Кассовая смена не найдена)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "ownerId": string,
    "organizationId": string,
    "storeId": string,
    "workplaceId": string,
    "workerId": string,
    "cashRegisterId": string,
    "closed": bool,
    "hidden": bool,
    "openedTime": string,
    "cashReceipts": [
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
        }, ...
    ]
}
```

### <div id="usage-open">Открытие кассовой смены</div>

#### API Endpoint
HttpPost [apiHost]/checkoutShift/openCheckoutShift

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- Совпадают workerId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/openCheckoutShift (для работников)

#### Request

```
Query
{
    "ownerId": string          | обязательное
    "organizationId": string    | обязательное
    "workerId": string          | обязательное
}
Body
Content-Type: "application/json"
{
    "storeId": string,
    "workplaceId": string,
    "cashRegisterId": string,
}
```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 500 (Если кассовую смену не удалось открыть)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "ownerId": string,
    "workerId": string,
    "organizationId": string,
    "storeId": string,
    "workplaceId": string,
    "cashRegisterId": string,
    "closed": bool,
    "hidden": bool,
    "openedTime": string,
}
```

### <div id="usage-close">Закрытие кассовой смены</div>

#### API Endpoint
HttpPatch [apiHost]/checkoutShift/closeCheckoutShift

#### Ограничения

- В Headers есть поле Authorization с токеном "Bearer [token]"
- Совпадают ownerId в токене и запросе
- Совпадают organizationId в токене и запросе (для работников)
- В токене есть разрешение /checkoutShift/closeCheckoutShift (для работников)

#### Request

```
Query
{
    "ownerId": string,         | обязательное
    "organizationId": string,   | обязательное
    "workerId"" string,         | обязательное
    "checkoutShiftId": string   | обязательное
}

```

####  Response 401 (Пользователь без токена)
####  Response 403 (Пользователь не прошёл ограничения)
####  Response 404 (Если кассовая смена не найдена)
####  Response 200
```
Body
Content-Type: "application/json"
{
    "id": string,
    "ownerId": string,
    "organizationId": string,
    "storeId": string,
    "workplaceId": string,
    "workerId": string,
    "cashRegisterId": string,
    "closed": bool,
    "hidden": bool,
    "openedTime": string,
    "cashReceipts": [
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
        }, ...
    ]
}
```