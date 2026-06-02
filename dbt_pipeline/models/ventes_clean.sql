SELECT
    date,
    produit,
    categorie,
    quantite,
    prix_unitaire,
    (quantite * prix_unitaire) AS chiffre_affaires,
    ville
FROM {{ source('raw', 'ventes_raw') }}
WHERE quantite > 0 AND prix_unitaire > 0


