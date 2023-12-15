# from uuid import UUID


# def change_format(body: dict) -> dict:
#     result = {}
#     naming_map = {
#         "id": "id",
#         "name": "name",
#         "count": "count",
#         "price": "price",
#         "product_id": "productId",
#         "productId": "product_id",
#         "position": "positionNum",
#         "positionNum": "position",
#         "owner_id": "ownerId",
#         "ownerId": "owner_id",
#     }
#     for name in naming_map.keys():
#         if name in body:
#             if isinstance(body[name], UUID):
#                 result[naming_map[name]] = str(body[name])
#             else:
#                 result[naming_map[name]] = body[name]
#     return result
