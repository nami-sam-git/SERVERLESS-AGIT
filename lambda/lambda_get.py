import json
import boto3

def lambda_handler(event, context):
    # Membuat klien DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BukuTamuTable')
    
    try:
        # Scan untuk mengambil semua item dari tabel
        response = table.scan()
        
        # Jika tidak ada item yang ditemukan, buat 5 baris data awal
        if not response['Items']:
            initial_data = [
                {'id': '1', 'nama': 'Agus', 'pesan': 'Samawa ya gaes'},
                {'id': '2', 'nama': 'Bambang', 'pesan': 'Sugeng ndalu'},
                {'id': '3', 'nama': 'Cheryl', 'pesan': 'GWS yah'},
                {'id': '4', 'nama': 'Darsimin', 'pesan': 'Semoga langgeng'},
                {'id': '5', 'nama': 'Eriana', 'pesan': 'Selamat menempuh hidup baru, salam dari Bapak'}
            ]
            
            # Masukkan data awal ke dalam tabel
            for item in initial_data:
                table.put_item(Item=item)
            
            # Scan lagi untuk mengambil data yang baru saja dimasukkan
            response = table.scan()
        
        # Mengembalikan data tamu
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Izinkan akses dari semua domain
            },
            'body': json.dumps(response['Items'])  # Langsung kembalikan array objek
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Izinkan akses dari semua domain
            },
            'body': json.dumps({'message': str(e)})
        }
