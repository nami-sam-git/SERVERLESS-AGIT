import json
import boto3
from botocore.exceptions import ClientError

# Inisialisasi klien DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')

def lambda_handler(event, context):
    try:
        # Ambil HTTP method dari event
        http_method = event['httpMethod']
        
        # Handle GET request (Mengambil semua tamu)
        if http_method == 'GET':
            return handle_get(event)
        
        # Handle POST request (Menambahkan tamu baru)
        elif http_method == 'POST':
            return handle_post(event)
        
        # Handle PUT request (Memperbarui tamu)
        elif http_method == 'PUT':
            return handle_put(event)
        
        # Handle DELETE request (Menghapus tamu)
        elif http_method == 'DELETE':
            return handle_delete(event)
        
        # Jika method tidak dikenali
        else:
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'message': 'Method not allowed'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }

# Fungsi untuk menangani GET request
def handle_get(event):
    try:
        # Ambil semua data dari tabel
        response = table.scan()
        
        # Jika tidak ada data, buat data awal
        if not response['Items']:
            initial_data = [
                {'id': '1', 'nama': 'Agus', 'pesan': 'Samawa ya gaes'},
                {'id': '2', 'nama': 'Bambang', 'pesan': 'Sugeng ndalu'},
                {'id': '3', 'nama': 'Cheryl', 'pesan': 'GWS yah'},
                {'id': '4', 'nama': 'Darsimin', 'pesan': 'Semoga langgeng'},
                {'id': '5', 'nama': 'Eriana', 'pesan': 'Selamat menempuh hidup baru, salam dari Bapak'}
            ]
            
            # Masukkan data awal ke tabel
            for item in initial_data:
                table.put_item(Item=item)
            
            # Ambil data lagi setelah memasukkan data awal
            response = table.scan()
        
        # Kembalikan data tamu
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response['Items'])
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }

# Fungsi untuk menangani POST request
def handle_post(event):
    try:
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Generate ID unik (contoh menggunakan timestamp)
        import time
        id = str(int(time.time()))
        
        # Masukkan data ke tabel
        table.put_item(Item={
            'id': id,
            'nama': nama,
            'pesan': pesan
        })
        
        # Kembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Tamu berhasil ditambahkan!', 'id': id})
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }

# Fungsi untuk menangani PUT request
def handle_put(event):
    try:
        # Ambil ID dari path parameter
        id = event['pathParameters']['id']
        
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Perbarui data di tabel
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET nama = :nama, pesan = :pesan',
            ExpressionAttributeValues={
                ':nama': nama,
                ':pesan': pesan
            }
        )
        
        # Kembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Tamu berhasil diperbarui!'})
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }

# Fungsi untuk menangani DELETE request
def handle_delete(event):
    try:
        # Ambil ID dari path parameter
        id = event['pathParameters']['id']
        
        # Hapus data dari tabel
        table.delete_item(Key={'id': id})
        
        # Kembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Tamu berhasil dihapus!'})
        }
    
    except ClientError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': str(e)})
        }
