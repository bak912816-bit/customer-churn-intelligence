
-- 1. Taux de churn global
SELECT
    Churn,
    COUNT(*) AS nombre_clients,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pourcentage
FROM customers
GROUP BY Churn
ORDER BY Churn;


-- 2. Churn par type de contrat
SELECT
    Contract,
    COUNT(*) AS nombre_clients,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE Churn = TRUE) / COUNT(*),
        2
    ) AS taux_churn
FROM customers
GROUP BY Contract
ORDER BY taux_churn DESC;


-- 3. Churn par méthode de paiement
SELECT
    PaymentMethod,
    COUNT(*) AS nombre_clients,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE Churn = TRUE) / COUNT(*),
        2
    ) AS taux_churn
FROM customers
GROUP BY PaymentMethod
ORDER BY taux_churn DESC;


-- 4. Churn par ancienneté
SELECT
    CASE
        WHEN tenure <= 12 THEN '0-12 mois'
        WHEN tenure <= 24 THEN '13-24 mois'
        WHEN tenure <= 48 THEN '25-48 mois'
        ELSE '49-72 mois'
    END AS groupe_anciennete,
    COUNT(*) AS nombre_clients,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE Churn = TRUE) / COUNT(*),
        2
    ) AS taux_churn
FROM customers
GROUP BY groupe_anciennete
ORDER BY MIN(tenure);
