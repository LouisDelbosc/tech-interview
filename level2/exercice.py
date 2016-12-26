import json

def load_data(filepath):
    with open(filepath) as data_file:
        res = json.load(data_file)
    return res

def find_article(articles, article_id):
    for article in articles:
        if article['id'] == article_id:
            return article
    return None

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


def cart_price(articles, fees, cart):
    price = 0
    for item in cart['items']:
        article = find_article(articles, item['article_id'])
        price += (article['price'] or 0) * item['quantity']
    price += compute_fees(fees, price)
    return {'id': cart['id'], 'total': price}

def compute_output(articles, fees, carts):
    res = [cart_price(articles, fees, cart) for cart in carts]
    return {'carts': res}

def test_solution(filepath, test_output):
    with open(filepath) as data_file:
        expected_output = json.load(data_file)
    return expected_output == test_output

if __name__ == "__main__":
    data = load_data('data.json')
    articles, carts, fees = data['articles'], data['carts'], data['delivery_fees']
    res = compute_output(articles, fees, carts)
    print test_solution('output.json', res)
