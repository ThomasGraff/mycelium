
## 💡 Info

- **Route**: `/`
- **Method**: `POST`
- **Description**: Creates a new data contract and stores it in the database.

### 📥 Input

- **Model**: `DataContractCreate`
- **Required Fields**:
  - Inherits all fields from the `DataContract` model.

### 📤 Output

- **Response Model**: `DataContractCreateResponse`
  - `message`: A success message indicating the data contract was created.
  - `data`: The created data contract object.

### Example Request

```bash
curl -X POST "https://api.example.com/" \
-H "Content-Type: application/json" \
-d '{
  "contract_id": "urn:datacontract:checkout:orders-latest",
  "schema": "schema-definition",
  "description": "This is a data contract for orders."
}'
```

### Example Response

```json
{
  "message": "✅ Data contract created successfully",
  "data": {
    "contract_id": "urn:datacontract:checkout:orders-latest",
    "schema": "schema-definition",
    "description": "This is a data contract for orders."
  }
}
```