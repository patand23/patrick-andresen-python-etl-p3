from google.cloud import bigquery
import sql
from pgsql import _query

if __name__ == '__main__':

    client = bigquery.Client()
    query = client.query("""
        SELECT geo_id, state, county, sales_vector FROM(
            SELECT geo_id, sub_region_1 AS state, sub_region_2 AS county, AVG(retail_and_recreation_percent_change_from_baseline) AS sales_vector
            FROM `bigquery-public-data.census_bureau_acs.county_2017_1yr`
            JOIN `bigquery-public-data.covid19_google_mobility.mobility_report`
            ON geo_id ||'.0' = census_fips_code
            WHERE median_rent < 2000 AND median_age < 30
            GROUP BY geo_id, state, county
            ORDER BY geo_id)
        WHERE sales_vector > -15
    """)

    _query(sql.create_schema)
    _query(sql.create_table)
    for row in query.result():
        _query(sql.insert_data, row)