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

def cart_price(articles, cart):
    price = 0
    for item in cart['items']:
        article = find_article(articles, item['article_id'])
        price += (article['price'] or 0) * item['quantity']
    return {'id': cart['id'], 'total': price}

def compute_output(articles, carts):
    res = [cart_price(articles, cart) for cart in carts]
    return {'carts': res}

def test_solution(filepath, test_output):
    with open(filepath) as data_file:
        expected_output = json.load(data_file)
    return expected_output == test_output

if __name__ == "__main__":
    data = load_data('data.json')
    articles, carts = data['articles'], data['carts']
    res = compute_output(articles, carts)
    print test_solution('output.json', res)
