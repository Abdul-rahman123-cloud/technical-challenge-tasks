# AWS 3-Tier Architecture Challenge Repository

## Overview

This repository contains a solution for a multi-part software engineering challenge. The solution demonstrates:

- **Task 1:** A complete 3-tier architecture application for inventory management deployed on AWS.
  - **Tier 1 (Presentation):** A front-end interface (`index.html`) hosted on AWS Amplify.
  - **Tier 2 (Application Logic):** AWS Lambda functions implementing business logic to fetch, add, and update inventory.
  - **Tier 3 (Data):** A DynamoDB table that stores the inventory data.
- **Task 2:** A Lambda function that retrieves metadata from an AWS EC2 instance and returns it as JSON, with the ability to query specific metadata keys.
- **Task 3:** A Lambda function that accepts a nested JSON object and a key path (using `/` as a separator) to extract and return the corresponding value.

The code is organized to showcase a reproducible, robust, and scalable solution, following software engineering best practices.

## Repository Structure

```
.
├── README.md
├── task1_tier2_fetch_inventory.py       # Lambda: Fetch inventory items from DynamoDB (Task 1 Tier 2)
├── task1_tier2_inventory_management.py   # Lambda: Business logic to add/update inventory (Task 1 Tier 2)
├── index.html                            # Front-end interface deployed via AWS Amplify (Task 1 Tier 1)
├── task1_tests.txt                       # Test cases for Task 1 Lambda functions
├── task2-metadata.py                     # Lambda: Query EC2 instance metadata (Task 2)
└── task3_nested_objects.py               # Lambda: Extract value from a nested JSON object (Task 3)
```

## Detailed Explanation & Alignment with Challenge Requirements

### Task 1: 3-Tier Inventory Management Application

#### **Architecture Overview:**

- **Tier 1 – Front-End (Presentation Layer):**
  - **File:** `index.html`
  - **Deployment:** Hosted on AWS Amplify ([Test it here](https://main.d1g0jgan4hvjfw.amplifyapp.com/))
  - **Function:** Provides a user interface using HTML, CSS (via Bootstrap), and JavaScript. It allows users to view the current inventory, add new items, or update item quantities by calling AWS Lambda endpoints.

- **Tier 2 – Application Logic (Business Logic Layer):**
  - **Files:** 
    - `task1_tier2_fetch_inventory.py`: A Lambda function that scans the DynamoDB table and retrieves all inventory items.
    - `task1_tier2_inventory_management.py`: A Lambda function that contains logic for:
      - **Adding a new item:** Generates a random product ID, validates inputs, and writes the item to the DynamoDB table.
      - **Updating an item:** Validates inputs and updates the quantity of the given product in the DynamoDB table.

- **Tier 3 – Data Layer:**
  - **Resource:** AWS DynamoDB Table (`inventory-db`)
  - **Function:** Stores the inventory data which is accessed and modified by the Lambda functions.

#### **How It Aligns with the Requirements:**

- **3-Tier Architecture:** The solution clearly separates the user interface (Amplify-hosted index.html), business logic (Lambda functions), and data storage (DynamoDB).
- **Reproducibility & Robustness:** Each Lambda function includes input validation, error handling, and standardized JSON responses to ensure consistent behavior.
- **Testing:** The provided test cases in `task1_tests.txt` describe how to verify both the add and update functionalities.

---

### Task 2: EC2 Instance Metadata Retrieval

- **File:** `task2-metadata.py`
- **Functionality:**
  - Uses the AWS SDK (`boto3`) to call `describe_instances` and extract metadata (e.g., instanceId, instanceType, launchTime, etc.) from a specific EC2 instance.
  - Supports querying the entire metadata set or retrieving a single key if provided via path parameters.
- **Testing:** 
  - **Test 1:** Retrieves all metadata.
  - **Test 2:** Retrieves a specific metadata key (e.g., `instanceId`).

---

### Task 3: Nested Object Value Extraction

- **File:** `task3_nested_objects.py`
- **Functionality:**
  - Accepts a nested JSON object and a key path string (formatted with `/` as a separator).
  - Traverses the object to extract the value corresponding to the provided key path.
- **Testing:**
  - **Example 1:** Given `{ "a": { "b": { "c": "d" } } }` with key path `a/b/c`, the function returns `"d"`.
  - **Example 2:** Given `{ "x": { "y": { "z": "a" } } }` with key path `x/y/z`, the function returns `"a"`.

---

## How to Test and Use the Project

### Testing AWS Lambda Functions

#### Task 1: Inventory Management

1. **Fetch Inventory:**
   - **Endpoint:** [Fetch Inventory](https://lgxymwdzhitho5nglp3se4gfce0yposx.lambda-url.us-east-1.on.aws/)
   - **Test:** Send a GET request. The function will return all items stored in the DynamoDB table.

2. **Add Item:**
   - **Endpoint:** [Inventory Management](https://ya5t24xky6tgjpl6ohckb42ljq0tysdn.lambda-url.us-east-1.on.aws/)
   - **Test Payload:**
     ```json
     {
       "action": "add_item",
       "product_name": "Notebook",
       "quantity": 100
     }
     ```

3. **Update Item:**
   - **Endpoint:** [Inventory Management](https://ya5t24xky6tgjpl6ohckb42ljq0tysdn.lambda-url.us-east-1.on.aws/)
   - **Test Payload:**
     ```json
     {
       "action": "update_item",
       "product_id": "ab123",
       "quantity": 75
     }
     ```

#### Task 2: EC2 Metadata Retrieval

- **Get All Metadata:**
  ```json
  {
    "httpMethod": "GET",
    "path": "/metadata",
    "pathParameters": null
  }
  ```

- **Get Specific Metadata:**
  ```json
  {
    "httpMethod": "GET",
    "path": "/metadata/instanceId",
    "pathParameters": {
      "key": "instanceId"
    }
  }
  ```

#### Task 3: Nested Object Extraction

- **Test Example 1:**
  ```json
  {
    "object": {
      "a": {
        "b": {
          "c": "d"
        }
      }
    },
    "key": "a/b/c"
  }
  ```

- **Test Example 2:**
  ```json
  {
    "object": {
      "x": {
        "y": {
          "z": "a"
        }
      }
    },
    "key": "x/y/z"
  }
  ```

---

## Conclusion

This repository demonstrates a well-structured, multi-tier AWS solution aligned with the challenge requirements. It illustrates the separation of concerns by isolating the presentation, business logic, and data storage layers. Additionally, tasks for querying EC2 metadata and extracting nested JSON values further showcase the use of AWS Lambda to solve diverse problems.

For further information, testing details, or to view the source code, please refer to the respective files in the repository.
