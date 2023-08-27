from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill.flat import Flatmate, Bill


app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template("index.html")


class BillFormPage(MethodView):
    def get(self):
        bill_form = BillForm()
        result = False
        return render_template("bill_form_page.html",
                               billform=bill_form, result=result)

    def post(self):
        billform = BillForm(request.form)
        total_billl = Bill(amount=float(billform.amount.data), period=billform.period.data)
        name1 = billform.name1.data
        days_in_house1 = int(billform.days_in_house1.data)
        name2 = billform.name2.data
        days_in_house2 = int(billform.days_in_house2.data)

        mate1 = Flatmate(name1, days_in_house1)
        mate2 = Flatmate(name2, days_in_house2)
        amount1 = round(mate1.pays(total_billl, mate2), 2)
        amount2 = round(mate2.pays(total_billl, mate1), 2)

        return render_template("bill_form_page.html", billform=billform,
                               result=True,
                               name1=name1, name2=name2,
                               amount1=amount1, amount2=amount2)


class ResultsPage(MethodView):

    def post(self):
        billform = BillForm(request.form)

        total_billl = Bill(amount=float(billform.amount.data), period=billform.period.data)
        name1 = billform.name1.data
        days_in_house1 = int(billform.days_in_house1.data)
        name2 = billform.name2.data
        days_in_house2 = int(billform.days_in_house2.data)

        mate1 = Flatmate(name1, days_in_house1)
        mate2 = Flatmate(name2, days_in_house2)
        amount1 = round(mate1.pays(total_billl, mate2), 2)
        amount2 = round(mate2.pays(total_billl, mate1), 2)

        return render_template("results.html", name1=name1, name2=name2,
                               amount1=amount1, amount2=amount2)


class BillForm(Form):
    amount = StringField("Bill Amount: ", default='250.000')
    period = StringField("Bill Period: ", default='May 2021')

    name1 = StringField("Name: ", default='John')
    days_in_house1 = StringField("Days in the House: ", default='25')
    name2 = StringField("Name: ", default='Jane')
    days_in_house2 = StringField("Days in the House: ", default='23')

    button = SubmitField('Calculate')


if __name__ == "__main__":

    app.add_url_rule('/',
                     view_func=HomePage.as_view('home_page'))
    app.add_url_rule('/bill_form',
                     view_func=BillFormPage.as_view('bill_form_page'))
    # app.add_url_rule('/results',
    #                  view_func=ResultsPage.as_view('results_page'))

    app.run(debug=True)
