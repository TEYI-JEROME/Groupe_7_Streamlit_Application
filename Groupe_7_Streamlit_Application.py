import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components
import time

# Titre principal de l'application
st.markdown("<h1 style='text-align: center; color: blue;'>AIMS COOP INNOVATION 2024 GROUPE 4</h1>", unsafe_allow_html=True)

# Description de l'application
with st.expander("Click here to learn more about the application"):
    st.markdown("""
    ### Welcome to our data collection application!

    This application enables the automatic extraction (web scraping) of information on various household appliances, including:
    - **Refrigerators and freezers**
    - **Air conditioners**
    - **Cookers and ovens**
    - **Washing machines**

    You can also **download the collected data** directly through the application.

    #### 🛠️ **Technologies used:**
    - `base64`
    - `pandas`
    - `streamlit`
    - `requests`
    - `bs4` (BeautifulSoup)

    #### 📚 **Data sources:**
    - <a href="https://www.expat-dakar.com/refrigerateurs-congelateurs" style="color: #FFD700;">Refrigerators and freezers</a>
    - <a href="https://www.expat-dakar.com/climatisation" style="color: #FFD700;">Air conditioners</a>
    - <a href="https://www.expat-dakar.com/cuisinieres-fours" style="color: #FFD700;">Cookers and ovens</a>
    - <a href="https://www.expat-dakar.com/machines-a-laver" style="color: #FFD700;">Washing machines</a>

    Explore the data and optimize your research with our tool! 🚀
    """, unsafe_allow_html=True)

# Fonction pour appliquer une image de fond
def background_App(image_path, image_format="jpg"):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/{image_format};base64,{base64_image}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

background_App("background_image.jpg", image_format="jpg")

# Fonction pour afficher le guide étape par étape
def show_guide():
    st.header("If you don't want to read all about our application you can use this guide")
    st.write("Welcome to the interactive guide of the app! Let's take a tour to help you understand the features.")

    # Utilisation d'un bouton pour démarrer le guide
    if 'step' not in st.session_state:
        st.session_state.step = 0  # Initialiser l'étape

    # Démarrer le guide si l'utilisateur clique sur le bouton
    if st.button("Start the guide") and st.session_state.step == 0:
        st.session_state.step = 1  # Lancer le guide à l'étape 1

    # Afficher la barre de progression
    progress_bar = st.progress(0)  # Initialiser la barre de progression à 0%

    # Gestion des étapes du guide
    if st.session_state.step == 1:
        st.write("Step 1: Explore the appliances the app scrapes data for")
        st.write("You can get data for the following appliances:")
        st.write("- Refrigerators and freezers")
        st.write("- Air conditioners")
        st.write("- Cookers and ovens")
        st.write("- Washing machines")
        
        progress_bar.progress(25)  # Met à jour la barre de progression à 25%
        
        if st.button("Next Step"):
            st.session_state.step = 2  # Passer à l'étape suivante
            time.sleep(1)  # Petit délai avant d'afficher la prochaine étape

    elif st.session_state.step == 2:
        st.write("Step 2: Learn about the technologies used in the app.")
        st.write("This app uses several technologies:")
        st.write("- `base64` for encoding data")
        st.write("- `pandas` for data manipulation")
        st.write("- `streamlit` for the web interface")
        st.write("- `requests` for HTTP requests")
        st.write("- `BeautifulSoup` for web scraping")

        progress_bar.progress(50)  # Met à jour la barre de progression à 50%

        if st.button("Next Step"):
            st.session_state.step = 3  # Passer à l'étape suivante
            time.sleep(1)

    elif st.session_state.step == 3:
        st.write("Step 3: Find the data sources used by the app.")
        st.write("Data is scraped from the following sources:")
        st.write("- [Refrigerators and freezers](https://www.expat-dakar.com/refrigerateurs-congelateurs)")
        st.write("- [Air conditioners](https://www.expat-dakar.com/climatisation)")
        st.write("- [Cookers and ovens](https://www.expat-dakar.com/cuisinieres-fours)")
        st.write("- [Washing machines](https://www.expat-dakar.com/machines-a-laver)")

        progress_bar.progress(75)  # Met à jour la barre de progression à 75%

        if st.button("Next Step"):
            st.session_state.step = 4  # Passer à l'étape suivante
            time.sleep(1)

    elif st.session_state.step == 4:
        st.write("Step 4: How to download the data.")
        st.write("After scraping, you can download the data in CSV format. Click the download button after scraping the data.")

        progress_bar.progress(100)  # Met à jour la barre de progression à 100%

        if st.button("End the guide"):
            st.session_state.step = 0  # Fin du guide et retour à l'état initial
            st.write("You have completed the guide! Feel free to explore the app further.")
            if st.button("Start again"):
                st.session_state.step = 0  # Réinitialiser et revenir au début du guide

# Afficher le guide intégré
show_guide()



# Start Web scraping 
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction pour scraper les données sur le refrigerateurs-congelateurs

