from bot import Bot

email = ''
password = ''

product_codes = ['B01545GQ9O', 'B016DCAOZY', 'B07MJKHYDC', 'B016DCAOOA',
                 'B07571223K', 'B077ZC9D8R', 'B00EP56O0G', 'B07VBM91JB',
                 'B07YY9ZD7M', 'B07T3MNKKW', 'B008WX2OY2', 'B07T5V4TCV',
                 'B01613I79K', 'B07VYRQZ69', 'B0015R1BL4', 'B074V8TCMY',
                 'B07VYRQZ69', 'B00FX4EBS0', 'B07YY9T1FQ']

if __name__ == '__main__':
    for product_code in product_codes:
        Bot(product_code, email, password).start()
