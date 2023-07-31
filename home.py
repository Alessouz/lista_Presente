from flask import Flask, render_template, request
import smtplib
import email.message
import json
import os

app = Flask(__name__)

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
'TÁBUA DE PASSAR ROUPA',
'TAPETE DE SALA',
'SAPATEIRA',
'ESPELHO DE CORPO',
'CORTINA BLECAUTE',
'JOGO DE LENÇOL C/ ELÁSTICO (QUEEN)',
'JOGO DE LENÇOL C/ ELÁSTICO (QUEEN)',
'JOGO DE LENÇOL C/ ELÁSTICO (QUEEN)',
'JOGO DE LENÇOL C/ ELÁSTICO (QUEEN)',
'EDREDOM DE CASAL',
'EDREDOM DE CASAL',
'DREDOM DE CASAL',
'MANTA DE CASAL + ALMOFADA',
'MANTA DE CASAL + ALMOFADA',
'MANTA DE CASAL + ALMOFADA',
'TOALHA DE CORPO + PORTA RETRATO',
'TOALHA DE CORPO + PORTA RETRATO',
'TOALHA DE CORPO + TOALHA DE ROSTO',
'TOALHA DE CORPO + TOALHA DE ROSTO',
'PREGADOR +CESTO DE ROUPA G',
'PREGADOR +FRIGIDEIRA ANTIADERENTE',
'PREGADOR + LIXEIRA DE PIA',
'PANO DE PRATO + PORTA TEMPERO',
'PANO DE PRATO + KIT POTES HERMÉTICOS',
'PANO DE PRATO + KIT POTES HERMÉTICOS',
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
'CONJUNTO ASSADERIAS DE ALUMÍNIO + POTES C/ TAMPA',
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
'KIT PANO DE CHÃO + JOGO DE TAPETES DE COZINHA',
'KIT PANO DE CHÃO + JOGO DE TAPETES DE COZINHA',
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

# Carregar os dados do arquivo JSON
itens_selecionados = list(load_data().values())

@app.route('/')
def landing_page():
    return render_template('landing_page.html', lista_de_itens=lista_de_itens)

@app.route('/pagina2')
def pagina2():
    return render_template('pagina2.html', lista_de_itens=lista_de_itens)

@app.route('/pagina3')
def pagina3():
    return render_template('pagina3.html', lista_de_itens=lista_de_itens)

@app.route('/item/<item>')
def item_details(item):
    return render_template('formulario.html', item=item, selecionado=item in itens_selecionados)

@app.route('/enviar_email', methods=['POST'])
def enviar_formulario():
    if request.method == 'POST':
        nome = request.form['nome']
        item_escolhido = request.form['item_escolhido']

        # Verifica se o item já foi selecionado
        if item_escolhido in itens_selecionados:
            return f"O item '{item_escolhido}' já foi selecionado."

        # Verifica se o item já foi selecionado
        if item_escolhido in itens_selecionados:
            return render_template('erro.html', item=item_escolhido)

        # Adiciona o item à lista de itens selecionados
        itens_selecionados.append(item_escolhido)

        # Salva os dados no arquivo JSON
        data = load_data()
        data[nome] = item_escolhido
        save_data(data)

        mensagem = f"""
        <p>Olá, Alessandro !</p>
        <p>{nome}, escolheu o item: {item_escolhido}</p>
        """

        # Definir o endereço de e-mail de destino como o seu endereço de e-mail
        email_destino = 'filho.pantaleao@gmail.com'  # Insira o e-mail do destinatário aqui

        enviar_email(mensagem, email_destino)  # Passa a mensagem e o endereço de e-mail de destino como argumentos
        return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)
