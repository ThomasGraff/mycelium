## 💡 Info

- **Route**: `/{id}`
- **Method**: `PUT`
- **Description**: Updates an existing data contract in the database.

### 📥 Input

- **Path Parameter**: `id` (required)
  - Example: `"urn:datacontract:checkout:orders-latest"`
- **Model**: `DataContractUpdate`
  - Inherits all fields from the `DataContract` model, and all fields are optional for partial updates.

### 📤 Output

- **Response Model**: `DataContractUpdateResponse`
  - `message`: A success message indicating the data contract was updated.
  - `data`: The updated data contract object.

### Example Request

```bash
curl -X PUT "https://api.example.com/urn:datacontract:checkout:orders-latest" \
-H "Content-Type: application/json" \
-d '{
  "description": "Updated description for orders data contract."
}'
```

### Example Response

```json
{
  "message": "✅ Data contract updated successfully",
  "data": {
    "contract_id": "urn:datacontract:checkout:orders-latest",
    "schema": "schema-definition",
    "description": "Updated description for orders data contract."
  }
}
```