def load_refrigerateurs_congelateurs(number_page):
    df = pd.DataFrame()
    for p in range(1, int(number_page) + 1):
        url = f'https://www.expat-dakar.com/refrigerateurs-congelateurs?page={p}'
        res = get(url)        
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all("div", class_='listing-card listing-card--tab listing-card--has-contact listing-card--has-content')        
        data = []
        for container in containers:
            try:
                details = container.find("div", class_="listing-card__header__title").text.strip()
                prices = container.find("span", class_="listing-card__price__value 1").text.strip().split()
                price = "".join(prices[0:2])
                eta_frigo = container.find("span", class_="listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new").text
                adresses = container.find("div", class_="listing-card__header__location").text.strip().replace(",\n ", "").split()
                adress = " ".join(adresses)
                image_link = container.find("div", class_="listing-card__image__inner").img["src"]
            
                dic = {'details': details,
                       'price': price,
                       'eta_frigo': eta_frigo,
                       'adresses': adress,
                       'image_link': image_link}
                data.append(dic)
            except:
                pass

        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

def load_cuisiniere_fours(number_page):
	
	df = pd.DataFrame()
	
	for p in range(1,int(number_page) + 1):

		url = f'https://www.expat-dakar.com/cuisinieres-fours?page={p}'
		res = get(url)
		soup = bs(res.text , 'html.parser')
		containers = soup.find_all('div', class_= 'listing-card listing-card--tab listing-card--has-contact listing-card--has-content')
		data = []
		for container in containers:
			try:
				ontainer = containers[0]
				detail = container.find("div", class_="listing-card__header__title").text.strip()
				prices = container.find("span",class_="listing-card__price__value 1").text.strip().split()
				price = "".join(prices[0:2])

				etat_cuisinier = container.find("span", class_="listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new").text
				adresse = container.find("div", class_= "listing-card__header__location").text.strip().replace(",\n ", "").split()
				adress = " ".join(adresse)
				image_link = container.find("div",class_= "listing-card__image__inner").img["src"]

				dic = {'details': detail,
					'price': price,
					'eta_clim':etat_cuisinier,
					'adresses': adress,
					'image_link':image_link,
					}
				data.append(dic)
			except:
				pass

		DF = pd.DataFrame(data)
		df= pd.concat([df, DF], axis =0).reset_index(drop = True)
		
	return df


def load_Machine_laver(number_page):

    df = pd.DataFrame()
    for p in range(1,int(number_page)+1):
        url = f'https://www.expat-dakar.com/machines-a-laver?page{p}'
        res = get(url)
        soup = bs(res.text , 'html.parser')
        containers = soup.find_all('div', class_ = 'listing-card listing-card--tab listing-card--has-contact listing-card--has-content')
        data = []
        for container in containers:
            try:
                container = containers[0]
                detail = container.find("div", class_="listing-card__header__title").text.strip()
                prices = container.find("span",class_="listing-card__price__value 1").text.strip().split()
                price = "".join(prices[0:2])

                etat_machine = container.find("span", class_="listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_used-abroad").text
                adresse = container.find("div", class_= "listing-card__header__location").text.strip().replace(",\n ", "").split()
                adress = " ".join(adresse)
                image_link = container.find("div",class_= "listing-card__image__inner").img["src"]

                dic = {'details': detail,
                    'price': price,
                    'eta_clim':etat_machine,
                    'adresses': adress,
                    'image_link':image_link,
                    }
                data.append(dic)
            except:
                pass

        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
    return df

def load_climatisation(number_page):

    df = pd.DataFrame()
    for p in range(1,int(number_page) + 1):
        url = f'https://www.expat-dakar.com/climatisation?page={p}'
        res = get(url)
        soup = bs(res.text , 'html.parser')
        containers = soup.find_all("div", class_= "listing-card listing-card--tab listing-card--has-contact listing-card--has-content")
        data = []
        for container in containers:
            try:
                details = container.find("div", class_="listing-card__header__title").text.strip()
                etat_frigo = container.find("span", class_="listing-card__header__tags__item listing-card__header__tags__item--condition listing-card__header__tags__item--condition_new").text.strip()
                adresses= container.find("div", class_="listing-card__header__location").text.strip().split()
                adress="".join(adresses)
                prices2 = container.find("span",class_= "listing-card__price__value 1").text.strip().split()
                price2 = "".join(prices1[0:2])
                image_link = container.find("div",class_= "listing-card__image__inner").img["src"]


                dic = {'details': details,
                    'price1': price1,
                    #'price2': price2,
                    'eta_frigo':etat_frigo,
                    'adresses': adress,
                    'image_link':image_link,
                        }
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df= pd.concat([df, DF], axis =0).reset_index(drop = True)
        
    return df


with st.sidebar.expander("User Input Features", expanded=True):
    Pages = st.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 300)]))
    Choices = st.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Fill the form'])

#st.sidebar.header('User Input Features')
#Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(2, 300)]))
#Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data',  'Fill the form'])

