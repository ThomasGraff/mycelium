## 💡 Info

- **Route**: `/{id}`
- **Method**: `GET`
- **Description**: Retrieves a data contract from the database by its ID.

### 📥 Input

- **Path Parameter**: `id` (required)
  - Example: `"urn:datacontract:checkout:orders-latest"`

### 📤 Output

- **Response Model**: `DataContractGetResponse`
  - `message`: A success message indicating the data contract was retrieved.
  - `data`: The retrieved data contract object.

### Example Request

```bash
curl -X GET "https://api.example.com/urn:datacontract:checkout:orders-latest"
```

### Example Response

```json
{
  "message": "✅ Data contract retrieved successfully",
  "data": {
    "contract_id": "urn:datacontract:checkout:orders-latest",
    "schema": "schema-definition",
    "description": "This is a data contract for orders."
  }
}
```