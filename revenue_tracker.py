import pandas as pd
from gdrive_app.utilities.authenticate import authenticate
from gdrive_app.utilities.file_management import get_file_by_name, download_bytesio
from gdrive_app.utilities.attendance_generator import convert_excel_bytes_to_dataframe
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import repeat

from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

pd.set_option('display.max_columns', 10)


app = Dash(__name__)

sheet_name = "Copy of Student List"
sheet = get_file_by_name(authenticate(), name=sheet_name)

df = convert_excel_bytes_to_dataframe(
        download_bytesio(
            get_file_by_name(
                authenticate(),
                sheet_name
            )[0],
            authenticate()
        )[0],
        "Installment Payers "
    )

df1 = convert_excel_bytes_to_dataframe(
        download_bytesio(
            get_file_by_name(
                authenticate(),
                sheet_name
            )[0],
            authenticate()
        )[0],
        "Overall"
    )

instal = df[['Student Name', 'Batch', 'Course', '# of Installments', 'Paid Installment', 'Installment price',
             'First payment date', 'Payment Status']]
instal[['Course Price', 'Fees Owed']] = df[['Course Price', 'Fees Owed']].astype(float)
instal = instal[instal.Batch.notnull()]
instal.dropna(subset=['# of Installments', 'First payment date'], inplace=True)
instal['# of Installments'] = instal['# of Installments'].astype(int)
instal = instal.reset_index()
instal = instal.drop('index', axis=1)


duration = list(instal['# of Installments'])
date = instal['First payment date']
time_range = []

#get current month

cmonth = datetime.now()
for i in range(6):
    cmonths = cmonth+relativedelta(months=i+1)
    time_range.append(cmonths.replace(day=1, hour=0,minute=0,second=0,microsecond=0))

student = instal['Student Name']
instal_amt = instal['Installment price']
stpaydate = []

#Get the expected payday of all students
for i in range(len(instal)):
    payday = []
    first = instal['First payment date'][i]
    pay_count = instal['# of Installments'][i]
    for j in range(pay_count):
        pay = first+relativedelta(months=j)
        payday.append(pay)
    stpaydate.append(payday)

instal['Payday'] = stpaydate


e_pmt = list(repeat(0, len(time_range)))

for i in range(len(time_range)):
    month=time_range[i]
    for j in range(len(stpaydate)):
        for k in stpaydate[j]:
            if k.year==month.year and k.month==month.month:
                e_pmt[i]=e_pmt[i]+instal_amt[j]


for i in range(len(time_range)):
    time_range[i]=time_range[i].strftime("%Y-%m")

exp = pd.DataFrame({
    "Month": time_range,
    "Expected Installment": e_pmt
})




#installment_graph = px.bar(instal, x="Month", y="Expected Installment", title='Installment Payments in Future')

rev = df1[['Course', 'Cohort Start Date', 'Revenue\n(Formulated)']]
rev = rev.dropna(subset=['Course'])
rev['Cohort Start Date'] = df1['Cohort Start Date'].astype(str)
rev = rev.reset_index()
rev = rev.drop('index', axis=1)


df1.dropna(subset='Cohort Start Date', inplace=True)
hc = df1[['Course', 'Cohort Start Date', 'Student Count']]
hc['Cohort Start Date'] = df1['Cohort Start Date'].astype(str)
drop_lst = ['All']
cohort_start = hc['Cohort Start Date'].unique()
for c in cohort_start:
    drop_lst.insert(1, c)

#Track all students who have not finished payments
track = instal[instal['Payment Status'].isin(['Still Paying', 'Overdue Payment'])]
track.dropna(subset='Fees Owed', inplace=True)
track['Received'] = list(map(lambda x, y: x-y, track['Course Price'], track['Fees Owed']))

track['Month Received'] = [0]*len(track)
track['Pay Date'] = ['na']*len(track)
exp_todate = []

