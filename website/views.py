from flask import Blueprint, render_template, request, redirect, url_for, session
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

views = Blueprint('views', __name__)

# Global variable to store dataset and results
df = None
frq_items = None
rules = None

@views.route('/', methods=['GET', 'POST'])
def home():
    global df, frq_items, rules

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file:
                # Save the file temporarily
                file_path = 'uploads/' + file.filename
                file.save(file_path)
                df = pd.read_excel(file_path)
                print(f"Dataset loaded with {len(df)} rows.")  # Debugging line

                # Store the dataset in session as JSON
                session['df'] = df.to_json()

                # Store the uploaded file name in the session
                session['uploaded_file_name'] = file.filename

                # Preprocess the dataframe
                df['Description'] = df['Description'].str.strip()
                df.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
                df['InvoiceNo'] = df['InvoiceNo'].astype('str')
                df = df[~df['InvoiceNo'].str.contains('C')]

                # Basket encoding
                basket_1 = (df
                            .groupby(['InvoiceNo', 'Description'])['Quantity']
                            .sum().unstack().reset_index().fillna(0)
                            .set_index('InvoiceNo'))

                def hot_encode(x):
                    if x <= 0:
                        return 0
                    if x >= 1:
                        return 1

                basket_encoded = basket_1.applymap(hot_encode)
                basket_encoded.drop('POSTAGE', axis=1, inplace=True)

                # Apply apriori with user-defined min_support
                min_support = float(request.form.get('min_support', 0))
                frq_items = apriori(basket_encoded, min_support=min_support, use_colnames=True)
                frq_items[''] = range(1, len(frq_items) + 1)
                frq_items = frq_items[[''] + [col for col in frq_items.columns if col != '']]

                # Apply association rules with user-defined min_threshold
                min_threshold = float(request.form.get('min_threshold', 0))
                rules = association_rules(frq_items, metric="confidence", min_threshold=min_threshold)
                rules = rules.drop(columns=['leverage', 'conviction'])
                rules[''] = range(1, len(rules) + 1)
                rules = rules[[''] + [col for col in rules.columns if col != '']]

                # Save the uploaded file name
                session['uploaded_file_name'] = file.filename 

    # Return the home page with the dataframe if loaded
    return render_template("home.html", 
                           df=df.head(100) if df is not None else None,
                           frq_items=frq_items if frq_items is not None else None,
                           rules=rules if rules is not None else None)

@views.route('/dataset', methods=['GET'])
def dataset():
    # Load the dataframe from the session if it exists
    if 'df' not in session:
        return redirect(url_for('views.home'))

    # Load the dataframe from the session (as JSON)
    df = pd.read_json(session['df'])

    uploaded_file_name = session.get('uploaded_file_name', 'No file uploaded')

    # Display the full dataset (instead of just the head)
    return render_template("dataset.html", df=df, file_name=uploaded_file_name)
