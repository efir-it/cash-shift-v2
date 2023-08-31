from event.base_producer import Producer


class SaleCheckProducer(Producer):
    module = "checkoutShift"
    event = "salesCashReceipt"
    event_consumers = ["prodMove"]


class ReturnCheckProducer(Producer):
    module = "checkoutShift"
    event = "returnCashReceipt"
    event_consumers = ["prodMove"]
