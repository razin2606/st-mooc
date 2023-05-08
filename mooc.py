import pandas as pd
import streamlit as st
import plotly.express as px


##Page Configuration
st.set_page_config(page_title="MOOC Analytics",
                   page_icon="🔢",
                   layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center'>MOOC Dashboard</h1>", unsafe_allow_html=True)
st.markdown("##")


##File Upload
uploaded_file = st.file_uploader(label= "Upload your csv file", type= ['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df["counter"] = 1
    except Exception as e:
        print(e)
        df = pd.read_excel(uploaded_file)
        df["counter"] = 1

## columns Rename
rename = {'User': 'name',
        'Date Time': 'date',
        '1. How would you classify yourself?': 'designation',
        '2. Do you have a startup experience?': 'startup_experience',
        '3. What level of expertise to you have regarding Artificial Intelligence? (one answer only)': 'ai_experience',
        '6. Are you interested to learn about other participants and their learnings or do you rather keep to yourself?': 'collaboration',
        'THANK YOU!Would you kindly answer a few extra questions and tell is about yourself?8. What is your current age in years?': 'age',
        '4. Rate the following topics regarding your prior knowledge about them:Artificial Intelligence and Technology': 'prior_ai',
        'Sustainability and Responsible AI': 'prior_sustainability',
        'Entrepreneurship, Startups and Innovation': 'prior_entrepreneurship',
        '5. Rate the following topics in the order of interest to you:Artificial Intelligence and Technology': 'interest_ai',
        'Sustainability and Responsible AI.1': 'interest_sustainability',
        'Entrepreneurship, Startups and Innovation.1': 'interest_entrepreneurship',
        '9. Which gender do you associate yourself with?': 'gender',
        '10. In which country do you currently live?': 'country',
        '11. In which city do you currently live?': 'city',
        '12. Are you curious about the idea to push forward your own project or even to found a startup/company yourself? (one answer only)': 'curiosity',
        '13. What else would you like to tell us?': 'message'
        }
df.rename(columns=rename,
          inplace=True)


st.dataframe(df)

#-----------sidebar--------
st.sidebar.header('Filters')

city = st.sidebar.multiselect(
    "Select the city",
    options=df["city"].unique(),
    default=df["city"].unique()
)

gender = st.sidebar.multiselect(
    "Select the gender",
    options=df["gender"].unique(),
    default=df["gender"].unique()
)

country = st.sidebar.multiselect(
    "Select the country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

designation = st.sidebar.multiselect(
    "Select the designation",
    options=df["designation"].unique(),
    default=df["designation"].unique()
)

df_selection = df.query(
    "city == @city & gender == @gender & country == @country & designation == @designation"
)

#st.dataframe(df_selection)


participants = len(df_selection.index)


st.markdown("<h3 style='text-align: center'>Total Participants</h3>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center'>{(participants)}</h4>", unsafe_allow_html=True)
st.markdown("##")



st.subheader(":bar_chart: Demographic Report")

## Gender statistics
gendercount = df_selection.groupby(by=["gender"]).sum()[["counter"]].sort_values(by="counter")
fig_gender = px.pie(gendercount, values='counter', names=gendercount.index, title = "Gender")
st.plotly_chart(fig_gender)

## Country statistics
countrycount = df_selection.groupby(by=["country"]).sum()[["counter"]].sort_values(by="counter")
fig_country = px.pie(countrycount, values='counter', names=countrycount.index, title = "Country")
st.plotly_chart(fig_country)
maxcountry = df_selection['country'].value_counts().idxmax()
st.markdown(maxcountry)

##City statistics
citycount = df_selection.groupby(by=["city"]).sum()[["counter"]].sort_values(by="counter")
fig_city = px.pie(citycount, values='counter', names=citycount.index, title = "City")
st.plotly_chart(fig_city)


## Designation statistics
designationcount = df_selection.groupby(by=["designation"]).sum()[["counter"]].sort_values(by="counter")
fig_designation = px.bar(
    designationcount,
    x= designationcount.index,
    y= "counter",
    orientation="v",
    title="<b>Designation</b>",
    color_discrete_sequence=["#C6458D"] * len(designationcount),
    template="plotly_white",
    text_auto=True    
)
fig_designation.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title='count'
)
st.plotly_chart(fig_designation)

## Startup experience Dataframe
st.markdown("Startup Experience")
startupcount = df_selection.groupby(by=["startup_experience"]).sum()[["counter"]].sort_values(by="counter", ascending=False)
st.dataframe(startupcount)





st.markdown("##")
st.subheader(":bar_chart: Participant Report")

## AI Interest barchart
aiinterest = df_selection.groupby(by=["interest_ai"]).sum()[["counter"]].sort_values(by="counter")

fig_intai = px.bar(
    aiinterest,
    x= aiinterest.index,
    y= "counter",
    orientation="v",
    title="<b>Interest in AI</b>",
    color_discrete_sequence=["#C6458D"] * len(aiinterest),
    template="plotly_white",
    text_auto=True    
)
fig_intai.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title='count'
)
st.plotly_chart(fig_intai)


## Sustainability Interest Barchart
sustinterest = df_selection.groupby(by=["interest_sustainability"]).sum()[["counter"]].sort_values(by="counter")


fig_intsust = px.bar(
    sustinterest,
    x= sustinterest.index,
    y= "counter",
    orientation="v",
    title="<b>Interest in Sustainability</b>",
    color_discrete_sequence=["#C6458D"] * len(sustinterest),
    template="plotly_white",
    text_auto=True    
)
fig_intsust.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title='count'
)
st.plotly_chart(fig_intsust)

## Entrepreneurship Interest Barchart
entinterest = df_selection.groupby(by=["interest_entrepreneurship"]).sum()[["counter"]].sort_values(by="counter")


fig_intent = px.bar(
    entinterest,
    x= entinterest.index,
    y= "counter",
    orientation="v",
    title="<b>Interest in Entrepreneurship</b>",
    color_discrete_sequence=["#C6458D"] * len(entinterest),
    template="plotly_white",
    text_auto=True    
)
fig_intent.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    yaxis_title='count'
)
st.plotly_chart(fig_intent)



