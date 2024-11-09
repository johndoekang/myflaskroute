from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, RadioField
from wtforms.validators import DataRequired

class UserInputForm(FlaskForm):
    # String field for stock symbol input
    query = StringField("Enter Stock Symbol", validators=[DataRequired()])

    # Select field for choosing the type of financial information to display
    financial_data_choice = SelectField(
        "Select Financial Information to Display",
        choices=[
            ('revenue', 'Revenue'),
            ('netIncome', 'Net Income'),
            ('eps', 'Earnings Per Share (EPS)'),
            ('operatingIncome', 'Operating Income'),
            ('operatingExpenses', 'Operating Expenses'),
            ('grossProfit', 'Gross Profit'),
            ('incomeBeforeTax', 'Income Before Tax')
        ],
        default='revenue',
        validators=[DataRequired()]
    )

    # Radio field for choosing the exchange (default is NASDAQ)
    exchange = RadioField(
        "Exchange",
        choices=[("NASDAQ", "NASDAQ"), ("NYSE", "NYSE"), ("AMEX", "AMEX")],
        default="NASDAQ",
        validators=[DataRequired()]
    )

    # Boolean field for agreeing to terms and conditions
    agree_terms = BooleanField("I agree to the terms and conditions", validators=[DataRequired()])

    # Submit field to submit the form
    submit = SubmitField("Search")
