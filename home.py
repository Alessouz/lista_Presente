from flask import Flask, render_template, request, send_from_directory
import smtplib
import email.message
from jinja2 import Environment, FileSystemLoader
import json
import os
from urllib.parse import unquote
import re

# Carregar os templates usando o Jinja2
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('landing_page.html')

# Função para carregar os dados do arquivo JSON
def load_data():
    try:
        with open('data.json', 'r') as f:
            # Verifica se o arquivo está vazio
            if os.stat('data.json').st_size == 0:
                return {}
            else:
                return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar os dados no arquivo JSON


def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


app = Flask(__name__)

# Lista de itens

lista_de_itens = [
    'CAFETEIRA',
    'SANDUICHEIRA',
    'LIQUIDIFICADOR',
    'BATEDEIRA',
    'AIR FRYER',
    'PANELA ELÉTRICA',
    'JOGO DE PANELAS ANTIADERENTES',
    'JOGO DE PANELAS',
    'PANELA DE PRESSÃO',
    'MIXER',
    'VENTILADOR',
    'ASPIRADOR DE PÓ',
    'PIPOQUEIRA',
    'VARAL DE CHÃO',
    'FERRO DE PASSAR ROUPA',
    'TÁBUA DE PASSAR ROUPA.',
    'TAPETE DE SALA',
    'SAPATEIRA',
    'ESPELHO DE CORPO',
    'CORTINA BLECAUTE',
    'JOGO DE LENÇOL COM ELÁSTICO (QUEEN)',
    'JOGO DE LENÇOL COM ELÁSTICO (QUEEN)',
    'JOGO DE LENÇOL COM ELÁSTICO (QUEEN).',
    'JOGO DE LENÇOL COM ELÁSTICO (QUEEN)..',
    'EDREDOM DE CASAL',
    'EDREDOM DE CASAL',
    'DREDOM DE CASAL',
    'MANTA DE CASAL + ALMOFADA',
    'MANTA DE CASAL + ALMOFADA.',
    'MANTA%20DE%20CASAL%20+%20ALMOFADA..',
    'TOALHA DE CORPO + PORTA RETRATO',
    'TOALHA DE CORPO + PORTA RETRATO.',
    'TOALHA DE CORPO + TOALHA DE ROSTO',
    'TOALHA DE CORPO + TOALHA DE ROSTO.',
    'PREGADOR +CESTO DE ROUPA G',
    'PREGADOR +FRIGIDEIRA ANTIADERENTE',
    'PREGADOR + LIXEIRA DE PIA',
    'PANO DE PRATO + PORTA TEMPERO',
    'PANO DE PRATO + KIT POTES HERMÉTICOS',
    'PANO DE PRATO + KIT POTES HERMÉTICOS.',
    'PANO DE PRATO + CUSCUZEIRA',
    'PANO DE PRATO + JOGO DE XÍCARAS',
    'PANO DE PRATO + COLHER DE SILICONE',
    'PANO DE PRATO + JOGO DE TALHERES',
    'JOGO DE TALHERES + DESCASCADOR',
    'JOGO DE COPOS + KIT COLHER DE PAU',
    'JOGO DE COPOS + JARRA DE SUCO 1L ACRÍLICO',
    'JARRA DE SUCO 1L + COPO MEDIDOR',
    'JARRA DE ÁGUA 2L VIDRO + 2 TAÇAS',
    'JARRA DE ÁGUA 2L + ESCORREDOR DE ARROZ INOX',
    'GARRAFA DE VIDRO 1L + LEITEIRA',
    'GARRAFA TÉRMICA DE CAFÉ + PORTA ÓLEO',
    'LEITEIRA + KIT POTES DE PLÁSTICO',
    'ASSADEIRA REDONDA P + ESPREMEDOR DE LIMÃO',
    'ESPREMEDOR DE FRUTA + FRUTEIRA',
    'CONJUNTO ASSADERIAS DE ALUMÍNIO + POTES COM TAMPA',
    'JOGO DE UTENSÍLIOS + BATEDOR DE CARNE',
    'JOGO DE UTENSÍLIOS + SOCADOR DE ALHO',
    'ESCORREDOR DE MASSAS + ASSADEIRA REDONDA M',
    'JOGO DE PRATOS BRANCO + COADOR DE CAFÉ',
    'JOGO DE PRATOS BRANCO + SALEIRO',
    'JOGO DE SOBREMESA + TÁBUA DE MADEIRA',
    'JOGO DE SOBREMESA + COLHER DE SORVETE',
    'AMOLADOR DE FACAS + PEGADOR DE SILICONE',
    'PORTA FRIOS + RALADOR MÉDIO',
    'BOLEIRA + ESPÁTULA DE BOLO',
    'CHALEIRA + FACA DE PÃO',
    'JOGO DE POTES DE COZINHA + CORTADOR DE PIZZA',
    'KIT POTES HERMÉTICOS + COLHER DE SUCO',
    'ESCORREDOR DE LOUÇA + CABIDES DE MADEIRA',
    'CABIDES DE MADEIRA + VASSOURA DE PELO',
    'CABIDES DE MADEIRA + RODO',
    'KIT PANO DE CHÃO + JOGO DE TAPETES DE COZINHA',
    'KIT PANO DE CHÃO + JOGO DE TAPETES DE COZINHA.',
    'KIT PANO DE CHÃO + JOGO DE TAPETES DE COZINHA..',
    'KIT PANO DE CHÃO + MOBI',
    'KIT PANO DE CHÃO + JOGO DE FLANELAS',
    'VASSOURA DE PELO + PÁ',
    'LIXEIRA DE COZINHA (CHÃO) + RODINHO DE PIA',
    'ESPANADOR G + LUVA TÉRMICA',
    'TABULEIRO RETANGULAR M + BALDE',
    'JOGO DE TAPETES DE BANHEIRO + PORTA SABONETE',
    'JOGO DE TAPETES DE BANHEIRO + ESCOVA SANITÁRIA',
    'JOGO DE TAPETES DE BANHEIRO + LIXEIRA DE BANHEIRO',
    'JOGO DE TAPETES DE BANHEIRO + POTE DE SABÃO EM PÓ',
    'CLAVICULÁRIO + TAPETE DE BEM-VINDO',
    'TESOURA DE COZINHA + ROLO DE MASSAS',
    'TRAVESSEIROS + PUXA SACO',
    'PORTA ESCOVA DE DENTES + PROTETOR DE TRAVESSEIRO',
    'DESCANSO DE PANELA + TAPETE ANTIADERENTE PARA BOX',
]

