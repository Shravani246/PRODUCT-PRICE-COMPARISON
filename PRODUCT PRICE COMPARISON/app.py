from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
def find_product_with_least_price(product_info_list):
    if len(product_info_list) == 0:
        return None

    min_price_product = min(product_info_list, key=lambda x: float(x['price']))
    return min_price_product
def scrape(url, keyword):
    try:
        res = requests.get(url + keyword).content
        soup = BeautifulSoup(res, 'html.parser')
        if url == 'https://www.flipkart.com/search?q=':
            items = soup.find_all('a', class_='_1fQZEK')
            costs = soup.find_all('div', class_='_30jeq3 _1_WHN1')
            images = soup.find_all('img', class_='_396cs4')
        elif url == 'https://www.amazon.in/s?k=':
            items = soup.find_all('span', class_='a-size-medium a-color-base a-text-normal')
            costs = soup.find_all('span', class_='a-offscreen')
            images = soup.find_all('img', class_='s-image')
        elif url == 'https://www.reliancedigital.in/search?q=':
            items = soup.find_all('p', class_='sp__name')
            costs = soup.find_all('span', class_='sc-bxivhb cHwYJ')
            images = soup.find_all('img', class_='product__img')
        elif url == 'https://www.happimobiles.com/mobiles/all?serach=&q=':
            items = soup.find_all('a', class_='name')
            costs = soup.find_all('div', class_='p-c')
            images = soup.find_all('img', class_='product-list-image')
        elif url == 'https://www.lotmobiles.com/catalogsearch/result/?q=':
            items = soup.find_all('a', class_='product-item-link')
            costs = soup.find_all('span', class_='price')
            images = soup.find_all('img', class_='product-image-photo')
        elif url == 'https://www.paiinternational.in/SearchResults.aspx?search=':
            items = soup.find_all('a', class_='prodHeaderDesc mb10')
            costs = soup.find_all('h3', class_='prodPrice d-inline')
            images = soup.find_all('img', class_='card-img-top')
        elif url == 'https://www.bajajelectronics.com/product/search?q=':
            items = soup.find_all('h3', class_='prodHeaderDesc mb10')
            costs = soup.find_all('h3', class_='prodPrice d-inline')
            images = soup.find_all('img', class_='card-img-top')
        else:
            items = []
            costs = []
            images = []

        product_info = []
        for item, cost, image in zip(items, costs, images):
            item_text = item.text.strip()
            cost_text = cost.text.strip()[1:]
            image_url = image['src']
            product_info.append({
                'name': item_text,
                'price': cost_text,
                'image': image_url
            })
        min_price_product = find_product_with_least_price(product_info)
        if min_price_product:
            return [min_price_product]
        return product_info
    except Exception as e:
        print(f"Error scraping data from {url}: {e}")
        return []



@app.route('/')
def index():
    return render_template('index.html')
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form['keyword']
    product_info = {}

    sites = {
        'Flipkart': 'https://www.flipkart.com/search?q=',
        'Amazon': 'https://www.amazon.in/s?k=',
        'Reliance': 'https://www.reliancedigital.in/search?q=',
        'Happi Mobiles': 'https://www.happimobiles.com/mobiles/all?serach=&q=',
        'Lot Mobiles': 'https://www.lotmobiles.com/catalogsearch/result/?q=',
        'Pai International': 'https://www.paiinternational.in/SearchResults.aspx?search=',
        'Bajaj Electronics': 'https://www.bajajelectronics.com/product/search?q='
    }

    for site, url in sites.items():
        product_info[site] = scrape(url, keyword)

    return render_template('results.html', keyword=keyword, product_infos=product_info)


if __name__ == '__main__':
    app.run(debug=True)