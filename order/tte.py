# import razorpay
# client = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))

# data = { "amount": 500, "currency": "INR", "receipt": "order_rcptid_11" }
# payment = client.order.create(data=data)


import razorpay

ord = 'order_MMr7e1h5HaZxRO'
print(ord)

def get_payment_method(pid):
  payment_id = pid
 

  payment = razorpay.Payment.fetch(payment_id)
  payment_method = payment.payment_method

  return payment_method

method = get_payment_method(ord)

print(method)
