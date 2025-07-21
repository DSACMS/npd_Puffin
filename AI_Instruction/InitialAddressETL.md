Initial Address ETL
===================

Eventually we will use Smarty Streets to correct the raw address data that we.
As a result, we are storing address data in the way that Smarty Streets API returns data. You must read sql/create_table_sql/create_address.sql now.
That contains two tables, one for international addresses, and one for domestic US addresses.

Inside the raw nppes data there are multiple addresses.

You must read nppes_main/npidata_pfile_20050523-20250608.create_table_postgres.sql which is the schema for the main nppes table
that lives in the database at nppes_raw.main_file

* Provider Mailing Address
* Provider Practice Location

the endpoint file is defined in nppes_endpoint/endpoint_pfile_20050523-20250608.create_table_postgres.sql which you must read now.

In the endpoint file, there is an "affiliation address"

And of course the secondary address file nppes_pl/pl_pfile_20050523-20250608.create_table_postgres.sql (you must read this file now)
is nothing but secondary practice addresses.

When the country code of an address in the raw tables is either 'US', blank '', or NULL then assume that the data being imported should be stored in
ndh.address_us

If it has some other value, then it belongs in ndh.address_international
Every address has an entry in ndh.address

assume that address_type 1 = Service Location, address_type = 2 mailing address and address_type = fhir affiliation and address_type 4 = other.

Do not attempt to link to state codes as this time.

Please place the program code in nppes_main/post_import_scripts/Step50_import_raw_address_without_smarty.py

Use the ETL practices as described in the default directions.  

In order to ensure that we do not import addresess again and again create and table in the intake schema called raw_address_import_map

start by creating a new table, which a list of all the addresses you find, without DISTINCT.. or any other de-duplication method.
this able should have a column called address_hash which is a 32 bit md5 hash of all of the other columns after converting them to lower-case. 
This intake.raw_address_import should be deleted and re-created on every import.

Then LEFT JOIN to raw_address_import_map to create a new table called intake.address_not_mapped
Then create new ndh data for each of these unmapped addresses.

After creating these addresses, join the intake.address_not_mapped and the ndh addresses to get the ndh.address.id and the intake.address_not_mapped.address_hash and insert that data into the intake.raw_address_import_map table.

Hash all of the relevant components of the incoming addresses (after you have forced them to lower-case)

For the time being, do not concern yourself with the ndh.address_nonstandard table

__Plan Details:__

1. __Setup & Configuration:__

   - Import necessary libraries: `plainerflow`, `os`.

   - Set up the database connection using `CredentialFinder`, pointing to the `.env` file in the parent-parent directory.

   - Define `DBTable` objects for all source and destination tables to make SQL statements clean and maintainable. This includes:

     - `nppes_raw.main_file`
     - `nppes_raw.endpoint`
     - `nppes_raw.pl_file`
     - `ndh.address`
     - `ndh.address_us`
     - `ndh.address_international`
     - `ndh.npi_address`
     - `intake.raw_address_import` (temporary)
     - `intake.raw_address_import_map` (persistent mapping)
     - `intake.address_not_mapped` (temporary)

2. __Step 1: Create `raw_address_import_map` Table (if not exists)__

   - Create the `intake.raw_address_import_map` table. This table will persist between runs.
   - __Schema:__ `address_hash VARCHAR(32) PRIMARY KEY, address_id INT NOT NULL`.

3. __Step 2: Aggregate All Raw Addresses__

   - Create a temporary table `intake.raw_address_import` that will be dropped and recreated on every run.

   - This table will contain the raw, un-deduplicated addresses from all four sources.

   - __Schema:__ It will include columns for `npi`, `address_type_id`, all relevant address fields (line 1, line 2, city, state, postal code, country), and an `address_hash` column.

   - Use a `UNION ALL` query to gather addresses from:

     - __`nppes_raw.main_file` (Mailing Address):__ `address_type_id = 2`
     - __`nppes_raw.main_file` (Practice Location Address):__ `address_type_id = 1`
     - __`nppes_raw.endpoint` (Affiliation Address):__ `address_type_id = 3`
     - __`nppes_raw.pl_file` (Secondary Practice Address):__ `address_type_id = 4`

   - For each `UNION` part, calculate the `address_hash` using `MD5()` on a concatenation of all address fields, converted to lowercase and with `NULL` values coalesced to empty strings.

4. __Step 3: Identify Unmapped Addresses__

   - Create a second temporary table, `intake.address_not_mapped`.
   - Populate this table by performing a `LEFT JOIN` from `intake.raw_address_import` to `intake.raw_address_import_map` on the `address_hash`.
   - Select only the rows where the `address_id` from the map is `NULL`. This gives us a distinct list of new, unseen addresses that need to be inserted.

5. __Step 4: Insert New US Addresses__

   - Insert into `ndh.address_us` from `intake.address_not_mapped`.
   - Filter for records where the country code is 'US', blank, or `NULL`.
   - Map the raw address fields to the corresponding columns in `ndh.address_us`.

6. __Step 5: Insert New International Addresses__

   - Insert into `ndh.address_international` from `intake.address_not_mapped`.
   - Filter for records where the country code is not 'US', not blank, and not `NULL`.
   - Map the raw address fields to the corresponding columns in `ndh.address_international`.

7. __Step 6: Populate the Main `ndh.address` Table__

   - Insert into `ndh.address` by `UNION ALL`'ing the newly inserted US and International addresses.
   - For US addresses, the `address_us_id` will be populated, and `address_international_id` will be `NULL`.
   - For International addresses, the `address_international_id` will be populated, and `address_us_id` will be `NULL`.
   - This step requires joining back to `ndh.address_us` and `ndh.address_international` to get their newly generated primary keys.

8. __Step 7: Update the `raw_address_import_map`__

   - Insert the newly processed addresses into `intake.raw_address_import_map`.
   - This involves joining `intake.address_not_mapped` with the newly created records in `ndh.address` to link the `address_hash` with the new `ndh.address.id`.

9. __Step 8: Link NPIs to Addresses__

   - First, `TRUNCATE` the `ndh.npi_address` table to ensure a clean slate.
   - Insert into `ndh.npi_address` by joining the full `intake.raw_address_import` table with the now-complete `intake.raw_address_import_map` on the `address_hash`.
   - This will create the many-to-many links between NPIs and their associated addresses for this import run.

10. __Step 9: Cleanup__

    - Drop the temporary tables `intake.raw_address_import` and `intake.address_not_mapped`.
