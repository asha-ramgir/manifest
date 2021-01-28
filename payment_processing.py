from flask import Flask, request
from datetime import datetime
app = Flask(__name__)

@app.route('/api/v1/processpayment', methods=['GET'])
def ProcessPayment():
    query_parameters = request.args
    try:
        credit_card_number = query_parameters.get('CreditCardNumber')
        assert credit_card_number and isinstance(credit_card_number, str), 'Invalid Credit Card Number'
        card_holder = query_parameters.get('CardHolder')
        assert card_holder and isinstance(card_holder, str), 'Invalid Card Holder'
        expiration_date = query_parameters.get('ExpirationDate')
        assert expiration_date and expiration_date < datetime.today(), 'Invalid Expiration Date'
        security_code = query_parameters.get('SecurityCode', '')
        amount = query_parameters.get('Amount')
        assert amount and (isinstance(amount, float) and amount > 0), 'Invalid Amount'

        if amount <= 20:
            payment_provider = CheapPaymentGateway()
        elif amount > 21 and amount <= 500:
            payment_provider = ExpensivePaymentGateway()
        else: #amount > 500
            payment_provider = PremiumPaymentGateway()
        result = payment_provider.process_payment(CreditCardNumber=credit_card_number, CardHolder=card_holder,
                                                  ExpirationDate=expiration_date,
                                                  SecurityCode=security_code, Amount=amount)
        if result:
            return {'data': {'code': '200', 'value': 'Payment processed successfully.', 'header': 'Success'}}
        else:
            return {'data': {'code': '500', 'value': 'Payment processing failed.', 'header': 'Success'}}

    except Exception as e:
        msg_code = e.message
        error_codes = {
            'invalid_credit_card_number': 'Invalid Credit Card Number',
            'invalid_card_holder': 'Invalid Card Holder',
            'invalid_expiration_date': 'Invalid Expiration Date',
            'invalid_amount': 'Invalid Amount',
        }
        value = error_codes.get(msg_code)
        if not value:
            code = '500'
            print "Something went wrong while processing payment for request: %s with error: %s" % (
            query_parameters, str(e))
            header = 'Internal Server Error'
            value = 'Something went wrong at our end. Please try again in few minutes or contact our team.'
        else:
            header = 'Invalid Request'
            code = '400'
        return {'data': {'code': code, 'value': value, 'header': header}}

#external service classes
class CheapPaymentGateway():
    def process_payment(self, CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
        try:
            #code to submit request to process payment
            pass
        except Exception as e:
            return False
        return True


class ExpensivePaymentGateway():
    def process_payment(self, CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
        try:
            #If gateway is not available, raise an error so that cheap payment gateway will be invoked
            #code to submit request to process payment
            pass
        except Exception as e:
            try:
                payment_provider = CheapPaymentGateway()
                payment_provider.process_payment(CreditCardNumber=CreditCardNumber, CardHolder=CardHolder,
                                                 ExpirationDate=ExpirationDate,
                                                 SecurityCode=SecurityCode, Amount=Amount)
            except Exception as e:
                return False
        return True


class PremiumPaymentGateway():
    def process_payment(self, CreditCardNumber, CardHolder, ExpirationDate, SecurityCode, Amount):
        retry_count = 3
        for i in range(0, retry_count):
            try:
                #code to submit request to process payment
                pass
            except Exception as e:
                if i+1 == retry_count:
                    return False
                else:
                    continue
        return True

app.run()

if __name__ == '__main__':
    app.run(debug=True)