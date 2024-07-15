import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration
st.set_page_config(
    page_title="Analyse des Retards GetAround",
    layout="wide"
)

DATA_URL = 'https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx'

# Titre et description
st.title("Analyse des Retards GetAround")
url_image="data:image/png;base64,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"
st.image(url_image)

st.markdown("""
    Bienvenue sur ce tableau de bord ! 

     Lors de l'utilisation de Getaround, les conducteurs réservent des voitures pour une période de temps spécifique, d'une heure à quelques jours. Ils sont censés ramener la voiture à l'heure, mais il arrive parfois que les conducteurs soient en retard pour le retour.
    Les retours tardifs peuvent générer de la frustration pour le prochain conducteur si la voiture devait être louée à nouveau le même jour : le service client rapporte souvent des utilisateurs mécontents car ils ont dû attendre que la voiture revienne de la location précédente ou des utilisateurs qui ont même dû annuler leur location car la voiture n'a pas été rendue à temps.

     L'objectif de ce tableau de bord est de déterminer un délai minimum entre deux locations ou du moins donner quelques indications sur le compromis de ce délai minimum. Une voiture ne sera pas affichée dans les résultats de recherche si les heures de check-in ou de check-out demandées sont trop proches d'une location déjà réservée.
      Cela résout le problème des retours tardifs mais peut aussi potentiellement nuire aux revenus de Getaround/propriétaires : nous devons trouver le bon compromis.

   
""")


st.markdown("---")

# Chargement des données avec mise en cache
@st.cache_data
def charger_donnees():
    data = pd.read_excel(DATA_URL)
    return data

st.text('Chargement des données ...')


etat_chargement_donnees = st.text('Chargement des données ...')
data = charger_donnees()
etat_chargement_donnees.text("Chargement des données terminé !")
# Vue d'ensemble du dataset
st.header('Vue d\'ensemble du dataset')

# Afficher les données brutes si la case à cocher est cochée
if st.checkbox('Afficher le dataset '):
    st.header('dataset')
    st.write(data)


st.header('Les chiffres clés ')
st.caption('*Ensembles des locations chez GETAROUND*')

col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    st.metric("réservations", value=21309, delta='locations', delta_color='normal')
    st.metric("parc", value=8142, delta='voitures uniques', delta_color='normal')
    
with col2:
    st.metric("retards", value=7945, delta='soit 44%', delta_color='inverse')
    st.metric("annulations", value=3264, delta='soit 15%', delta_color='inverse')

with col3:
    st.metric("temps de retour", value=-46, delta='minutes', delta_color='inverse')
    st.metric("retard moyen", value=202, delta='minutes', delta_color='inverse')

with col4:
    st.metric("check-in mobile", value=17002, delta='soit 80%', delta_color='normal')
    st.metric("check-in connect", value=4307, delta='soit 20%', delta_color='normal')

fig1 = px.histogram(data_frame=data,
        x='delay_at_checkout_in_minutes',
        color='checkin_type',
        histnorm='percent',
        barmode='overlay')

st.header("À quelle fréquence les conducteurs sont-ils en retard pour le check-out ?")
delay = (data["delay_at_checkout_in_minutes"] >= 0).value_counts(normalize=True)
fig10 = go.Figure(data=[go.Pie(labels=delay.rename(index={True: 'En retard', False: 'En avance ou à l\'heure'}).index, values=delay.values, textinfo='percent', hole=.5)])
fig10.update_traces(marker=dict(colors=['#FF5733', '#33FF57']))
st.plotly_chart(fig10)

fig2 = px.histogram(data_frame=data,
        x='time_delta_with_previous_rental_in_minutes',
        color='checkin_type',
        nbins=100,
        histnorm='percent',
        barmode='overlay')

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("Les utilisateurs choisissant l'accord de location mobile rendent la voiture plus tard que ceux utilisant l'accord connect. Cela n'est pas très surprenant car, dans une location mobile, le propriétaire peut aussi être en retard pour le check-in/check-out.")

# Diagramme à barres pour la répartition des types de check-in
fig6 = px.bar(data, x='checkin_type', y='rental_id', color='checkin_type', 
              labels={'rental_id':'Nombre de locations', 'checkin_type':'Type de check-in'},
              title='Répartition des types de check-in')
