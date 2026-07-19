

from pydantic import BaseModel



class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

product = Product(name="iPhone", price=1000, in_stock=True)



json_data = product.model_dump_json()
print(json_data)


product_obj = Product.model_validate_json(json_data)
print(product_obj)



