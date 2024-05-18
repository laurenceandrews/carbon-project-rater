-- models/project_transformation.sql
with projects as (
    select *
    from {{ source('carbon_project_rater_source', 'carbon_project') }}
)

select
    id,
    name,
    description,
    rating
from projects
