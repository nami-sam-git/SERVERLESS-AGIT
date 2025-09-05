import json
import boto3
from botocore.exceptions import ClientError

# Inisialisasi klien DynamoDB dan SQS
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('BukuTamuTable')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/694368835432/BukuTamuQueue'  # Ganti dengan URL SQS Anda

# Fungsi untuk menangani POST request
def lambda_handler(event, context):
    try:
        # Parse data dari body request
        body = json.loads(event['body'])
        nama = body['nama']
        pesan = body['pesan']
        
        # Generate ID unik (contoh menggunakan timestamp)
        import time
        id = str(int(time.time()))
        
        # Buat pesan untuk dikirim ke SQS
        message = {
            'id': id,
            'nama': nama,
            'pesan': pesan
        }
        
        # Kirim pesan ke SQS
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message)
        )
        
        # Kembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'message': 'Data tamu berhasil dikirim ke antrian!', 'id': id})
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