from ifirma.request import sign_raw, Request
from stubs import (
   SAMPLE_API_USER, 
   SEND_EMAIL_WITH_INVOICE_REQUEST
)

SAMPLE_API_KEY='EAB0D8ACF3308F3B'

args = dict(api_user=SAMPLE_API_USER, api_key=SAMPLE_API_KEY)

def test_sign():
    # example data from https://api.ifirma.pl/faq/
    assert '1558ab6c5ab2b0d1cd129b9ad11527cf33486705' == sign_raw('222222', b'111111')
    assert 'cec153ee6350475f117a307111e2bd7d83034925' == sign_raw('222222', '111111')

def test_sign_get_invoices_list_request():
    from datetime import date, timedelta
    df = date(1970, 1, 1)
    dt = df + timedelta(days=30)

    expected_header = 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=081dec7098dbed6aab839e76501a964aa5b9386a'
    
    req1 = Request(**args).list(params=dict(date_from=df, date_to=dt, page=7))
    req2 = Request(**args).list(params=dict(date_from=dt, date_to=df, page=0))

    # signature does not depends on params
    assert expected_header == req1.auth_header
    assert expected_header == req2.auth_header

def test_sign_get_invoice_details_request():
    req = Request(**args).get(invoice_id=1337)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=40600699c8f72e4165b11f98c4cb93253a3cc7dc' == req.auth_header

def test_sign_download_invoice_request():
    req = Request(**args).download(invoice_id=1337)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=e87ba74ecc88097841fe48d16040aa9675c6cb9a' == req.auth_header


def test_sign_send_email_request():
    req = Request(**args).email(invoice_id=0, data=SEND_EMAIL_WITH_INVOICE_REQUEST)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=491bd26d7f487fb822007899183cf1a29de02f7a' == req.auth_header


SAMPLE_DATA_DIR = './test/data'
#from ifirma.request import API_CREATE_INVOICE_URL

def test_sign_create_vat_payer_invoice_with_known_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_known_customer.request.json').read()
    req = Request(**args).submit(payload)
    
    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=33443d8492027e0fb549f4d4aeed48cc5891cf2f' == req.auth_header

def test_sign_create_vat_payer_invoice_with_new_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_vat_payer_invoice_with_new_customer.request.json').read()
    req = Request(**args).submit(payload)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=418cea6c93f4deadbeb5a5e9b25f63145db6a9c0' == req.auth_header

def test_sign_create_nonvat_payer_invoice_with_new_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_new_customer.request.json').read()
    req = Request(**args).submit(payload)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=c2d3a2c69988792b2941336a3059dc035253407d' == req.auth_header

def test_sign_create_nonvat_payer_invoice_with_known_customer_request():
    payload = open(f'{SAMPLE_DATA_DIR}/create_nonvat_payer_invoice_with_known_customer.request.json').read()
    req = Request(**args).submit(payload)

    assert 'IAPIS user=jan.nowak@ifirma.pl, hmac-sha1=ec0b955b8e63733ecb6ebd461d0783391c09bce1' == req.auth_header