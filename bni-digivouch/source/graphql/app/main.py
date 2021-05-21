import graphene, datetime
from fastapi import FastAPI
from starlette.graphql import GraphQLApp
from data import db, setup
import tinydb
import request,json

setup()

class Product(graphene.ObjectType):
    category = graphene.String(default_value="")
    brand = graphene.String()
    product_name = graphene.String()
    product_code = graphene.String()
    paid_price_by_customer = graphene.String()
    status = graphene.String()
    host_partner = graphene.String()
    biller_code = graphene.String()
    region_code = graphene.String()
    fee = graphene.String()
    
    def resolve_category(parent, info):
        return parent.category


class Request(graphene.ObjectType):
    post_quotation = """{"partnerId":"DKfMyNbLtjsP"}"""

    r = requests.post('http://dev.openapi.ayopop.id/api/v1/partner/products', json=json.loads(post_quotation))

class Inquiry(graphene.ObjectType):
    partner_id = graphene.String()
    account_number = graphene.String()
    product_code = graphene.String()
    

class Query(graphene.ObjectType):
    digital_product_list = graphene.List(Product, category=graphene.String(default_value="*"), 
    		startIndex=graphene.Int(default_value=0), endIndex=graphene.Int(default_value=1000) )
    digital_product = graphene.Field(Product, productCode=graphene.String())
    total_count = graphene.Int()
    inquiry = graphene.Field(Inquiry)
    
    def resolve_total_count(self, info):
    	return len(db)
    def resolve_digital_product_list(self, info, category, startIndex, endIndex):
    	produk = tinydb.Query()
    	list_product = []
    	cari = db.all()[startIndex: endIndex] if category=="*" else db.search(produk.Category == category)[startIndex: endIndex]
    	
    	for i in cari:
    		list_product.append(Product(category=i.get("Category"),
    								brand=i.get("Brand"),
    								product_name=i.get("ProductName"),
    								product_code=i.get("ProductCode"),
    								paid_price_by_customer=i.get("PaidPriceByCustomer"),
    								status=i.get("Status"),
                                    host_partner=i.get("HostPartner"),
                                    biller_code=i.get("BillerCode"),
                                    region_code=i.get("RegionCode"),
                                    fee=i.get("Fee")
    								))
    	return list_product
    def resolve_digital_product(self, info, productCode):
    	produk = tinydb.Query()
    	cari = db.search(produk.ProductCode==productCode)
    	if len(cari)==0: return None
    	p = Product(category=cari[0].get("Category"),
    				brand=cari[0].get("Brand"),
    				product_name=cari[0].get("ProductName"),
    				product_code=cari[0].get("ProductCode"),
    				paid_price_by_customer=cari[0].get("PaidPriceByCustomer"),
    				status=cari[0].get("Status"),
                    host_partner=cari[0].get("HostPartner"),
                    biller_code=cari[0].get("BillerCode"),
                    region_code=cari[0].get("RegionCode"),
                    fee=cari[0].get("Fee"))
    	return p
    def resolve_inquiry
app = FastAPI()
app.add_route("/graphql", GraphQLApp(schema=graphene.Schema(query=Query)))