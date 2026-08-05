# Debugging the `check-auth_role` API Failure in Staging

When the `check-auth_role` API failed in the staging environment, the issue was traced using the following steps:

## 1. Check the API Logs

* Open **AWS CloudWatch**.
* Navigate to the latest logs for the **Timesheets** service.
* Review the logs for the failing `check-auth_role` API.
* The logs indicated that the **user role was missing**.

## 2. Verify the Application Code

* Locate the code where the log message was added.
* Review the implementation to ensure the API logic is correct.
* Confirm that there are **no code issues** and that the problem is not caused by the application.

## 3. Verify the Database Data

Since the issue was not in the code, the next step is to verify the staging database.

### Connect to the Staging EC2 Instance

* Log in to the **staging EC2 instance**.

### Update the Database Security Group

* Open **EC2** in the AWS Console.
* Go to **Security Groups**.
* Open the security group named **`timesheets_staging_database-sg`**.
* Add the following inbound rule:

  * **Type:** PostgreSQL
  * **Source:** `0.0.0.0/0`

> **Note:** This rule should only be used temporarily for troubleshooting. Remove it after you finish.

### Retrieve Database Credentials

* Open **AWS Systems Manager**.
* Navigate to **Parameter Store**.
* Retrieve the staging database details, including:

  * Database name
  * Username
  * Password
  * Host (if required)
  * Port (if required)

## 4. Connect to the PostgreSQL Database

* Open your preferred PostgreSQL database client.
* Enter the following details:

  * Database name
  * Username
  * Password
  * Host
  * Port
* Connect to the staging database.

## 5. Update the Database

* Verify the required records in the database.
* Execute the necessary SQL queries to update the missing or incorrect data.
* Validate that the user role is now present and retry the `check-auth_role` API.

## Summary

The CloudWatch logs confirmed that the API failure was caused by a missing user role. After verifying that there were no code issues, the staging database was accessed by temporarily updating the database security group, retrieving the credentials from Parameter Store, connecting through a PostgreSQL client, and updating the required records using SQL queries.
