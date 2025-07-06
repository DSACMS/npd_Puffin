-- It is obvious that we need a mechanism to support "brand-level" searching in the NDH. This is likely not sophisticated enough but it is an OK MVP, given that we 
-- do not know for certain what should be here. 

CREATE TABLE ndh.HealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_name VARCHAR(200)   NOT NULL,
    TrademarkSerialNumber VARCHAR(20)   NOT NULL
);

CREATE TABLE ndh.OrganizationToHealthcareBrand (
    id SERIAL PRIMARY KEY,
    HealthcareBrand_id INT   NOT NULL,
    Organization_id INT   NOT NULL
);
