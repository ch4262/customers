# Customers API

[![Build Status](https://github.com/CSCI-GA-2820-SU24-001/customers/actions/workflows/ci.yml/badge.svg)](https://github.com/CSCI-GA-2820-SU24-001/customers/actions)
[![codecov](https://codecov.io/github/CSCI-GA-2820-SU24-001/customers/graph/badge.svg?token=284AWMT30I)](https://codecov.io/github/CSCI-GA-2820-SU24-001/customers)

## Introduction
This is the RESTful API for manageing customers. It allows you to create, retrieve, update, and delete customers.

## Getting Started
Clone this repository and open the folder in a container. 

## API Endpoints

### POST /customers
- **Method:** POST
- **Description:** Creates a customer.

### GET /customers/<int:customer_id>
- **Method:** GET
- **Description:** Read an existing customer with specific customer ID.

### PUT /customers/<int:customer_id>
- **Method:** PUT
- **Description:** Update an existing customer.

### GET /customers
- **Method:** GET
- **Description:** List existing customers and query customer attributes like name, email, address, phone number and member since

### DELETE /customers/<int:customer_id>
- **Method:** DELETE
- **Description:** Delete an existing customer with specific customer ID.

### PUT /customers/<int:customer_id>/suspend
- **Method:** PUT
- **Description:** Suspend an existing customer with specific customer ID.

## Error Handling
The API returns a JSON object with a status code and a string message when an error occurs. For example, `{ status.HTTP_404_NOT_FOUND, f"Customer with id '{customer_id}' was not found.", }`.

## Testing
Run 'make test' to execute the test suite.

## Kubernetes
- **Create cluster:** Run 'make cluster' to create a kubernetes cluster
- **Delete cluster:** Run 'make cluster-rm' to create a kubernetes cluster
- **Display what is running in kubernetes cluster:** kubectl get all
- **Create a secret:** kubectl create secret generic customers-creds --from-literal=database_uri=$DATABASE_URI
- **Retrieve the secret:** kubectl get secrets customers-creds -o yaml
- **Check the secret:** echo -n <secret value>| base64 -d 
- **Create a customer service:** kubectl get secrets
  - Apply persistent volume: kubectl apply -f k8s/pv.yaml
  - Verify that the persistent volume was created: kubectl get pv
  - Apply redis to the cluster: kubectl apply -f k8s/service.yaml
- **Delete a service:** kubectl delete -f k8s/
- **Create a customer namespace (optional):** kubectl create namespace customer
- **Enter the customer namespace (optional):** kubectl config set-context --current --namespace customer