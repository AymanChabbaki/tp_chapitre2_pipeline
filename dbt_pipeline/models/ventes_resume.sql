SELECT
    categorie,
    SUM(chiffre_affaires) AS total_chiffre_affaires,
    SUM(quantite) AS total_quantite,
    COUNT(*) AS nombre_transactions
FROM {{ ref('ventes_clean') }}
GROUP BY categorie
