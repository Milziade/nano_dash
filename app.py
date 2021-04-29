from flask import Flask, redirect, url_for, request, render_template
from form import LinkAddressForm
from address_func import *

app = Flask(__name__)
app.config['SECRET_KEY'] = '4e28a0ce03d1af568ddb0ea71be52fae30a5bab695dea817421e2a4fdb760014'


@app.route("/", methods=["GET", "POST"])
def home():
    form = LinkAddressForm()
    if form.is_submitted():
        result = request.form
        address = result['address']
        return redirect(url_for('results', address=address))
    return render_template('home.html', form=form)


@app.route("/results/<address>")
def results(address):
    history = get_json(address)
    if not history:
        return render_template('error.html')
    df, columns = get_df(history)
    accounts_rec, amount_rec, accounts_send, amount_send = pie_chart(df)
    balance = get_balance(address)
    overall_bal, time, insta_bal = balance_over_time(df)
    colors = get_colors(len(accounts_rec))
    return render_template('results.html', address=address, history=history,
                           df=df, colnames=columns, accounts_rec=accounts_rec, amount_rec=amount_rec,
                           accounts_send=accounts_send, amount_send=amount_send, balance=balance,
                           overall_bal=overall_bal, time=time, insta_bal=insta_bal, colors=colors)


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/bar')
def bar():
    bar_labels=labels
    bar_values=values
    return render_template('bar_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values)


@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)


@app.route('/pie')
def pie():
    pie_labels = labels
    pie_values = values
    return render_template('pie_chart.html', title='Bitcoin Monthly Price in USD', max=17000, set=zip(values, labels, colors))


@app.route('/r/<address>')
def r(address):
    history = get_json(address)
    df, columns = get_df(history)
    accounts, amount = pie_chart(df)
    return render_template('risultati.html', accounts=accounts, amount=amount)


if __name__ == "__main__":
    app.run(debug=True)
