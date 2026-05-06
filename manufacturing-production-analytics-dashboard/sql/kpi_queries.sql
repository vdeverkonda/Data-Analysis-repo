-- Daily throughput and yield
SELECT
    date,
    SUM(units_produced) AS throughput,
    ROUND(SUM(good_units) * 100.0 / SUM(units_produced), 2) AS yield_percent,
    SUM(downtime_minutes) AS downtime_minutes
FROM production_jobs
GROUP BY date
ORDER BY date;

-- Inventory variance by material
SELECT
    material,
    AVG(variance) AS avg_variance,
    SUM(ABS(variance)) AS total_absolute_variance
FROM inventory
GROUP BY material
ORDER BY total_absolute_variance DESC;

-- Downtime Pareto
SELECT
    downtime_reason,
    SUM(minutes) AS total_minutes
FROM downtime_logs
GROUP BY downtime_reason
ORDER BY total_minutes DESC;
