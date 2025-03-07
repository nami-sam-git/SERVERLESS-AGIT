import json
import boto3

def lambda_handler(event, context):
    # Membuat klien SQS
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.xxxxxxxxxxxxxxxxxxxxxxx/BukuTamuQueue'  # Ganti dengan URL SQS Anda

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

        # Mengembalikan respons sukses
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Izinkan akses dari semua domain
            },
            'body': json.dumps({'message': 'Data tamu berhasil dikirim ke antrian!', 'id': id})
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
