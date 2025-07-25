import requests

BASE_URL = "http://127.0.0.1:8000/api"  # Change this to your API base URL

def print_result(test_name, passed, expected=None, got=None, request_data=None, response_body=None):
    if passed:
        print(f"✓ {test_name}: PASSED")
    else:
        print(f"✗ {test_name}: FAILED")
        if request_data:
            print(f"  Request: {request_data}")
        if expected is not None and got is not None:
            print(f"  Expected: {expected}, Got: {got}")
        if response_body:
            print(f"  Response Body: {response_body}")

def test_register_user():
    """
    Change payload keys/values as needed for your registration API.
    Expected status codes are 201 (created) or 409 (conflict if user exists).
    """
    payload = {"username": "puja", "password": "mypassword"}  # Change username/password if needed
    res = requests.post(f"{BASE_URL}/register/", json=payload)
    passed = res.status_code in [201, 409]
    print_result("User Registration", passed, "201 or 409", res.status_code, payload, res.text)

def test_login():
    """
    Change payload for different username/password.
    On success, expects 200 status and an 'access_token' in JSON response.
    Returns the token for authenticated requests.
    """
    payload = {"username": "puja", "password": "mypassword"}  # Change to test different login credentials
    res = requests.post(f"{BASE_URL}/login/", json=payload)
    token = None
    passed = False
    if res.status_code == 200:
        try:
            token = res.json().get("access")
            passed = token is not None
        except Exception:
            passed = False
    print_result("Login Test", passed, "200 with access_token", res.status_code, payload, res.text)
    print("token:::: ", token)
    return token

def test_add_product(token):
    """
    Change payload fields as per your product API requirements.
    Must include Authorization header with Bearer token.
    Returns product_id on success to be used in other tests.
    """
    payload = {
        "name": "Phone",  # Change product name
        "type": "Electronics",  # Change type/category
        "sku": "PHN-001",  # Change SKU if needed
        "image_url": "https://example.com/phone.jpg",  # Change image URL
        "description": "Latest Phone", # Change description
        "quantity": 5, # Initial quantity
        "price": 999.99 # Price
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/products/", json=payload, headers=headers)
    product_id = None
    passed = False
    
    if res.status_code == 201:
        try:
            response_data = res.json()
            product_id = response_data.get("id") or response_data.get("product_id")
            passed = product_id is not None
        except Exception:
            passed = False
    # product_id = 4
    print_result("Add Product", passed, "201 with product ID", res.status_code, payload, res.text)
    return product_id

def test_get_products(token):
    """Test GET /api/products/ endpoint"""
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/products/", headers=headers)
    passed = res.status_code == 200
    print_result("Get Products", passed, 200, res.status_code, None, res.text)

# def test_get_product_by_id(token, product_id):
#     """Test GET /api/products/{id}/ endpoint"""
#     if product_id is None:
#         print_result("Get Product by ID", False, "Product ID required", "None", None, "No product ID provided")
#         return
    
#     headers = {"Authorization": f"Bearer {token}"}
#     res = requests.get(f"{BASE_URL}/products/{product_id}/", headers=headers)
#     passed = res.status_code == 200
#     print_result("Get Product by ID", passed, 200, res.status_code, f"Product ID: {product_id}", res.text)

def test_update_product(token, product_id):
    """Test PUT /api/products/{id}/ endpoint"""
    if product_id is None:
        print_result("Update Product", False, "Product ID required", "None", None, "No product ID provided")
        return
    
    payload = {
        "quantity" : 7
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.put(f"{BASE_URL}/products/{product_id}/quantity/", json=payload, headers=headers)
    passed = res.status_code == 200
    print_result("Update Product", passed, 200, res.status_code, payload, res.text)



def main():
    print("Starting Inventory Management API Tests...")
    print(f"Testing against: {BASE_URL}")
    print("-" * 50)
    
    # Test 1: Register User
    test_register_user()
    
    # Test 2: Login
    token = test_login()
    print("Token,...,,.,.,.,.,. ",token)
    
    if token:
        print(f"\nAuthentication successful. Token: {token[:20]}...")
        
        # Test 3: Add Product
        product_id = test_add_product(token)
        
        # Test 4: Get Products
        test_get_products(token)
        
        # Test 5: Get Product by ID
        # test_get_product_by_id(token, product_id)
        
        # Test 6: Update Product
        test_update_product(token, product_id)
        
        # Test 7: Delete Product
        # test_delete_product(token, product_id)
    else:
        print("\nSkipping authenticated tests due to login failure.")
    
    print("-" * 50)
    print("API Tests Completed!")

if __name__ == "__main__":
    main()