import json
import boto3
from botocore.exceptions import ClientError

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')

# Fungsi untuk menangani DELETE request
def lambda_handler(event, context):
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