Python
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestion de Stock - Magasin", page_icon="📦", layout="centered"
)

st.title("📦 Alerte Réapprovisionnement Stock")
st.write(
    "Importez votre fichier CSV exporté depuis votre POS pour vérifier les stocks bas."
)

# Zone pour glisser-déposer le fichier CSV
uploaded_file = st.file_uploader(
    "Déposez votre fichier stock.csv ici", type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Vérification des colonnes nécessaires
        if "quantite" in df.columns:
            stock_critique = df[df["quantite"] <= 2]

            if not stock_critique.empty:
                st.error(
                    f"⚠️ Attention ! {len(stock_critique)} produit(s) ont un stock <= 2 pièces."
                )

                # Affichage du tableau interactif
                st.dataframe(stock_critique, use_container_width=True)

                # Préparation du fichier Excel/CSV pour la commande
                df_export = stock_critique.copy()
                df_export["Quantité à commander"] = ""
                df_export = df_export.rename(
                    columns={
                        "code_barre": "Code-Barres",
                        "nom_produit": "Désignation",
                        "quantite": "Stock Actuel",
                    }
                )

                # Conversion en CSV pour le téléchargement
                csv_data = df_export.to_csv(index=False).encode("utf-8")
                nom_fichier = (
                    f"commande_stock_{datetime.now().strftime('%Y-%m-%d')}.csv"
                )

                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger le Bon de Commande",
                    data=csv_data,
                    file_name=nom_fichier,
                    mime="text/csv",
                )
            else:
                st.success("✅ Tous les produits ont un stock supérieur à 2.")
        else:
            st.warning(
                "Le fichier CSV doit contenir une colonne nommée 'quantite'."
            )

    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
