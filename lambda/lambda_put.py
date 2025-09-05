import json
import boto3
from botocore.exceptions import ClientError

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')

# Fungsi untuk menangani PUT request
def lambda_handler(event, context):
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