# Adicione mais novos itens aqui
novos_itens = [
    'ESCOVA ROLO DE ADESIVO + 2 SACOLAS RECICLÁVEIS',
    'ESCOVA DE LAVAR ROUPAS + UMIDIFICADOR',
    'ITEM 3'
]

# Adicione os novos itens à lista existente
lista_de_itens.extend(novos_itens)

url_encoded = "MANTA%20DE%20CASAL%20+%20ALMOFADA.."

# Decodificar a string
decoded_text = unquote(url_encoded)

# Remover símbolos e espaços da string decodificada
cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', decoded_text)

# Imprimir o resultado
print(cleaned_text)

def enviar_email(mensagem, destinatario):
    msg = email.message.Message()
    msg['Subject'] = "Escolheram um item na lista do chá "
    msg['From'] = 'filho.pantaleao@gmail.com'
    msg['To'] = destinatario
    password = 'bgcnbtygirlzgmjs'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(mensagem)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')
    s.quit()

def chunk_list(lst, chunk_size):
    """Divide uma lista em pedaços do tamanho especificado."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('/templates/landing_page.html')

itens_por_pagina = len(lista_de_itens) // 3
lista_dividida = chunk_list(lista_de_itens, itens_por_pagina)

@app.route('/')
def landing_page():
    # Carrega os dados do arquivo JSON
    data = load_data()
    itens_escolhidos = list(data.values())

    return render_template('landing_page.html', lista_de_itens=lista_dividida[0], itens_escolhidos=itens_escolhidos)

# Rota para servir as imagens estáticas
@app.route('/imagens/<path:filename>')
def servir_imagens(filename):
    return send_from_directory('imagens', filename)

@app.route('/pagina2')
def pagina2():
    data = load_data()
    itens_escolhidos = list(data.values())
    return render_template('pagina2.html', lista_de_itens=lista_dividida[1], itens_escolhidos=itens_escolhidos)

@app.route('/pagina3')
def pagina3():
    data = load_data()
    itens_escolhidos = list(data.values())
    return render_template('pagina3.html', lista_de_itens=lista_dividida[2], itens_escolhidos=itens_escolhidos)

@app.route('/item/<item>')
def item_details(item):
    return render_template('formulario.html', item=item)

@app.route('/enviar_email', methods=['POST'])
def enviar_formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        item_escolhido = request.form['item_escolhido']

        # Carrega os dados do arquivo JSON
        data = load_data()

        # Verifica se o item já foi escolhido
        if item_escolhido in data.values():
            return render_template('erro.html', item=item_escolhido)

        # Adiciona as informações no arquivo JSON
        data[nome] = item_escolhido
        save_data(data)

        mensagem = f"""
        <p>Olá, Alessandro !</p>
        <p>{nome}, escolheu o item: {item_escolhido}</p>
        """

        # Definir o endereço de e-mail de destino como o seu endereço de e-mail
        email_destino = 'filho.pantaleao@gmail.com'

        # Passa a mensagem e o endereço de e-mail de destino como argumentos
        enviar_email(mensagem, email_destino)
        return render_template('sucesso.html')

@app.route('/url_decode', methods=['GET'])
def url_decode():
    encoded_url = request.args.get('url')
    decoded_url = unquote(encoded_url)
    return decoded_url

if __name__ == '__main__':
    app.run(debug=True)
