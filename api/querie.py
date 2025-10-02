from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from transformers import VisionEncoderDecoderModel, TrOCRProcessor
from io import BytesIO
from PIL import Image
import time, re, unicodedata

URL_PROJUDI = 'https://consulta.tjpr.jus.br/projudi_consulta/'
MAX_RETRIES = 40

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=options)

    return driver


def get_captcha_response(image:Image, processor: TrOCRProcessor, model: VisionEncoderDecoderModel):
    image = image.convert("RGBA")
    background = Image.new("RGBA", image.size, (255, 255, 255))
    combined = Image.alpha_composite(background, image).convert("RGB")
    pixel_values = processor(combined, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


def get_projudi(row):
    record = {
        'NR_PROCESSO': None,
        'PARTES': [],
        'DISTRIBUICAO': None,
        'CLASSE_PROCESSUAL': None
    }


    elements = row.find_all(attrs={"nowrap": True})
    processo_html = elements[0]
    record['NR_PROCESSO'] = processo_html.text.strip()
    record['DISTRIBUICAO'] = elements[1].text.strip()

    classe_element = row.find_all(attrs={"style": "text-align:center"})[-1]
    classe_element = classe_element.text.strip().split('\n')
    record['CLASSE_PROCESSUAL'] = classe_element[0].strip() + ' ' + classe_element[-1].strip()
    record['CLASSE_PROCESSUAL'] = record['CLASSE_PROCESSUAL'].upper()

    partes = [parte for parte in row.find(class_='form').find_all('tr') if parte.text.strip() != '']

    for parte in partes:
        parte = parte.text.split(':')
        tipo_parte = parte[0].strip().upper()

        names = parte[1].strip().split('\n')
        names = [name.upper() for name in names]

        record['PARTES'].append({
            'TIPO': tipo_parte,
            'NAMES': names
        })

    link_processo = 'https://consulta.tjpr.jus.br' + processo_html.find('a')['href']
    return record, link_processo


def get_processo(driver, link_processo: str):
    
    driver.get(link_processo)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')


    result = {}

    # movimentações do processo
    table = soup.find('div', id='idAjaxMovimentacoesmov1Grau1').find('tbody').find_all('tr')
    movimentacoes = []
    for tr in table:
        td = tr.find_all('td')[1:]

        if len(td) == 0:
            continue

        td_evento = td[2].text.strip().upper().split('\t')
        tp_evento = td_evento[0].strip()
        ds_evento = None
        if len(td_evento) > 1:
            ds_evento = td_evento[-1].strip()

        movimentado_lista = td[3].text.strip().upper().split('\t')
        movimentado = movimentado_lista[0].strip()
        if len(movimentado_lista) > 1:
            movimentado += ' - ' + movimentado_lista[-1].strip() # cargo

        movimentado = movimentado.replace("\xa0", " ")
        movimentacoes.append({
            'SEQUENCIA': td[0].text.strip(),
            'DATA': td[1].text.strip(),
            'TP_EVENTO': tp_evento,
            'DS_EVENTO': ds_evento,
            'MOVIMENTADO': movimentado,
        })

    result['MOVIMENTACOES'] = movimentacoes
    

    # informações do processo
    table = soup.find('table', class_='form').find_all('tr')
    result.update({
        'STATUS': table[0].text.strip().upper().split('\n')[-1],
        'CLASSE_PROCESSUAL': table[1].text.strip().upper().split('-')[-1].strip(),
        'ASSUNTO_PRINCIPAL': table[2].text.strip().upper().split('-')[-1].strip(),
        'NIVEL_SIGILO': table[3].text.strip().upper().split('\n')[-1].strip(),
    })


    info_geral = {}
    table = soup.find('div', id='tabprefix0').find_all('tr')[1:]
    for tr in table:
        tds = tr.find_all('td')
        tds = [td for td in tds if td.text.strip() != ""]
        labels = [
            value.text.strip().replace(':', '').upper()
            for value in tr.find_all('td', class_=['label', 'labelRadio'])
        ]
        init = 0
        while init * 2 < len(tds):
            label = ''.join([c for c in unicodedata.normalize('NFKD', labels[init]) if not unicodedata.combining(c)])
            info_geral[label] = " ".join(value.strip() for value in tds[init * 2 + 1].text.strip().split('\t') if value.strip() != "").upper()
            init += 1


    # informação geral do processo
    result.update(info_geral)

    container_partes = soup.find('div', id='includeContent')
    tables = container_partes.find_all('table', class_='resultTable')

    names = [name.text.strip().upper() for name in container_partes.find_all('h4')]

    partes = []

    for index, table in enumerate(tables):

        table = table.find_all('tr', class_=['even', 'odd'])

        for row in table:
            tds = row.find_all('td')

            nome = tds[0].text.strip().split('\t')[0].strip().upper()
            observacao = tds[1].text.strip().replace('(', '').replace(')', '').upper()

            advogados = [
                " ".join(text.strip() for text in li.text.strip().split('\n') if text.strip() != "").upper()
                for li in tds[2].find_all('li')
            ]


            # if len(advogados) > 1:

            # # if 'PARTE SEM ADVOGADO' not in tds[2].text.strip().upper():
            # #     advogados = [
            # #         advogado.strip()
            # #         for advogado in tds[2].find('li')
            # #         for advogado in advogado.strip().split('\n')
            # #         if advogado.strip() != ""
            # #     ]

            # #     advogados = " ".join(item for item in advogados).upper()

            # # else:
            # #     advogados = 'PARTE SEM ADVOGADO'

            partes.append({
                'TIPO': names[index],
                'NAME': nome,
                'OBSERVACAO': observacao if observacao else None,
                'ADVOGADOS': advogados
            })

    result.update({'PARTES': partes})

    return result


def consulta(cpf_cnpj:str):
    
    driver = None

    try:

        driver = get_driver()
        driver.get(URL_PROJUDI)

        processor = TrOCRProcessor.from_pretrained("anuashok/ocr-captcha-v3")
        model = VisionEncoderDecoderModel.from_pretrained("anuashok/ocr-captcha-v3")

        iframe = driver.find_element(By.ID, 'mainFrame')
        driver.switch_to.frame(iframe)

        filtro_basico = driver.find_element(By.ID, 'divFiltroBasico')
        input_cpf = filtro_basico.find_element(By.ID, 'cpfCnpj')
        input_cpf.clear()
        input_cpf.send_keys(cpf_cnpj)

        message = None

        for _ in range(MAX_RETRIES):

            tag_img = filtro_basico.find_element(By.ID, 'captchaImage')
            png_bytes = tag_img.screenshot_as_png
            imagem = Image.open(BytesIO(png_bytes))
            response_captcha = get_captcha_response(imagem, processor, model)
            
            response_captcha = response_captcha.strip().lower()
            response_captcha = re.sub(r'[^a-zA-Z0-9 ]', '', response_captcha)[:5]
            
            if len(response_captcha) != 5:
                filtro_basico = driver.find_element(By.ID, 'divFiltroBasico')
                refresh = driver.find_element(By.ID, 'refresh-button')
                refresh.click()
                message = True
                continue

            print("PASSOU:", response_captcha)

            input_response = filtro_basico.find_element(By.NAME, 'answer')
            input_response.send_keys(response_captcha)

            input_element = driver.find_element(By.XPATH, '//input[@value="Pesquisar"]')
            input_element.click()

            time.sleep(2)

            try:

                message = driver.find_element(By.ID, 'errorMessages').text.replace('\n', ' ')

                # 'Alguns erros foram encontrados: CPF/CNPJ inválido OAB inválido!'

                if 'captcha inválida' in message.lower():
                    filtro_basico = driver.find_element(By.ID, 'divFiltroBasico')
                    continue

                
                return {
                    'data': None,
                    'message': message
                }

            except:
                message = None
                break #significa que não teve mensagem de erro

        if message:
            return {
                'data': None,
                'message': 'Erro ao tentar validar o captcha'
            }

        table = driver.find_element(By.CLASS_NAME, 'resultTable')

        soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')
        tr = soup.find_all(class_=['even', 'odd'])

        processos = []

        for row in tr:

            processo_html = row.find(attrs={"nowrap": True})
            link_processo = 'https://consulta.tjpr.jus.br' + processo_html.find('a')['href']

            processo = get_processo(driver, link_processo)
            processos.append(processo)

        return {
            'data': processos,
            'message': 'OK'
        }
    
    except Exception as e:
        raise Exception(e)
    
    finally:
        if driver: driver.quit()
