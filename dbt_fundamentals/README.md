# dbt Fundamentals

## dbt and the ADLC

### ETL vs ELT: two data strategies

- **ETL - Extract, Transform, Load**

    ![](../images/etl.png)

- **ELT - Extract, Load, Transform**

    ![](../images/elt.png)

Benefits to using ELT over ETL
- Leverage cloud infrastructure: ELT takes advantage of the massive processing power of CDWs like Snowflake, BigQuery, and Redshift
- Faster data availability
- Cost efficiency: ELT reduces the need for expensive on-premises hardware or complex ETL tools
- Flexible, iterative transformation
- Data democratization: ELT enables analysts and data teams can access and transform data as needed without being bottlenecked by upstream ETL processes

dbt plays a crucial role in the ELT process by serving as the transformation layer within the data warehouse with dbt features
- **Version-controlled transformations**: dbt enables version control for all transformations, making it easy to track changes and collaborate across teams
- **Automation and scheduling**: With dbt, you can automate transformation processes, ensuring that the most up-to-date data is always available for analysis
- **Comprehensive testing**: dbt offers built-in testing capabilities to validate transformations, ensuring data quality and integrity throughout the ELT process

### Data Team Roles

|| Data Engineer | Analytics engineer | Data Analyst |
|:-----|:-----|:-----|:-----|
| Definition | Data engineers build systems to collect and process data (data pipeline) | Analytics engineering is a relatively recent data team role. An analytics engineer is a valuable addition to a data team | Data analysts evaluate transformed data and turn that into business insights. They answer questions using data analysis methods. Their focus is on solving business problems |
| Key roles | Designing data infrastructure and architecture<br> Creating and maintaining data pipelines<br> Ensuring data quality and availability | Exploration: Exploring data already ingested into data platforms in response to stakeholder questions and needs<br> Preparation: Cleaning and preparing datasets for analytics use cases<br> Transformation: Transforming prepared datasets into objects that can serve organizational objectives, such as a super-table that can serve as a base for multiple applications<br> Documentation: Documenting the objects they find and create in the data warehouse, ensuring that other users can also see, understand, and use them | Interpreting data to find trends<br> Creating reports and visualizations<br> Working closely with business stakeholders |

### dbt

**ADLC - Analytics Development Lifecycle**

![](../images/adlc.png)

- Provides a structured process for building, testing, reviewing, and deploying analytics
- Encourages iteration and collaboration so teams can confidently move from idea to production
- Aligns data work with software engineering best practices, such as version control, testing, and continuous improvement

**dbt as the Data Control Plane**

- dbt orchestrates and governs the ADLC across your data ecosystem
- It ensures consistency in how data is developed, tested, documented, and deployed
- By serving as the “control plane,” dbt integrates with the modern data stack to enforce trust, scalability, and readiness for AI-driven use cases

## Getting Started

In this demo, you need to set up [VSCode](https://code.visualstudio.com/download), [dbt Core](https://docs.getdbt.com/docs/local/install-dbt?version=2.0#dbt-core), a [data platform](https://docs.getdbt.com/docs/supported-data-platforms) and a Git provider, e.g., [GitHub](https://github.com/) to get started with dbt (follow to [this guide](https://docs.getdbt.com/guides/manual-install))

Here I choose **PostgreSQL** as a data platform because I'm quite familiar with it

### First Step Demo

1. `dbt init jaffle_shop`
    - Create a new dbt project named **jaffle_shop**
    - Then, you enter the information as shown in the image below

        ![](../images/dbt_init.png)

    - `cd jaffle_shop`
    - Two important files
        - `dbt_project.yml` file, which contains important information that tells dbt how to operate your project
        - `profiles.yml` file, which stores database connection credentials and configuration for dbt projects

2. `docker run --name postgres-dbt -e POSTGRES_PASSWORD=your_password -d -p 5432:5432 -v postgres-data:/var/lib/postgresql/data postgres:16`
    - Starting a Postgres instance with default user and database is `postgres`
    - `dbt debug`: test the database connection

        ![](../images/dbt_debug.png)

3. `dbt run`
    - Run the models in the project (defined in `models/`)
    - The result looks like in below

        ![](../images/dbt_run_1.png)

4. **Commit and push the changes**

- Create a repo on Github
- Then, enter the following commands

    ```bash
    git init
    git branch -M main
    git add .
    git commit -m "Init a dbt project"
    git remote add origin github_repo_url
    git push -u origin main
    ```

### Build First dbt Model

**Setup**

- Check out a new git branch to work on new code: `git checkout -b add-customers-model`
- Run a setup script (ensure PostgreSQL instance is running): `python3 setup.py`

**Run a dbt Project**

- `dbt run`

    ![](../images/dbt_run_2.png)

- Demystifying the components of dbt project

    - Each dbt model are **materialized**, which is strategies for persisting dbt models in a warehouse (e.g., view, table). Materialization configurations are defined in `dbt_project.yml`

        ![](../images/materialization_config.png)

    - `{{ ref() }}` macro (pieces of code that can be reused multiple times): this function defines how you reference one model within another. Here, `dim_customers.sql` refers to both `stg_jaffle_shop__customers.sql` and `stg_jaffle_shop__orders.sql`
        
        ![](../images/ref.png)

    - dbt models are structured according to [this DBT best practice](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)

        ```bash
        staging/
        marts/
        ```