# Ajouter la description d'AIMS avec un fond rouge clair dans l'espace libre de la sidebar
with st.sidebar.expander("À propos d'AIMS", expanded=False):
    st.markdown("""
    <div style="background-color: lightyellow; padding: 10px; border-radius: 5px; color: darkred;">
    The African Institute for Mathematical Sciences (AIMS) is a pan-African network of centers of excellence for training and research in mathematical sciences. Founded in 2003, AIMS contributes to the socio-economic transformation of Africa through innovative education, scientific discoveries, and public engagement to foster the continent's scientific emergence.

    AIMS offers a Master’s program in mathematical sciences, including a cooperative option with industry, as well as research programs. AIMS also supports initiatives such as Quantum Leap Africa and the Next Einstein Forum to propel Africa onto the global scientific stage.
    </div>
    """, unsafe_allow_html=True)



local_css('style.css')

if Choices=='Scrape data using beautifulSoup':

    refrigerateurs_congelateurs_number_page = load_refrigerateurs_congelateurs(Pages) 
    cuisiniere_fours_number_page = load_cuisiniere_fours(Pages)
    Machine_laver_number_page = load_Machine_laver(Pages)
    Climatisation_number_page = load_climatisation(Pages)
    
    load(refrigerateurs_congelateurs_number_page, 'Refigerateur and congelateurs data', '1', '214')
    load(cuisiniere_fours_number_page, 'Cuisiniere and fourdata', '1', '87')
    load(Machine_laver_number_page, 'Machine a laver', '1','68')
    load(Climatisation_number_page, 'Climatisation','1','139')


elif Choices == 'Download scraped data': 

    refrigerateurs_congelateurs = pd.read_excel('data_1_url_1_refrigerateurs_congelateurs.xlsx')    
    cuisiniere_fours = pd.read_excel("data_1_url_3_cuisinieres-fours.xlsx")
    Machine_laver = pd.read_excel("data_1_url_4_machines-a-laver.xlsx")
    climatisation = pd.read_excel("data_1_url_2_climatisation.xlsx")
    
    load(refrigerateurs_congelateurs, 'refrigerateurs congelateurs', '1', '214')
    load(cuisiniere_fours, 'cuisiniere and four', '1', '87')
    load(Machine_laver,'Machine a laver','1','68')
    load(climatisation, 'Climatisation')

elif Choices == 'Dashbord of the data':
    # Charger les données
    machines = pd.read_excel('Machine_lavage_clean.xlsx')
    refrigerateurs = pd.read_excel('Refrigerateurs_clean.xlsx')
    climatiseurs = pd.read_excel('Climatiseurs_clean.xlsx')
    cuisinieres = pd.read_excel('Cuisinieres_Fours_clean.xlsx')

    # Définir des tranches pour les classes de prix
    bins = [0, 100000, 250000, 500000, 1000000, float('inf')]
    labels = ['0 - 100 000', '100 000 - 250 000', '250 000 - 500 000', '500 000 - 1 000 000', '> 1 000 000']
    for df in [machines, refrigerateurs, climatiseurs, cuisinieres]:
        df['Prix_Classé'] = pd.cut(df['Prix'], bins=bins, labels=labels)

    col1, col2 = st.columns(2)

    with col1:
        plot1 = plt.figure(figsize=(11, 7))
        color = (0.2, 0.4, 0.2, 0.6)
        plt.bar(machines['Prix_Classé'].value_counts().sort_index().index,
                machines['Prix_Classé'].value_counts().sort_index().values,
                color=color)
        plt.title('Répartition des prix des machines à laver')
        plt.xlabel('Classe de prix')
        plt.ylabel('Nombre de machines')
        st.pyplot(plot1)

    with col2:
        plot2 = plt.figure(figsize=(11, 7))
        color = (0.5, 0.7, 0.9, 0.6)
        plt.bar(refrigerateurs['Prix_Classé'].value_counts().sort_index().index,
                refrigerateurs['Prix_Classé'].value_counts().sort_index().values,
                color=color)
        plt.title('Répartition des prix des réfrigérateurs')
        plt.xlabel('Classe de prix')
        plt.ylabel('Nombre de réfrigérateurs')
        st.pyplot(plot2)

    col3, col4 = st.columns(2)

    with col3:
        plot3 = plt.figure(figsize=(11, 7))
        color = (0.9, 0.4, 0.3, 0.6)
        plt.bar(climatiseurs['Prix_Classé'].value_counts().sort_index().index,
                climatiseurs['Prix_Classé'].value_counts().sort_index().values,
                color=color)
        plt.title('Répartition des prix des climatiseurs')
        plt.xlabel('Classe de prix')
        plt.ylabel('Nombre de climatiseurs')
        st.pyplot(plot3)

    with col4:
        plot4 = plt.figure(figsize=(11, 7))
        color = (0.6, 0.3, 0.8, 0.6)
        plt.bar(cuisinieres['Prix_Classé'].value_counts().sort_index().index,
                cuisinieres['Prix_Classé'].value_counts().sort_index().values,
                color=color)
        plt.title('Répartition des prix des cuisinières et fours')
        plt.xlabel('Classe de prix')
        plt.ylabel('Nombre de cuisinières')
        st.pyplot(plot4)


else :
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/x/Rv4gHYdc" width="800" height="1100"></iframe>
    """,height=1100,width=800)

