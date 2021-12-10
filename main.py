from google.cloud import bigquery
import sql
from pgsql import _query

if __name__ == '__main__':

    client = bigquery.Client()
    query = client.query(
        """
        SELECT geo_id, state, county, sales_vector FROM(
            SELECT c.geo_id, m.sub_region_1 AS state, m.sub_region_2 AS county, avg(m.retail_and_recreation_percent_change_from_baseline) AS sales_vector
            FROM `bigquery-public-data.census_bureau_acs.county_2017_1yr` c
            JOIN `bigquery-public-data.covid19_google_mobility.mobility_report` m 
            ON c.geo_id ||'.0' = m.census_fips_code
            WHERE c.median_rent < 2000 AND c.median_age < 30
            GROUP BY c.geo_id, state, county
            ORDER BY geo_id DESC)
        WHERE sales_vector > -15
        """
    )
    for row in query.result():
        _query(sql.insert_data, row)

    _query(sql.create_schema)
    _query(sql.create_table)
