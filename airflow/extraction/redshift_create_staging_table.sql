--Intermediary table to receive data from S3, after receiving we transfer it into our real table
-- If ID already exists in table, remove it, and insert the updated one
CREATE TABLE IF NOT EXISTS our_staging_table(
LIKE redshift_table
);