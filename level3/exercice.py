import json

def load_data(filepath):
    with open(filepath) as data_file:
        res = json.load(data_file)
    return res

def get_discount(discounts, article_id):
    for discount in discounts:
        if discount['article_id'] == article_id:
            return discount
    return None

def get_article_price(articles, discounts, article_id):
    discount_operation = {
        'amount': lambda x, y: x - y,
        'percentage': lambda x, y: x * (100 - y) / 100
    }
    for article in articles:
        if article['id'] == article_id:
            d = get_discount(discounts, article_id)

            try:
                price = discount_operation[d['type']](article['price'], d['value'])
            except Exception:
                price = article['price']

            return price
    return 0

def is_in_price_range(fee, price):
    p_range = fee['eligible_transaction_volume']
    if price >= (p_range['min_price'] or 0) and price < (p_range['max_price'] or 0):
        return True
    return False

def compute_fees(fees, price):
    for fee in fees:
        if is_in_price_range(fee, price):
            return fee['price']
    return 0


def cart_price(articles, fees, discounts, cart):
    price = 0
    for item in cart['items']:
        article_price = get_article_price(articles, discounts, item['article_id'])
        price += article_price * item['quantity']
    price += compute_fees(fees, price)
    return {'id': cart['id'], 'total': price}

def compute_output(articles, fees, discounts, carts):
    res = [cart_price(articles, fees, discounts, cart) for cart in carts]
    return {'carts': res}


def test_solution(filepath, test_output):
    with open(filepath) as data_file:
        expected_output = json.load(data_file)
    return expected_output == test_output



if __name__ == "__main__":
    data = load_data('data.json')
    articles, carts = data['articles'], data['carts']
    fees, discounts = data['delivery_fees'], data['discounts']
    res = compute_output(articles, fees, discounts, carts)
    print test_solution('output.json', res)
