
-- Organizations have lots of DBAs and brand names that require a many-to-one notation.. 
-- and we can define the whole concept of a higher level brand as a many-to-many name relationship..
-- If NUCC codes were reasonable, we could possibly do away with Organization Type as a seperate table.
-- But NUCC is so broken that I suspect in the future we are going to want to track data "just about SNFs"
-- JUst about Hospitals and just about FQHCs etc etc. Given that, having a org type that we control seems like an invaluable first step. 
-- Also want to clarify when I am talking about organizations that provide clinical care directly, as opposed to holding companies
-- which own clinical organizations but are not themselves clinical. Which strangely enough can also include payers.. 
-- TODO: discuss the clinical org, payer, and holding company question with Sarah and team. 

CREATE TABLE ndh.ClinicalOrganization (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_legal_name VARCHAR(200)   NOT NULL,
    AuthorizedOfficial_Individual_id INT   NOT NULL,
    ParentOrganization_id INT   NOT NULL,
    OrganizationTIN VARCHAR(10)   NOT NULL,
    primary_VTIN_id INT   NOT NULL,
    OrganizationGLIEF VARCHAR(300)   NOT NULL,
    CONSTRAINT uc_Organization_OrganizationTIN UNIQUE (
        OrganizationTIN
    )
);

CREATE TABLE ndh.VTIN (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_id INT NOT NULL,
    VTIN VARCHAR(37) NOT NULL,
    VTIN_extension_number INT NOT NULL -- defaults to 0
)


CREATE TABLE ndh.ClinicalOrgnameTypeLUT (
    id SERIAL PRIMARY KEY,
    orgname_type_description TEXT   NOT NULL,
    source_file TEXT   NOT NULL,
    source_field TEXT   NOT NULL,
    CONSTRAINT uc_OrgnameTypeLUT_orgname_description UNIQUE (
        orgname_type_description
    )
);

CREATE TABLE ndh.Orgname (
    id SERIAL PRIMARY KEY,
    ClinicalOrganization_id INT   NOT NULL,
    ClinicalOrganization_name VARCHAR(70)   NOT NULL,
    ClinicalOrgnameType_id INTEGER   NOT NULL
);
