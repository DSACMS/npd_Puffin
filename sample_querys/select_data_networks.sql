-- read the contents of ./sql/create_table_sql as needed to understand the structure of the underlying database.
-- this sample qquery does a SELECT * on the ndh.data_network table and then joins in the FHIR endpoint for that data network using two JOINS

SELECT
    data_network.data_network_name,
    data_network.data_network_blurb,
    data_network.data_network_homepage_url,
    interop_endpoint.fhir_endpoint_url,
    interop_endpoint.endpoint_name,
    interop_endpoint.endpoint_desc
FROM
    ndh.data_network AS data_network
JOIN
    ndh.data_network_interop_endpoint AS data_network_interop_endpoint
    ON data_network.id = data_network_interop_endpoint.data_network_id
JOIN
    ndh.interop_endpoint AS interop_endpoint
    ON data_network_interop_endpoint.interop_endpoint_id = interop_endpoint.id;