## AI Prior knowledge Barchart
priorai = df_selection.groupby(by=["prior_ai"]).sum()[["counter"]].sort_values(by="counter")


fig_priorai = px.bar(
    priorai,
    x= "counter",
    y= priorai.index,
    orientation="h",
    title="<b>Prior Knowledge in AI</b>",
    color_discrete_sequence=["#C6458D"] * len(entinterest),
    template="plotly_white",
    text_auto=True    
)
fig_priorai.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title='count'
)
st.plotly_chart(fig_priorai)

## Sustainability Prior knowledge Barchart
priorsust = df_selection.groupby(by=["prior_sustainability"]).sum()[["counter"]].sort_values(by="counter")


fig_priorsust = px.bar(
    priorsust,
    x= "counter",
    y= priorsust.index,
    orientation="h",
    title="<b>Prior Knowledge in Sustainability</b>",
    color_discrete_sequence=["#C6458D"] * len(priorsust),
    template="plotly_white",
    text_auto=True    
)
fig_priorsust.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title='count'
)
st.plotly_chart(fig_priorsust)


## Entrepreneurship Prior knowledge Barchart
priorent = df_selection.groupby(by=["prior_entrepreneurship"]).sum()[["counter"]].sort_values(by="counter")


fig_priorent = px.bar(
    priorent,
    x= "counter",
    y= priorent.index,
    orientation="h",
    title="<b>Prior Knowledge in Entrepreneurship</b>",
    color_discrete_sequence=["#C6458D"] * len(priorent),
    template="plotly_white",
    text_auto=True    
)
fig_priorent.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title='count'
)
st.plotly_chart(fig_priorent)

## Curiosity Barchart
curiosity = df_selection.groupby(by=["curiosity"]).sum()[["counter"]].sort_values(by="counter")


fig_curiosity = px.bar(
    curiosity,
    x= "counter",
    y= curiosity.index,
    orientation="h",
    title="<b>Curiosity</b>",
    color_discrete_sequence=["#C6458D"] * len(curiosity),
    template="plotly_white",
    text_auto=True    
)
fig_curiosity.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False)),
    xaxis_title='count'
)
st.plotly_chart(fig_curiosity)

## Messages Dataframe
pmessage = df_selection[['name', 'message']].groupby(by=["message"]).sum()


st.markdown("Remarks from Participants")
st.dataframe(pmessage)


