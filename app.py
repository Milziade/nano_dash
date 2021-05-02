from flask import Flask, redirect, url_for, request, render_template
from form import LinkAddressForm
from address_func import *
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=os.environ.get('DEBUG'))