st.plotly_chart(fig6, use_container_width=True)

st.markdown("nous pouvons observer que la part des locations par le bias de mobile est beaucoup plus importante que par le connect")

# Box plot pour la distribution des retards au check-out
fig7 = px.box(data, x='checkin_type', y='delay_at_checkout_in_minutes', color='checkin_type',
              labels={'delay_at_checkout_in_minutes':'Retard au check-out (minutes)', 'checkin_type':'Type de check-in'},
              title='Distribution des retards au check-out par type de check-in')
st.plotly_chart(fig7, use_container_width=True)





# Analyse du délai minimum
st.header('Quelle devrait être la durée minimale du délai ?')

data = data.dropna(subset=["time_delta_with_previous_rental_in_minutes", "delay_at_checkout_in_minutes"])
data_test = pd.melt(data, id_vars=['car_id', 'rental_id', 'state', 'checkin_type'], value_vars=['time_delta_with_previous_rental_in_minutes', 'delay_at_checkout_in_minutes'])

st.metric(label="Flotte de voitures", value=8142)

fig5 = px.pie(data, values="time_delta_with_previous_rental_in_minutes", names='checkin_type')
st.plotly_chart(fig5, use_container_width=True)

fig3 = px.ecdf(
    data_test[data_test['checkin_type'] == 'mobile'],
    x='value',
    color='variable',
    ecdfnorm='percent',
    range_x=[0, 800],
    labels={"value": 'Seuil (minutes)', "percent": 'Proportion d\'utilisateurs (%)'}
)

fig4 = px.ecdf(
    data_test[data_test['checkin_type'] == 'connect'],
    x='value',
    color='variable',
    ecdfnorm='percent',
    range_x=[0, 800],
    labels={"value": 'Seuil (minutes)', "percent": 'Proportion d\'utilisateurs (%)'}
)

data['minutes_passed_checkin_time'] = data['delay_at_checkout_in_minutes'] - data['time_delta_with_previous_rental_in_minutes']

impacted_df = data[~data["time_delta_with_previous_rental_in_minutes"].isna()]

st.header("Combien de locations sont impactées et résolues en fonction du seuil et du périmètre ?")

threshold_range = np.arange(0, 60*12, step=15) # Intervalles de 15 minutes pour 12 heures
impacted_list_mobile = []
impacted_list_connect = []
impacted_list_total = []
solved_list_mobile = []
solved_list_connect = []
solved_list_total = []

solved_list = []
for t in range(721):
    connect_impact = impacted_df[impacted_df['checkin_type'] == 'connect']
    mobile_impact = impacted_df[impacted_df['checkin_type'] == 'mobile']
    connect_impact = connect_impact[connect_impact['time_delta_with_previous_rental_in_minutes'] < t]
    mobile_impact = mobile_impact[mobile_impact['time_delta_with_previous_rental_in_minutes'] < t]
    impacted = impacted_df[impacted_df['time_delta_with_previous_rental_in_minutes'] < t]
    impacted_list_connect.append(len(connect_impact))
    impacted_list_mobile.append(len(mobile_impact))
    impacted_list_total.append(len(impacted))

    solved = impacted_df[data['minutes_passed_checkin_time'] > 0]
    connect_solved = solved[solved['checkin_type'] == 'connect']
    mobile_solved = solved[solved['checkin_type'] == 'mobile']
    connect_solved = connect_solved[connect_solved['delay_at_checkout_in_minutes'] < t]
    mobile_solved = mobile_solved[mobile_solved['delay_at_checkout_in_minutes'] < t]
    solved = solved[solved['delay_at_checkout_in_minutes'] < t]
    solved_list_connect.append(len(connect_solved))
    solved_list_mobile.append(len(mobile_solved))
    solved_list_total.append(len(solved))


# Convertir la plage en une liste pour l'argument 'x'
x_values = list(range(721))

