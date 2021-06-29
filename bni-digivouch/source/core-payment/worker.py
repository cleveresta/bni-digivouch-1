from kafka import KafkaConsumer, KafkaProducer
import requests, json
from string import Template


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "core-payment",
        bootstrap_servers=["localhost:9092"],
        group_id="digivouch-group",
        auto_offset_reset="latest",
        value_deserializer=lambda message: json.loads(message.decode('utf-8'))
    )

    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                            message.offset, message.key,
                                            message.value))

        x = json.loads(message.value)

        inq_id = x["inquiryId"]
        acc_num = x["accountNumber"]
        prod_code = x["productCode"]
        amnt = x["amount"]
        rf_num = x["refNumber"]
        prtnr_id = x["partnerId"]
        byr_email = x["buyerDetails"]["buyerEmail"]
        pblc_byr_id = x["buyerDetails"]["publicBuyerId"]
        cb_url = x["CallbackUrls"]
        cr_account = x["coreAccount"]
        cr_amount = x["coreAmount"]

        post_data = """<soapenv:Envelope xmlns:q0="http://service.bni.co.id/core" xmlns:bo="http://service.bni.co.id/core/bo" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
        <soapenv:Body>
            <q0:transaction>
                <request>
                    <systemId>MHP</systemId>
                        <content xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="bo:BillingPaymentReq">
                            <billerCode>0124</billerCode>
                            <regionCode>0001</regionCode>
                            <billerName>ayopop</billerName>
                            <cardNum>8696017054206000</cardNum>
                            <cardName>Digivouch-Ayopop</cardName>
                            <paymentMethod>2</paymentMethod>
                            <accountNum>${cr_account}</accountNum>
                            <trxAmount>${cr_amount}</trxAmount>
                            <feeAmount>0</feeAmount>
                            <naration>KDIURAN180700295902 VA8696017054206000 NPPJJ0P6895</naration>
                            <invoiceNum>8696017054206000</invoiceNum>
                            <journalNum/>
                            <sign>1</sign>
                            <refNo/>
                            <flag>Y</flag>
                            <amount1>${amnt}</amount1>
                            <amount2>129870.000</amount2>
                            <amount3>162339.000</amount3>
                            <amount4>0</amount4>
                            <amount5>1623376.000</amount5>
                        </content>
                    </request>
                </q0:transaction>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        r = Template(post_data)
        s = r.substitute(amnt=amnt, cr_account=cr_account, cr_amount=cr_amount)
        #print(s)
        core_response = requests.post('http://192.168.151.220:57004/CoreService', 
                    headers={'Content-type': 'application/xml'}, 
                    data=s )
        print(core_response.text)

        payload = """{"inquiryId": ${inq_id},
                "accountNumber": "${acc_num}",
                "productCode": "${prod_code}",
                "amount": ${amnt},
                "refNumber": "${rf_num}",
                "partnerId": "${prtnr_id}",
                "buyerDetails": {
                    "buyerEmail": "${byr_email}",
                    "publicBuyerId": "${pblc_byr_id}"
                },
                "CallbackUrls": [
                    "${cb_url}"
                ]
            }"""

        t = Template(payload)
        p = t.substitute(inq_id=inq_id, acc_num=acc_num, prod_code=prod_code, amnt=amnt, rf_num=rf_num,
                    prtnr_id=prtnr_id, byr_email=byr_email, pblc_byr_id=pblc_byr_id, cb_url=cb_url, 
                    cr_account=cr_account, cr_amount=cr_amount)

        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
        value_serializer=lambda m: json.dumps(p).encode('utf-8'))
        producer.send('ayopop-payment', {'test':'perdana'})
