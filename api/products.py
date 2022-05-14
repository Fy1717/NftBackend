from flask import jsonify, Blueprint, request

apiProducts = Blueprint("apiProducts", __name__, url_prefix="/api/products")

from ecommerce.models import Product

''' from ecommerce.jwtAuthorize import login_required
 '''

@apiProducts.route("/")
def products():
    try:
        allProducts = Product.get_all_products()
        products = []

        for product in allProducts:
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "oldPrice": product.oldPrice,
                    "description": product.description,
                    "category_id": product.category_id,
                    "image": product.image,
                }
            )

        return jsonify({"success": True, "data": products, "count": len(products)})

    except Exception as e:
        print("ERROR IN PRODUCTS: ", e)
        return jsonify({"message": "There is an error.."}), 400

@apiProducts.route("/filterByCategory/<int:categoryId>")
def getProductsForCategory(categoryId):
    try:
        allProductsForCategory = Product.get_products_for_category(categoryId)

        products = []

        for product in allProductsForCategory:
            products.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "oldPrice": product.oldPrice,
                    "description": product.description,
                    "category_id": product.category_id,
                    "image": product.image,
                }
            )

        return jsonify({"success": True, "data": products, "count": len(products)})
    except Exception as e:
        print("ERROR IN PRODUCTS FOR CATEGORY: ", e)
        return jsonify({"message": "There is an error.."}), 400

@apiProducts.route("/addProduct", methods=["POST"])
def addproduct():
    try:
        name = request.form.get("name")
        price = request.form.get("price")
        oldPrice = request.form.get("oldPrice")
        description = request.form.get("description")
        category_id = request.form.get("categoryId")
        image = request.form.get("image")

        if name == None:
            return jsonify({"message": "Name is required"}), 400
        if price == None:
            return jsonify({"message": "Price is required"}), 400
        if oldPrice == None:
            oldPrice = price
        if description == None:
            return jsonify({"message": "Description is required"}), 400
        if category_id == None:
            return jsonify({"message": "Category is required"}), 400
        if image == None:
            return jsonify({"message": "Image is required"}), 400

        Product.add_product(name, price, oldPrice, description, category_id, image)

        return jsonify({"success": True, "message": "Product added successfully"})
    except Exception as e:
        print("ERROR in add_admin: ", e)
        return jsonify({"message": "There is an error.."}), 400


@apiProducts.route("/<int:id>", methods=["GET"])
def getProduct(id):
    try:
        product = Product.get_product_by_id(id)

        if product is None:
            return jsonify({"message": "Product not found"}), 400

        if request.method == "GET":
            productObj = {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "oldPrice": product.oldPrice,
                "description": product.description,
                "category_id": product.category_id,
                "image": product.image,
            }

            return jsonify({"success": True, "data": productObj})
    except Exception as e:
        print("ERROR in product: ", e)
        return jsonify({"message": "There is an error.."}), 400

@apiProducts.route("/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        product = Product.get_product_by_id(id)

        if product is None:
            return jsonify({"message": "Product not found"}), 400

        elif request.method == "DELETE":
            Product.delete_product(id)

            return jsonify({"success": True, "message": "product deleted"})

    except Exception as e:
        print("ERROR in product: ", e)
        return jsonify({"message": "There is an error.."}), 400

@apiProducts.route("/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        product = Product.get_product_by_id(id)

        if product is None:
            return jsonify({"message": "Product not found"}), 400

        elif request.method == "PUT":
            name = request.form.get("name")
            price = request.form.get("price")
            oldPrice = request.form.get("oldPrice")
            description = request.form.get("description")
            category_id = request.form.get("categoryId")
            image = request.form.get("image")

            if name == None:
                name = product.name
            if price == None:
                price = product.price
            if oldPrice == None:
                oldPrice = product.oldPrice
            if description == None:
                description = product.description
            if category_id == None:
                category_id = product.category_id
            if image == None:
                image = product.image

            Product.update_product(id, name, price, oldPrice, description, category_id, image)

            return jsonify({"success": True, "message": "product updated"})
    except Exception as e:
        print("ERROR in product: ", e)
        return jsonify({"message": "There is an error.."}), 400
            