tcond = lambda x: x.date() <= cmonth.date()
same_month = lambda x, y: x.month == y.month and x.year == y.year
for s in track['Student Name']:
    row = track.loc[track['Student Name'] == s]
    payd = row['Payday'].values[0]
    if row['Payment Status'].values[0] == 'Overdue Payment':
        ep = row['Course Price'].values[0]
        track.loc[track['Student Name'] == s, 'Pay Date'] = payd[-1]
    else:
        count = sum(1 for t in payd if tcond(t))
        ip = row['Installment price'].values[0]
        ep = ip*count
        for index, date in enumerate(payd):
            if same_month(date, cmonth):
                track.loc[track['Student Name'] == s, 'Pay Date'] = date
                if tcond(date):
                    if (index+1) == row['Paid Installment'].values[0]:
                        track.loc[track['Student Name'] == s, 'Month Received'] = ip

    exp_todate.append(ep)

track['Expected'] = exp_todate
track[['Month Received', 'Installment price']] = track[['Month Received', 'Installment price']].astype(float)

sub = track[track['Payment Status'].isin(['Still Paying'])]

#Plot tracking graphs
revenue_graph = px.bar(rev, x="Cohort Start Date", y="Revenue\n(Formulated)", hover_name="Course", barmode="stack",
                       title="Revenue by course")
revenue_graph.update_xaxes(type="category")

installment_graph = px.bar(exp, x="Month", y="Expected Installment", title='Installment Payments in Future')

#Tracking all payment to date by student
pmt_todate = px.bar(
    track, x="Student Name", y="Received",
    color='Payment Status',
    color_discrete_map={'Overdue Payment': 'red', 'Still Paying': '#3366CC'},
    title="Received Payment(to date)"
)
pmt_todate.add_trace(
    go.Scatter(x=track['Student Name'], y=track['Expected'], name="Expected",
               #color=track['Payment Status'],
               mode="lines+markers",
               )
)
pmt_todate.update_traces(xaxis='x2')

track_month = px.bar(
    sub, x="Pay Date", y=["Month Received", "Installment price"],
    color_discrete_sequence=px.colors.qualitative.Set2, hover_name='Student Name',
    barmode='group', title=f'Installment Tracker for {cmonth.year}-{cmonth.month}'
)
track_month.update_layout(
    yaxis_title="Amount ($)",
)

app.layout = html.Div(children=[
    html.H1(
        children='Sales Dashboard',
        style={
            'textAlign': 'center'
        }
    ),

    html.Div(children=[
        dcc.Graph(
            id='fig1_1', figure=pmt_todate, style={'width': '50%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id='fig1_2', figure=installment_graph, style={'width': '50%', 'display': 'inline-block'}
        ),
    ]),

    dcc.Graph(id='fig2_1', figure=track_month, style={'width': '33%', 'display': 'inline-block'}),


    html.Div(children=[
        dcc.Graph(
            id='fig3', figure=revenue_graph, style={'width': '50%', 'display': 'inline-block'}
        ),
        html.Div(children=[
            dcc.Dropdown(
                drop_lst,
                'All',
                id='xaxis-column',
                style={'width': '50%'}
            ),
            dcc.Graph(id='hc_graph')
        ], style={'width': '50%', 'display': 'inline-block'})])
])


@callback(
    Output('hc_graph', 'figure'),
    Input('xaxis-column', 'value'))
def update_hc(xaxis_column):
    if xaxis_column == 'All':
        hc_fig = px.bar(hc, x='Cohort Start Date', y="Student Count", color='Course', title="Overall Student Headcount")
        hc_fig.update_xaxes(type="category")
    else:
        subset = hc[hc['Cohort Start Date'] == xaxis_column]
        hc_fig = px.bar(subset, x='Course', y="Student Count", title=f"Headcount for Student Cohort {xaxis_column}")
    return hc_fig


if __name__ == '__main__':
    app.run(debug=True)
