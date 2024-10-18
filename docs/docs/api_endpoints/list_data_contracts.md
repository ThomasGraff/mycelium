## 💡 Info

- **Route**: `/`
- **Method**: `GET`
- **Description**: Retrieves a list of all data contracts from the database.

### 📥 Input

None.

### 📤 Output

- **Response Model**: `DataContractListResponse`
  - `message`: A success message indicating the data contracts were retrieved.
  - `data`: A list of data contract objects.

### Example Request

```bash
curl -X GET "https://api.example.com/"
```

### Example Response

```json
{
  "message": "✅ Data contracts retrieved successfully",
  "data": [
    {
      "contract_id": "urn:datacontract:checkout:orders-latest",
      "schema": "schema-definition",
      "description": "This is a data contract for orders."
    }
  ]
}
```
