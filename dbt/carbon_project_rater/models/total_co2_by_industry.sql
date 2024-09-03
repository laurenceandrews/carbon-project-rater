-- models/total_co2_by_industry.sql

WITH base AS (
    SELECT
        industry_type,
        SUM(total_mass_co2_sequestered) AS total_co2
    FROM
        {{ source('carbon_project_rater', 'carbon_project') }}
    GROUP BY
        industry_type
)

SELECT * FROM base