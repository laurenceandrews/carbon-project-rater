FROM fishtownanalytics/dbt:1.0.0

WORKDIR /usr/app

# Copy the DBT project files
COPY carbon_project_rater /usr/app
# Copy the profiles.yml file to the user's home directory where DBT expects it
COPY profiles.yml /root/.dbt/profiles.yml

ENTRYPOINT ["dbt"]