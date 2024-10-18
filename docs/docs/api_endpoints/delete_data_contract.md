## 💡 Info

- **Route**: `/{id}`
- **Method**: `DELETE`
- **Description**: Deletes an existing data contract from the database.

### 📥 Input

- **Path Parameter**: `id` (required)
  - Example: `"urn:datacontract:checkout:orders-latest"`

### 📤 Output

- **Response Model**: `DataContractDeleteResponse`
  - `message`: A success message indicating the data contract was deleted.
  - `data`: The deleted data contract object.

### Example Request

```bash
curl -X DELETE "https://api.example.com/urn:datacontract:checkout:orders-latest"
```

### Example Response

```json
{
  "message": "✅ Data contract deleted successfully",
  "data": {
    "contract_id": "urn:datacontract:checkout:orders-latest",
    "schema": "schema-definition",
    "description": "This is a data contract for orders."
  }
}
```
