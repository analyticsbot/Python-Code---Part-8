from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL
from flask.ext.cors import CORS


mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'fab@1234'
app.config['MYSQL_DATABASE_DB'] = 'Fab2UAPI'



mysql.init_app(app)

api = Api(app)
CORS(app)


class GetCustomerIdByMobile(Resource):
   def get(self):
       try:
        parser = reqparse.RequestParser()
        parser.add_argument('mobile', type=str, help='city id ')
        parser.add_argument('otp', type=str, help='salon search')
        
        args = parser.parse_args()

        _mobile = args['mobile']
        _otp = args['otp']
        
		
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_get_customer_mobile',(_mobile, _otp))
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        items_list=[];
        for item in data:
            i = {
                    'customerId':item[0],
                    'customerName':item[1]
                }
            items_list.append(i)
        
        return {'StatusCode':'200','Items':items_list}     

       except Exception as e:
            return {'error': str(e)}
			

class GetVendorsCity(Resource):
   def get(self):
       try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_bind_city')
        data = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        items_list=[];
        for item in data:
            i = {
                    'cityid':str(item[0]),
                    'cityname':str(item[1])
                }
            items_list.append(i)
        
        return {'StatusCode':'200','Items':items_list}     

       except Exception as e:
            return {'error': str(e)}


api.add_resource(GetVendorsCity, '/GetVendorsCity')		
api.add_resource(GetCustomerIdByMobile, '/GetCustomerIdByMobile')			

if __name__ == '__main__':
    app.run(debug=True)