col1, col2 = st.columns(2)
with col1:

    # Création des 3 traces
    total_impacted_cars = go.Scatter(x=x_values, y=impacted_list_total, name='Toutes les voitures', line=dict(color='royalblue'))
    impacted_connect_cars = go.Scatter(x=x_values, y=impacted_list_connect, name='Voitures Connect', line=dict(color='orange'))
    impacted_mobile_cars = go.Scatter(x=x_values, y=impacted_list_mobile, name='Voitures Mobile', line=dict(color='green'))

    # Créer la mise en page pour le graphique
    layout = go.Layout(
        title='Nombre de cas impactés par seuil',
        xaxis=dict(title='Seuil en minutes'),
        yaxis=dict(title='Nombre de cas impactés'),
        xaxis_tickvals=list(range(0, 721, 60)), # Intervalle de 60 minutes de 0 à 12h
        legend=dict(orientation='h', yanchor='bottom', xanchor='right', y=1.02, x=1)
    )

    # Créer une figure et ajouter les traces
    fig = go.Figure(data=[total_impacted_cars, impacted_connect_cars, impacted_mobile_cars], layout=layout)
    st.plotly_chart(fig, width=800, height=600, use_container_width=True)

with col2:

    # Création des 3 traces
    total_solved_cars = go.Scatter(x=x_values, y=solved_list_total, name='Toutes les voitures', line=dict(color='royalblue'))
    connect_solved_cars = go.Scatter(x=x_values, y=solved_list_connect, name='Voitures Connect', line=dict(color='orange'))
    mobile_solved_cars = go.Scatter(x=x_values, y=solved_list_mobile, name='Voitures Mobile', line=dict(color='green'))

    # Créer la mise en page pour le graphique
    layout = go.Layout(
        title='Nombre de cas résolus par seuil',
        xaxis=dict(title='Seuil en minutes'),
        yaxis=dict(title='Nombre de cas résolus'),
        xaxis_tickvals=list(range(0, 721, 60)), # Intervalle de 60 minutes de 0 à 12h
        legend=dict(orientation='h', yanchor='bottom', xanchor='right', y=1.02, x=1)
    )

    # Créer une figure et ajouter les traces
    fig = go.Figure(data=[total_solved_cars, connect_solved_cars, mobile_solved_cars], layout=layout)
    st.plotly_chart(fig, width=800, height=600, use_container_width=True)

st.subheader("Analyse des graphiques")
st.markdown("""* La courbe des cas résolus tend à se stabiliser nettement autour de **120 minutes**, voire jusqu'à 180 minutes.
* Nous pourrions être tentés de mettre en place un seuil beaucoup plus élevé afin de résoudre le plus grand nombre de cas problématiques possible.
* Mais nous sommes confrontés à un double problème : plus le seuil est élevé, plus l'impact sur le nombre de voitures disponibles et évidemment sur nos revenus est important.
* Nous devons donc trouver le bon équilibre entre le nombre de cas problématiques résolus et la proportion de revenus impactés.
* Dans cette optique, un seuil de :red[**120 minutes**] semble être un bon compromis pour notre entreprise.""")

st.write("")
st.header("Terrain de jeu dynamique des effets de seuil et de périmètre")
st.markdown("Vous pouvez ici ajuster le seuil et le périmètre souhaités pour voir les effets sur les données.")
    ## Formulaire pour le seuil et le périmètre
with st.form("threshold_testing"):
    threshold = st.slider("Choisissez le seuil en minutes", 0, 720, 0)
    checkin_type = st.radio("Choisissez le type de check-in souhaité", ["Tous", "Connect", "Mobile"])
    submit = st.form_submit_button("Voyons les résultats")

    if submit:
        # Se concentrer uniquement sur le type de check-in sélectionné
        st.markdown(f"Avec un seuil de **{threshold}** et pour un périmètre de **{checkin_type}**")
        if checkin_type == "Tous":
            st.metric(f"Le nombre de cas impactés est :", impacted_list_total[threshold])
            st.metric("Le nombre de cas résolus est :", solved_list_total[threshold])
        elif checkin_type == "Connect":
            st.metric(f"Le nombre de cas impactés est :", impacted_list_connect[threshold])
            st.metric("Le nombre de cas résolus est :", solved_list_connect[threshold])
        else :
            st.metric(f"Le nombre de cas impactés est :", impacted_list_mobile[threshold])
            st.metric("Le nombre de cas résolus est :", solved_list_mobile[threshold])










