import json
import boto3

def lambda_handler(event, context):
    # Membuat klien DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BukuTamuTable')
    
    try:
        # Ambil ID dari path parameter
        id = event['pathParameters']['id']
        
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Perbarui item di tabel
        table.update_item(
            Key={'id': id},
            UpdateExpression='SET nama = :nama, pesan = :pesan',
            ExpressionAttributeValues={
                ':nama': nama,
                ':pesan': pesan
            }
        )
        
        # Mengembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Izinkan akses dari semua domain
            },
            'body': json.dumps({'message': 'Tamu berhasil diperbarui!'})
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
