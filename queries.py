import sqlite3
import pandas as pd

conn = sqlite3.connect("fraud.db")

print("\n" + "="*50)
print("  QUERY 1 — OVERVIEW")
print("="*50)
q1 = """
SELECT
  COUNT(*) as total_transactions,
  SUM(Class) as fraud_count,
  ROUND(CAST(SUM(Class) AS FLOAT)/COUNT(*)*100, 4) as fraud_rate_pct,
  ROUND(SUM(CASE WHEN Class=1 THEN Amount ELSE 0 END), 2) as total_losses,
  ROUND(AVG(CASE WHEN Class=1 THEN Amount END), 2) as avg_fraud_amount
FROM transactions
"""
print(pd.read_sql(q1, conn).to_string(index=False))

print("\n" + "="*50)
print("  QUERY 2 — LOSS BY TRANSACTION TIER")
print("="*50)
q2 = """
SELECT Amount_Tier,
  COUNT(*) as fraud_cases,
  ROUND(SUM(Amount), 2) as total_loss,
  ROUND(AVG(Amount), 2) as avg_loss
FROM transactions
WHERE Class = 1
GROUP BY Amount_Tier
ORDER BY total_loss DESC
"""
print(pd.read_sql(q2, conn).to_string(index=False))

print("\n" + "="*50)
print("  QUERY 3 — PEAK FRAUD HOURS")
print("="*50)
q3 = """
SELECT Hour,
  COUNT(*) as fraud_cases,
  ROUND(SUM(Amount), 2) as total_loss,
  ROUND(AVG(Amount), 2) as a
  vg_per_case
FROM transactions
WHERE Class = 1
GROUP BY Hour
ORDER BY total_loss DESC
LIMIT 5
"""
print(pd.read_sql(q3, conn).to_string(index=False))

print("\n" + "="*50)
print("  QUERY 4 — HIGH VALUE VS STANDARD FRAUD")
print("="*50)
q4 = """
SELECT
  CASE WHEN Amount >= 200 THEN 'High Value (over $200)'
       ELSE 'Standard (under $200)' END as segment,
  COUNT(*) as fraud_cases,
  ROUND(SUM(Amount), 2) as total_loss,
  ROUND(CAST(COUNT(*) AS FLOAT) /
    (SELECT COUNT(*) FROM transactions WHERE Class = 1) * 100, 2) as pct_of_all_fraud
FROM transactions
WHERE Class = 1
GROUP BY segment
"""
print(pd.read_sql(q4, conn).to_string(index=False))

print("\n" + "="*50)
print("  QUERY 5 — RISK LEVEL BREAKDOWN")
print("="*50)
q5 = """
SELECT Risk_Level,
  COUNT(*) as total_transactions,
  SUM(Class) as fraud_cases,
  ROUND(SUM(CASE WHEN Class=1 THEN Amount ELSE 0 END), 2) as fraud_losses,
  ROUND(CAST(SUM(Class) AS FLOAT)/COUNT(*)*100, 2) as fraud_rate_pct
FROM transactions
GROUP BY Risk_Level
ORDER BY fraud_losses DESC
"""
print(pd.read_sql(q5, conn).to_string(index=False))

conn.close()