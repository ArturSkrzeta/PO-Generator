from datetime import date
from flask import Flask, render_template, make_response
import pdfkit
import json

app = Flask(__name__)
config = pdfkit.configuration(wkhtmltopdf=r'.\wkhtmltopdf\bin\wkhtmltopdf.exe')

def refresh_data():

    with open('data.json') as json_f:
        purchase_order = json.load(json_f)

    products = purchase_order['purchase-order']['products']
    vendor = purchase_order['purchase-order']['vendor']
    company = purchase_order['purchase-order']['company']
    po_number = purchase_order['purchase-order']['po_number']
    currency = purchase_order['purchase-order']['currency']

    total = 0
    for product in products:
        total += product['Price Each']*product['Quantity']

    return products, vendor, company, po_number, currency, total

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/pdf')
def pdf_template():

    products, vendor, company, po_number, currency, total = refresh_data()

    css = ['static/main.css']
    rnd = render_template('pdf_template.html', today=date.today(),
                                                products=products,
                                                vendor=vendor,
                                                company=company,
                                                po_number=po_number,
                                                currency=currency,
                                                total=total)


    pdf = pdfkit.from_string(rnd, False, css=css, configuration=config)

    rspns = make_response(pdf)
    rspns.headers['Content-Type'] = 'application/pdf'
    #uncomment when you want to download the file
    #rspns.headers['Content-Disposition'] = 'attachment; filename=PurchaseOrder.pdf'

    return rspns

if __name__ == "__main__":
    app.run(debug=True)
